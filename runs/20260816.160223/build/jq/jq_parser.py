"""Precedence-aware jq parser and immutable AST."""
from dataclasses import dataclass
import json
from typing import Any
from jq_lexer import Token, tokenize

class ParseError(ValueError):
    pass

@dataclass(frozen=True)
class Identity: pass
@dataclass(frozen=True)
class Literal: value: Any
@dataclass(frozen=True)
class Field: base: Any; name: str; optional: bool = False
@dataclass(frozen=True)
class Index: base: Any; key: Any; optional: bool = False
@dataclass(frozen=True)
class Iterate: base: Any; optional: bool = False
@dataclass(frozen=True)
class Slice: base: Any; start: Any; end: Any; optional: bool = False
@dataclass(frozen=True)
class Pipe: left: Any; right: Any
@dataclass(frozen=True)
class Comma: left: Any; right: Any
@dataclass(frozen=True)
class Binary: operator: str; left: Any; right: Any
@dataclass(frozen=True)
class Unary: operator: str; expression: Any
@dataclass(frozen=True)
class Array: expression: Any
@dataclass(frozen=True)
class Object: pairs: tuple[tuple[Any, Any], ...]
@dataclass(frozen=True)
class Interpolated: parts: tuple[Any, ...]
@dataclass(frozen=True)
class Call: name: str; args: tuple[Any, ...]
@dataclass(frozen=True)
class Binding: expression: Any; name: str; body: Any
@dataclass(frozen=True)
class Conditional: condition: Any; yes: Any; no: Any
@dataclass(frozen=True)
class Try: expression: Any; handler: Any | None
@dataclass(frozen=True)
class Reduce: source: Any; name: str; initial: Any; update: Any
@dataclass(frozen=True)
class Label: name: str; body: Any
@dataclass(frozen=True)
class Break: name: str
@dataclass(frozen=True)
class Definition: name: str; args: tuple[str, ...]; body: Any
@dataclass(frozen=True)
class Program: definitions: tuple[Definition, ...]; body: Any; module: Any | None = None


def _is_constant(node: Any) -> bool:
    """Return whether a node is a compile-time JSON value."""
    if isinstance(node, Literal):
        return not (isinstance(node.value, tuple) and node.value[0] in {"var", "call"})
    if isinstance(node, Array):
        return _is_constant(node.expression)
    if isinstance(node, Object):
        return all(_is_constant(key) and _is_constant(value) for key, value in node.pairs)
    return False


def _validate_variables(program: Program) -> None:
    """Reject variable references that are not visible at compile time."""
    def visit(node: Any, bound: frozenset[str], labels: frozenset[str] = frozenset()) -> None:
        if isinstance(node, Literal):
            if isinstance(node.value, tuple) and node.value[0] == "var" and node.value[1] not in bound:
                raise ParseError(f"undefined variable: ${node.value[1]}")
            return
        if isinstance(node, Binding):
            visit(node.expression, bound, labels)
            visit(node.body, bound | {node.name}, labels)
            return
        if isinstance(node, Break):
            if node.name not in labels:
                raise ParseError(f"undefined break label: ${node.name}")
            return
        if isinstance(node, Label):
            visit(node.body, bound, labels | {node.name})
            return
        if isinstance(node, Reduce):
            visit(node.source, bound, labels)
            visit(node.initial, bound, labels)
            visit(node.update, bound | {node.name}, labels)
            return
        if isinstance(node, Definition):
            visit(node.body, bound | frozenset(node.args))
            return
        if isinstance(node, Program):
            for definition in node.definitions:
                visit(definition, frozenset())
            visit(node.body, frozenset())
            if node.module is not None:
                if not _is_constant(node.module):
                    raise ParseError("module metadata must be constant")
                if not isinstance(node.module, Object):
                    raise ParseError("module metadata must be an object")
            return
        if isinstance(node, Object):
            for key, value in node.pairs:
                if isinstance(key, Literal) and not isinstance(key.value, str):
                    raise ParseError("constant object key must be a string")
                visit(key, bound)
                visit(value, bound)
            return
        if isinstance(node, (Identity,)):
            return
        if hasattr(node, "__dataclass_fields__"):
            for field in node.__dataclass_fields__:
                child = getattr(node, field)
                if isinstance(child, tuple):
                    for item in child:
                        if hasattr(item, "__dataclass_fields__"):
                            visit(item, bound, labels)
                        elif isinstance(item, tuple):
                            for nested in item:
                                if hasattr(nested, "__dataclass_fields__"):
                                    visit(nested, bound, labels)
                elif hasattr(child, "__dataclass_fields__"):
                    visit(child, bound, labels)

    visit(program, frozenset())

