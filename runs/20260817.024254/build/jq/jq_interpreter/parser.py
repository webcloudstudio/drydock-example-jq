"""Pratt parser for the executable subset of jq used by the interpreter."""
from __future__ import annotations

from dataclasses import dataclass
from .diagnostics import CompileError
from .lexer import tokenize


@dataclass(frozen=True)
class Filter:
    kind: str
    value: object = None
    children: tuple["Filter", ...] = ()


class Parser:
    # Lower number binds less tightly.  jq's comma is a generator, not an
    # argument separator; semicolons are the argument separators.
    PRECEDENCE = {"=": 0, "|=": 0, "+=": 0, "-=": 0, "*=": 0, "/=": 0,
                  "%=": 0, "//=": 0, "|": 1, ",": 2, "//": 3,
                  "or": 4, "and": 5, "==": 6, "!=": 6, "<": 6,
                  ">": 6, "<=": 6, ">=": 6, "+": 7, "-": 7,
                  "*": 8, "/": 8, "%": 8}

    def __init__(self, source: str) -> None:
        self.source = source
        # A binding is a compile-time name, not a dynamic lookup.  Keeping the
        # names here lets the parser distinguish an unbound `$name` (jq's
        # static error) from a binding introduced by `as`.
        self.bound_names: set[str] = set()
        self.function_names: set[tuple[str, int]] = set()
        self.parameter_names: set[str] = set()
        self.labels: set[str] = set()
        keyword = {"as", "if", "then", "else", "elif", "end", "or", "and", "catch", "label", "break"}
        self.tokens = [((str(t.value) if t.kind == "IDENT" and t.value in keyword else
                         {"NUMBER":"num", "STRING":"str", "IDENT":"id", "FIELD":"field", "BINDING":"binding", "FORMAT":"format"}.get(t.kind, t.kind)), t.value, t.position)
                       for t in tokenize(source)]
        self.pos = 0

    def peek(self, *k: str) -> bool:
        return self.tokens[self.pos][0] in k

    def pop(self, expected: str | None = None) -> tuple[str, object, int]:
        token = self.tokens[self.pos]
        if expected is not None and token[0] != expected:
            raise CompileError(f"expected {expected} at position {token[2]}")
        self.pos += 1
        return token

    def parse(self) -> Filter:
        if self.peek("EOF"):
            raise CompileError("empty filter")
        result = self.query()
        if not self.peek("EOF"):
            raise CompileError(f"unexpected token at position {self.tokens[self.pos][2]}")
        return result

    def query(self) -> Filter:
        # Definitions are expressions in jq: a definition installs a lexical
        # function and the expression after its semicolon is its continuation.
        if self.peek("id") and self.tokens[self.pos][1] == "def":
            self.pop()
            name = str(self.pop("id")[1])
            params: list[tuple[str, str]] = []
            if self.peek("("):
                self.pop()
                if not self.peek(")"):
                    while True:
                        kind, value, _ = self.pop()
                        if kind not in {"id", "binding"}:
                            raise CompileError("expected function parameter")
                        params.append(("value" if kind == "binding" else "filter", str(value)))
                        if not self.peek(";"): break
                        self.pop()
                self.pop(")")
            self.pop(":")
            signature = (name, len(params))
            self.function_names.add(signature)  # permits recursion
            old_params = self.parameter_names
            self.parameter_names = old_params | {p[1] for p in params}
            try:
                body = self.query()
            finally:
                self.parameter_names = old_params
            self.pop(";")
            continuation = self.query()
            return Filter("def", (name, tuple(params)), (body, continuation))
        if self.peek("label"):
            self.pop(); name = str(self.pop("binding")[1]); self.pop("|")
            old_labels = self.labels
            self.labels = old_labels | {name}
            try: body = self.query()
            finally: self.labels = old_labels
            return Filter("label", name, (body,))
        # Binding is deliberately parsed below pipe precedence: `x as $y | f`.
        left = self.expr(0)
        if self.peek("as"):
            self.pop()
            pat = self.pattern()
            patterns = [pat]
            while self.peek("?//"):
                self.pop(); patterns.append(self.pattern())
            pat = patterns[0] if len(patterns) == 1 else Filter("pattern_alt", children=tuple(patterns))
            self.pop("|")
            previous = self.bound_names
            self.bound_names = previous | self._pattern_names(pat)
            try:
                body = self.query()
            finally:
                self.bound_names = previous
            binding = Filter("as", None, (left, pat, body))
            # The input to the binding is the value at the point where `as`
            # appears.  A pipe immediately to its left is therefore outside
            # the binding, not part of its source expression.
            if left.kind == "binary" and left.value == "|":
                return Filter("binary", "|", (left.children[0], Filter("as", None, (left.children[1], pat, body))))
            return binding
        return left

    def _pattern_names(self, pattern: Filter) -> set[str]:
        if pattern.kind == "pattern":
            return {str(pattern.value)}
        if pattern.kind in {"array_pattern", "object_pattern"}:
            values: set[str] = set()
            children = pattern.children if pattern.kind == "array_pattern" else tuple(
                child for _, child in pattern.value
            )
            for child in children:
                values.update(self._pattern_names(child))
            return values
        if pattern.kind == "pattern_alt":
            values: set[str] = set()
            for child in pattern.children:
                values.update(self._pattern_names(child))
            return values
        return set()

    def expr(self, minimum: int) -> Filter:
        left = self.primary()
        while True:
            op = self.tokens[self.pos][0]
            if op not in self.PRECEDENCE or self.PRECEDENCE[op] < minimum:
                break
            precedence = self.PRECEDENCE[op]
            self.pop()
            # assignment and // are right associative; arithmetic is left.
            right = self.expr(precedence if op in {"=", "|=", "+=", "-=", "*=", "/=", "%=", "//=", "//"} else precedence + 1)
            left = Filter("binary", op, (left, right))
        return left

    def pattern(self) -> Filter:
        if self.peek("binding"):
            return Filter("pattern", self.pop()[1])
        if self.peek("["):
            self.pop(); items = []
            if not self.peek("]"):
                while True:
                    items.append(self.pattern())
                    if not self.peek(","): break
                    self.pop()
            self.pop("]"); return Filter("array_pattern", children=tuple(items))
        if self.peek("{"):
            self.pop(); items = []
            while not self.peek("}"):
                key_kind, key_value, _ = self.pop()
                if key_kind == "binding" and self.peek(",", "}"):
                    items.append((str(key_value), Filter("pattern", key_value)))
                else:
                    if key_kind == "binding":
                        key = str(key_value)
                    else:
                        key = str(key_value)
                    self.pop(":"); items.append((key, self.pattern()))
                if not self.peek(","): break
                self.pop()
            self.pop("}"); return Filter("object_pattern", items)
        raise CompileError(f"expected binding at position {self.tokens[self.pos][2]}")

    def primary(self) -> Filter:
        kind, value, position = self.pop()
        if kind == "EOF": raise CompileError("expected filter")
        if kind == "num" or kind == "str":
            node = Filter("template", value) if isinstance(value, list) else Filter("literal", value)
        elif kind == "field":
            node = Filter("field", value, (Filter("identity"),))
        elif kind == ".":
            node = Filter("identity")
        elif kind == "binding":
            if str(value) in self.bound_names:
                node = Filter("binding", value)
            elif str(value) in self.parameter_names:
                node = Filter("param", "@" + str(value))
            else:
                raise CompileError(f"variable is not defined at position {position}")
        elif kind == "break":
            label = str(self.pop("binding")[1])
            if label not in self.labels:
                raise CompileError(f"label is not defined at position {position}")
            node = Filter("break", label)
        elif kind == "..":
            node = Filter("recurse")
        elif kind == "-":
            node = Filter("unary", "-", (self.primary(),))
        elif kind == "(":
            node = self.query(); self.pop(")")
        elif kind == "[":
            parts = []
            if not self.peek("]"):
                parts.append(self.query())
            self.pop("]"); node = Filter("array", children=tuple(parts))
        elif kind == "{":
            pairs = []
            while not self.peek("}"):
                key = self.pop()
                if key[0] == "(" : key_filter = self.query(); self.pop(")")
                elif key[0] == "binding": key_filter = Filter("binding", key[1])
                else: key_filter = Filter("literal", str(key[1]))
                if self.peek(":"):
                    self.pop(); value_filter = self.expr(3)
                else:
                    # {name} and {$name} are shorthand for .name and
                    # $name respectively.  Keywords are legal identifiers in
                    # object literals too.
                    if key[0] == "binding" and self.peek(":"):
                        value_filter = Filter("binding", key[1])
                    elif key[0] == "binding":
                        key_filter = Filter("literal", str(key[1]))
                        value_filter = Filter("binding", key[1])
                    else:
                        value_filter = Filter("field", str(key[1]), (Filter("identity"),))
                pairs.append((key_filter, value_filter))
                if not self.peek(","): break
                self.pop()
            self.pop("}"); node = Filter("object", tuple(pairs))
        elif kind in {"id", "if"}:
            if value in {"true", "false", "null"}: node = Filter("literal", {"true": True, "false": False, "null": None}[value])
            elif value == "empty": node = Filter("empty")
            elif value == "if":
                cond = self.query(); self.pop("then"); yes = self.query()
                no = Filter("literal", None)
                if self.peek("elif"):
                    self.pop(); no = self._parse_elif()
                elif self.peek("else"):
                    self.pop(); no = self.query()
                self.pop("end"); node = Filter("if", children=(cond, yes, no))
            elif value == "try":
                attempt = self.primary() if not self.peek("(") else self.primary()
                handler = Filter("empty")
                if self.peek("catch"):
                    self.pop(); handler = self.query()
                node = Filter("try", children=(attempt, handler))
            elif value in {"reduce", "foreach"}:
                # These are syntactic forms, not ordinary builtins.  The
                # source generator and binding pattern are evaluated once,
                # while init/update/extract are filters over the accumulator.
                source = self.expr(0)
                self.pop("as")
                pattern = self.pattern()
                self.pop("(")
                previous = self.bound_names
                self.bound_names = previous | self._pattern_names(pattern)
                try:
                    init = self.query()
                    self.pop(";")
                    update = self.query()
                    extract = Filter("identity")
                    if value == "foreach" and self.peek(";"):
                        self.pop(); extract = self.query()
                    self.pop(")")
                finally:
                    self.bound_names = previous
                node = Filter(value, (source, pattern, init, update, extract))
            elif value == "def":
                name = str(self.pop("id")[1]); params = []
                if self.peek("("):
                    self.pop()
                    if not self.peek(")"):
                        while True:
                            pk, pv, _ = self.pop(); params.append(("value" if pk == "binding" else "filter", str(pv)))
                            if not self.peek(";"): break
                            self.pop()
                    self.pop(")")
                self.pop(":"); self.function_names.add((name, len(params)))
                old_params = self.parameter_names; self.parameter_names = old_params | {p[1] for p in params}
                try: body = self.query()
                finally: self.parameter_names = old_params
                self.pop(";"); continuation = self.query()
                node = Filter("def", (name, tuple(params)), (body, continuation))
            else: node = self.call_or_builtin(str(value), position)
        elif kind == "format": node = Filter("format", value, (Filter("identity"),))
        else: raise CompileError(f"expected filter at position {position}")
        return self.postfix(node)

    def _parse_elif(self) -> Filter:
        cond = self.query(); self.pop("then"); yes = self.query()
        no = Filter("literal", None)
        if self.peek("elif"):
            self.pop(); no = self._parse_elif()
        elif self.peek("else"):
            self.pop(); no = self.query()
        return Filter("if", children=(cond, yes, no))

    def call_or_builtin(self, name: str, position: int) -> Filter:
        builtins = {"error","length","utf8bytelength","keys","values","type","add","any","all","flatten","sort","unique","reverse","min","max","floor","ceil","abs","not","arrays","objects","iterables","scalars","booleans","nulls","strings","numbers","tojson","fromjson","tostring","tonumber","sqrt","infinite","nan","try","range","map","map_values","contains","has","select","join","split","startswith","endswith","ltrimstr","rtrimstr","trimstr","getpath","setpath","delpaths","del","pow","log2","round","reduce","foreach","isempty","first","last","nth","have_decnum","walk","IN"}
        if name in self.parameter_names and not self.peek("("):
            return Filter("param", "@" + name)
        if not self.peek("("):
            if name not in builtins and (name, 0) not in self.function_names:
                raise CompileError(f"unknown filter at position {position}")
            return Filter("call", name, ())
        self.pop("("); args = []
        if not self.peek(")"):
            while True:
                args.append(self.query())
                if not self.peek(";"): break
                self.pop(";")
        self.pop(")")
        if (name, len(args)) not in self.function_names and name not in builtins:
            raise CompileError(f"unknown function {name}/{len(args)}")
        return Filter("call", name, tuple(args))

    def postfix(self, node: Filter) -> Filter:
        while True:
            if self.peek("field"):
                node = Filter("field", self.pop()[1], (node,))
            elif self.peek(".") and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == "str":
                self.pop(); node = Filter("index", (node, self.primary(), None))
            elif self.peek("["):
                self.pop()
                if self.peek("]"):
                    self.pop(); node = Filter("iterate", (node,))
                else:
                    start = None if self.peek(":") else self.query()
                    if self.peek(":"):
                        self.pop(); end = None if self.peek("]") else self.query(); self.pop("]")
                        node = Filter("slice", (node, start, end))
                    else:
                        self.pop("]"); node = Filter("index", (node, start, None))
            elif self.peek("?"):
                self.pop(); node = Filter("optional", children=(node,))
            else: break
        return node


def parse(program: str) -> Filter:
    return Parser(program).parse()
