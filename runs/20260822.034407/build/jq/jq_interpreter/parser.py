"""Parser boundary producing an immutable AST."""

import json

from .ast import Comma, Filter, Identity, Literal, Pipeline
from .errors import CompileError
from .lexer import Token, tokenize


class Parser:
    """Precedence-aware parser for the foundation grammar."""

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._position = 0

    def parse(self) -> Filter:
        result = self._parse_comma()
        if self._peek().kind != "EOF":
            raise CompileError("unexpected token")
        return result

    def _parse_comma(self) -> Filter:
        result = self._parse_pipeline()
        while self._accept("COMMA"):
            result = Comma(result, self._parse_pipeline())
        return result

    def _parse_pipeline(self) -> Filter:
        result = self._parse_atom()
        while self._accept("PIPE"):
            result = Pipeline(result, self._parse_atom())
        return result

    def _parse_atom(self) -> Filter:
        token = self._peek()
        if self._accept("DOT"):
            return Identity()
        if token.kind in {"STRING", "NUMBER", "ATOM"}:
            self._position += 1
            try:
                return Literal(json.loads(token.value))
            except json.JSONDecodeError as error:
                raise CompileError("invalid literal") from error
        if self._accept("LPAREN"):
            result = self._parse_comma()
            if not self._accept("RPAREN"):
                raise CompileError("missing closing parenthesis")
            return result
        raise CompileError("expected filter")

    def _peek(self) -> Token:
        return self._tokens[self._position]

    def _accept(self, kind: str) -> bool:
        if self._peek().kind == kind:
            self._position += 1
            return True
        return False


def parse(source: str) -> Filter:
    """Compile source text into an AST or raise :class:`CompileError`."""

    return Parser(tokenize(source)).parse()
