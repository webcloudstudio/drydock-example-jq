"""Parser and immutable AST for the jq language front end.

The parser deliberately keeps evaluation concerns out of the tree.  Every
node records its construct and children, so the generator runtime can choose
how to evaluate it without the parser retaining input or lexical state.
"""

from __future__ import annotations

from dataclasses import dataclass
import json

from jq_lexer import LexError, Token, tokenize


class ParseError(ValueError):
    """Raised for syntax or compile-time jq errors."""


@dataclass(frozen=True)
class Node:
    kind: str
    value: object = None
    children: tuple["Node", ...] = ()

    def __repr__(self) -> str:
        if self.children:
            return f"Node({self.kind!r}, {self.value!r}, {self.children!r})"
        return f"Node({self.kind!r}, {self.value!r})"


_PREC = {",": 100, "//": 20, "=": 30, "|=": 30, "+=": 30, "-=": 30,
         "*=": 30, "/=": 30, "%=": 30, "//=": 30, "or": 40, "and": 50,
         "==": 60, "!=": 60, "<": 60, ">": 60, "<=": 60, ">=": 60,
         "+": 70, "-": 70, "*": 80, "/": 80, "%": 80, "|": 90}
_RIGHT_ASSOC = {"=", "|=", "+=", "-=", "*=", "/=", "%=", "//=", "//", "|"}


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0
        self.functions: set[tuple[str, int]] = set()
        self.bindings: list[set[str]] = [set()]
        self.labels: list[str] = []

    def current(self) -> Token:
        return self.tokens[self.index]

    def take(self) -> Token:
        token = self.current()
        self.index += 1
        return token

    def accept(self, value: str) -> bool:
        if self.current().value == value:
            self.take()
            return True
        return False

    def expect(self, value: str) -> Token:
        if not self.accept(value):
            token = self.current()
            raise ParseError(f"expected {value!r} at position {token.position}")
        return self.tokens[self.index - 1]

    def expect_kind(self, kind: str) -> Token:
        token = self.current()
        if token.kind != kind:
            raise ParseError(f"expected {kind!r} at position {token.position}")
        return self.take()

    def parse(self) -> Node:
        declarations: list[Node] = []
        while self.current().value in {"module", "import", "include", "def"}:
            if self.current().value == "def":
                declarations.append(self.parse_definition())
            else:
                declarations.append(self.parse_module_directive())
        if self.current().kind == "eof":
            raise ParseError("expected filter")
        body = self.expression()
        if self.current().kind != "eof":
            token = self.current()
            raise ParseError(f"unexpected token {token.value!r} at position {token.position}")
        if declarations:
            return Node("program", children=tuple(declarations + [body]))
        return body

    def expression(self, minimum: int = 0) -> Node:
        left = self.term()
        while True:
            token = self.current()
            op = token.value
            if op == "as":
                if minimum > 25:
                    break
                self.take()
                pattern = self.pattern()
                self.expect("|")
                self.bindings[-1].update(self.pattern_names(pattern))
                right = self.expression(0)
                left = Node("as", children=(left, pattern, right))
                continue
            if op not in _PREC or _PREC[op] < minimum:
                break
            self.take()
            next_min = _PREC[op] if op in _RIGHT_ASSOC else _PREC[op] + 1
            right = self.expression(next_min)
            left = Node(op, children=(left, right))
        return left

    def term(self) -> Node:
        token = self.take()
        if token.kind == "eof":
            raise ParseError(f"expected filter at position {token.position}")
        if token.value == ".":
            node = Node("identity")
        elif token.kind == "field":
            node = Node("index", value=token.value, children=(Node("identity"),))
        elif token.kind == "binding":
            if token.value not in self.bindings[-1]:
                # Builtin/private bindings are legal without a local declaration.
                if not token.value.startswith("__") and token.value not in {"ENV", "ARGS"}:
                    raise ParseError(f"undefined variable ${token.value}")
            node = Node("binding", token.value)
        elif token.kind == "number":
            node = Node("literal", json.loads(token.value))
        elif token.kind == "string":
            node = Node("literal", token.value)
        elif token.kind == "qqstring_start":
            node = self.qqstring()
        elif token.value == "if":
            node = self.conditional()
        elif token.value == "try":
            node = self.try_expression()
        elif token.value in {"reduce", "foreach"}:
            node = self.reducer(token.value)
        elif token.value == "label":
            label = self.take()
            if label.kind != "binding":
                raise ParseError("label requires a binding")
            self.expect("|")
            self.labels.append(label.value)
            try:
                body = self.expression()
            finally:
                self.labels.pop()
            node = Node("label", label.value, (body,))
        elif token.value == "break":
            label = self.take()
            if label.kind != "binding":
                raise ParseError("break requires a label")
            if label.value not in self.labels:
                raise ParseError(f"undefined label ${label.value}")
            node = Node("break", label.value)
        elif token.kind in {"word", "format"}:
            node = self.word(token)
        elif token.value == "(" :
            node = self.expression()
            self.expect(")")
        elif token.value == "[":
            node = self.array()
        elif token.value == "{":
            node = self.object()
        elif token.value == "-":
            node = Node("negate", children=(self.term(),))
        elif token.value == "..":
            node = Node("recurse")
        else:
            raise ParseError(f"unexpected token {token.value!r} at position {token.position}")
        return self.postfix(node)

    def word(self, token: Token) -> Node:
        if token.kind == "format":
            base = Node("format", token.value)
            if self.current().kind in {"string", "qqstring_start"}:
                return Node("format_string", children=(base, self.term()))
            return base
        if token.value in {"true", "false", "null", "empty"}:
            return Node(token.value)
        if self.accept("("):
            args = self.arguments()
            return Node("call", token.value, tuple(args))
        return Node("call", token.value, ())

    def postfix(self, node: Node) -> Node:
        while True:
            if self.current().kind == "field":
                field = self.take().value
                optional = self.accept("?")
                node = Node("index_opt" if optional else "index", field, (node,))
            elif self.accept(".") or self.current().kind in {"string", "qqstring_start"}:
                key = self.take()
                if key.kind not in {"string", "qqstring_text"}:
                    raise ParseError(f"expected string field at position {key.position}")
                optional = self.accept("?")
                node = Node("index_opt" if optional else "index", key.value, (node,))
            elif self.accept("["):
                if self.accept("]"):
                    node = Node("iterate", children=(node,))
                else:
                    first = self.expression()
                    if self.accept(":"):
                        second = None if self.current().value in {"]", "?"} else self.expression()
                        self.expect("]")
                        node = Node("slice", children=(node, first, second or Node("null")))
                    else:
                        self.expect("]")
                        node = Node("index", children=(node, first))
                if self.accept("?"):
                    node = Node("optional", children=(node,))
            elif self.accept("?"):
                node = Node("optional", children=(node,))
            else:
                return node

    def arguments(self) -> list[Node]:
        if self.accept(")"):
            return []
        args = [self.expression()]
        while self.accept(";"):
            args.append(self.expression())
        self.expect(")")
        return args

    def array(self) -> Node:
        if self.accept("]"):
            return Node("array", children=())
        value = self.expression()
        self.expect("]")
        return Node("array", children=(value,))

    def object(self) -> Node:
        pairs: list[Node] = []
        if self.accept("}"):
            return Node("object", children=())
        while True:
            key = self.take()
            if key.kind not in {"word", "string", "binding", "qqstring_text"}:
                raise ParseError(f"invalid object key at position {key.position}")
            if self.accept(":"):
                # Commas separate object pairs; they remain available to the
                # object parser rather than becoming the value's comma node.
                value = self.expression(_PREC[","] + 1)
            else:
                value = Node("index", key.value, (Node("identity"),))
            pairs.append(Node("pair", key.value, (value,)))
            if not self.accept(","):
                break
        self.expect("}")
        return Node("object", children=tuple(pairs))

    def conditional(self) -> Node:
        condition = self.expression()
        self.expect("then")
        yes = self.expression()
        branches = [condition, yes]
        while self.accept("elif"):
            branches.extend((self.expression(), self.expect("then") and self.expression()))
        no = Node("identity")
        if self.accept("else"):
            no = self.expression()
        self.expect("end")
        branches.append(no)
        return Node("if", children=tuple(branches))

    def try_expression(self) -> Node:
        expression = self.expression(0)
        if self.accept("catch"):
            return Node("try", children=(expression, self.expression()))
        return Node("try", children=(expression, Node("empty")))

    def reducer(self, kind: str) -> Node:
        # The source ends at the grammar's ``as`` delimiter; ``as`` is not
        # an ordinary binary operator in a reducer.
        source = self.expression(26)
        self.expect("as")
        pattern = self.pattern()
        self.bindings[-1].update(self.pattern_names(pattern))
        self.expect("(")
        initial = self.expression()
        self.expect(";")
        update = self.expression()
        parts = [source, pattern, initial, update]
        if kind == "foreach":
            self.expect(";")
            parts.append(self.expression())
        self.expect(")")
        return Node(kind, children=tuple(parts))

    def pattern(self) -> Node:
        if self.current().kind == "binding":
            return Node("pattern", self.take().value)
        if self.accept("["):
            parts = []
            if self.accept("]"):
                raise ParseError("empty array destructuring pattern")
            parts.append(self.pattern())
            while self.accept(","):
                parts.append(self.pattern())
            self.expect("]")
            return Node("array_pattern", children=tuple(parts))
        if self.accept("{"):
            parts = []
            if self.accept("}"):
                raise ParseError("empty object destructuring pattern")
            while True:
                key = self.take()
                if self.accept(":"):
                    value = self.pattern()
                else:
                    value = Node("pattern", key.value)
                parts.append(Node("pattern_pair", key.value, (value,)))
                if not self.accept(","):
                    break
            self.expect("}")
            return Node("object_pattern", children=tuple(parts))
        raise ParseError("expected destructuring pattern")

    def pattern_names(self, node: Node) -> set[str]:
        if node.kind in {"pattern", "pattern_pair"}:
            names = {str(node.value)} if node.kind == "pattern" else set()
            return names | set().union(*(self.pattern_names(c) for c in node.children))
        return set().union(*(self.pattern_names(c) for c in node.children))

    def qqstring(self) -> Node:
        parts: list[Node] = []
        while self.current().kind != "qqstring_end":
            token = self.take()
            if token.kind == "qqstring_text":
                parts.append(Node("literal", token.value))
            elif token.kind == "interpolation_start":
                parts.append(self.expression())
                self.expect_kind("interpolation_end")
            else:
                raise ParseError(f"invalid string part at position {token.position}")
        self.take()
        return Node("string", children=tuple(parts))

    def parse_definition(self) -> Node:
        self.expect("def")
        name = self.take()
        if name.kind != "word":
            raise ParseError("function definition requires a name")
        params: list[Node] = []
        if self.accept("("):
            if not self.accept(")"):
                params.append(self.pattern() if self.current().kind == "binding" else Node("param", self.take().value))
                while self.accept(";"):
                    params.append(Node("param", self.take().value))
                self.expect(")")
        self.expect(":")
        body = self.expression()
        self.expect(";")
        self.functions.add((name.value, len(params)))
        return Node("def", name.value, tuple(params) + (body,))

    def parse_module_directive(self) -> Node:
        kind = self.take().value
        if kind == "module":
            metadata = self.expression()
            if metadata.kind != "object":
                raise ParseError("module metadata must be constant")
            self.expect(";")
            return Node("module", children=(metadata,))
        path = self.take()
        if path.kind != "string":
            raise ParseError("import path must be constant")
        if kind == "import":
            self.expect("as")
            alias = self.take()
            if alias.kind not in {"word", "binding"}:
                raise ParseError("import requires an alias")
        # Metadata is optional, but if present it must be a constant object.
        metadata = None
        if self.current().value != ";":
            metadata = self.expression()
            if metadata.kind != "object":
                raise ParseError("module metadata must be constant")
        self.expect(";")
        return Node(kind, path.value, () if metadata is None else (metadata,))


def parse(source: str) -> Node:
    """Tokenize and parse *source*, returning an immutable executable AST."""
    try:
        return Parser(tokenize(source)).parse()
    except (LexError, json.JSONDecodeError) as error:
        raise ParseError(str(error)) from error