PRECEDENCE = {"//": 2, "=": 3, "|=": 3, "+=": 3, "-=": 3, "*=": 3,
              "/=": 3, "%=": 3, "or": 4, "and": 5, "==": 6, "!=": 6,
              "<": 6, ">": 6, "<=": 6, ">=": 6, "+": 7, "-": 7,
              "*": 8, "/": 8, "%": 8, "|": 1, ",": 0}

class Parser:
    def __init__(self, tokens: list[Token]): self.tokens, self.pos = tokens, 0
    def current(self) -> Token: return self.tokens[self.pos]
    def accept(self, kind: str) -> Token | None:
        if self.current().kind == kind:
            token = self.current(); self.pos += 1; return token
        return None
    def take(self, kind: str) -> Token:
        token = self.accept(kind)
        if token is None: raise ParseError(f"expected {kind}, got {self.current().kind}")
        return token
    def parse(self) -> Program:
        defs: list[Definition] = []
        while self.accept("def"):
            name = self.take("IDENT").text
            args: list[str] = []
            if self.accept("("):
                if self.current().kind != ")":
                    while True:
                        token = self.current()
                        if token.kind not in {"IDENT", "BINDING"}: raise ParseError("invalid function parameter")
                        args.append(token.text); self.pos += 1
                        if not self.accept(";"): break
                self.take(")")
            self.take(":"); body = self.expression(0); self.take(";")
            defs.append(Definition(name, tuple(args), body))
        module = None
        if self.accept("module"):
            module = self.expression(0)
            self.take(";")
        body = self.expression(0)
        self.take("EOF")
        program = Program(tuple(defs), body, module)
        _validate_variables(program)
        return program
    def expression(self, minimum: int) -> Any:
        left = self.prefix()
        if minimum <= 1 and self.accept("as"):
            name = self.take("BINDING").text
            self.take("|")
            left = Binding(left, name, self.expression(1))
        while self.current().kind in PRECEDENCE and PRECEDENCE[self.current().kind] >= minimum:
            op = self.current().kind; precedence = PRECEDENCE[op]; self.pos += 1
            right = self.expression(precedence + (0 if op in {"|", "//", "="} else 1))
            left = Pipe(left, right) if op == "|" else Comma(left, right) if op == "," else Binary(op, left, right)
        return left
    def prefix(self) -> Any:
        token = self.current()
        if token.kind in {"-", "+"}:
            self.pos += 1; return Unary(token.kind, self.expression(9))
        if token.kind == "try":
            self.pos += 1; expr = self.expression(3)
            handler = None
            if self.accept("catch"): handler = self.expression(3)
            return Try(expr, handler)
        if token.kind == "label":
            self.pos += 1
            name = self.take("BINDING").text
            self.take("|")
            return Label(name, self.expression(1))
        if token.kind == "break":
            self.pos += 1
            return Break(self.take("BINDING").text)
        if token.kind == "if":
            self.pos += 1; condition = self.expression(0); self.take("then"); yes = self.expression(0)
            if self.accept("else"): no = self.expression(0)
            else: no = Identity()
            self.take("end"); return Conditional(condition, yes, no)
        if token.kind == "reduce":
            self.pos += 1; source = self.expression(3); self.take("as"); name = self.take("BINDING").text
            self.take("("); initial = self.expression(0); self.take(";"); update = self.expression(0); self.take(")")
            return Reduce(source, name, initial, update)
        if token.kind == "(":
            self.pos += 1; value = self.expression(0); self.take(")")
        elif token.kind == ".": self.pos += 1; value = Identity()
        elif token.kind == "FIELD": self.pos += 1; value = Field(Identity(), token.text)
        elif token.kind == "BINDING": self.pos += 1; value = Literal(("var", token.text))
        elif token.kind == "LITERAL": self.pos += 1; value = Literal(json.loads(token.text))
        elif token.kind == "STRING": self.pos += 1; value = self.string_value(token.text)
        elif token.kind == "FORMAT": self.pos += 1; value = Call(token.text, ())
        elif token.kind == "IDENT":
            self.pos += 1; name = token.text
            if self.accept("("):
                args = []
                if self.current().kind != ")":
                    while True:
                        args.append(self.expression(0))
                        if not self.accept(";"): break
                self.take(")"); value = Call(name, tuple(args))
            else: value = Literal(True if name == "true" else False if name == "false" else None if name == "null" else ("call", name))
        elif token.kind == "[":
            self.pos += 1
            if self.accept("]"):
                value = Literal([])
            else:
                inner = self.expression(0); self.take("]"); value = Array(inner)
        elif token.kind == "{": value = self.object_value()
        else: raise ParseError(f"unexpected token {token.kind}")
        while True:
            if self.accept("."):
                if self.accept("["):
                    key = self.expression(0); self.take("]"); value = Index(value, key)
                else: value = Field(value, self.take("STRING").text[1:-1])
            elif self.current().kind == "FIELD": value = Field(value, self.take("FIELD").text)
            elif self.accept("["):
                if self.accept("]"): value = Iterate(value)
                else:
                    first = None if self.current().kind == ":" else self.expression(0)
                    if self.accept(":"):
                        end = None if self.current().kind == "]" else self.expression(0); self.take("]"); value = Slice(value, first, end)
                    else: self.take("]"); value = Index(value, first)
            elif self.accept("?"):
                if isinstance(value, Field): value = Field(value.base, value.name, True)
                elif isinstance(value, Iterate): value = Iterate(value.base, True)
                elif isinstance(value, Index): value = Index(value.base, value.key, True)
                else: value = Try(value, None)
            else: break
        return value
    def object_value(self) -> Object:
        self.take("{"); pairs: list[tuple[Any, Any]] = []
        if self.accept("}"): return Object(tuple(pairs))
        while True:
            key = self.current()
            if key.kind in {"IDENT", "as", "def", "if", "then", "else", "end", "and", "or"}:
                self.pos += 1; key_ast: Any = Literal(key.text)
                if self.accept(":"): val = self.expression(1)
                else: val = Field(Identity(), key.text)
            elif key.kind == "STRING": self.pos += 1; key_ast = self.string_value(key.text); self.take(":"); val = self.expression(1)
            elif key.kind == "BINDING": self.pos += 1; key_ast = Literal(key.text); val = Literal(("var", key.text)) if not self.accept(":") else self.expression(1)
            elif key.kind == "(":
                self.pos += 1
                key_ast = self.expression(0)
                self.take(")"); self.take(":"); val = self.expression(1)
            else: raise ParseError("invalid object key")
            pairs.append((key_ast, val))
            if not self.accept(","): break
        self.take("}"); return Object(tuple(pairs))
    def string_value(self, text: str) -> Any:
        body = text[1:-1]; parts: list[Any] = []; literal = []; index = 0
        while index < len(body):
            if body.startswith("\\(", index):
                if literal: parts.append(Literal(json.loads('"'+''.join(literal)+'"'))); literal=[]
                depth=1; cursor=index+2
                while cursor < len(body) and depth:
                    if body[cursor] == "(": depth += 1
                    elif body[cursor] == ")": depth -= 1
                    cursor += 1
                if depth: raise ParseError("unterminated interpolation")
                parts.append(parse(body[index+2:cursor-1])); index=cursor
            else: literal.append(body[index]); index += 1
        if literal or not parts: parts.append(Literal(json.loads('"'+''.join(literal)+'"')))
        return parts[0] if len(parts)==1 else Interpolated(tuple(parts))

def parse(source: str) -> Program: return Parser(tokenize(source)).parse()
