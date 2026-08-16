"""Precedence-aware parser for the foundational jq expression subset."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from jq_lexer import Token, tokenize


class ParseError(ValueError):
    pass


@dataclass(frozen=True)
class Identity:
    pass


@dataclass(frozen=True)
class Literal:
    value: Any


@dataclass(frozen=True)
class Field:
    name: str


@dataclass(frozen=True)
class Iterate:
    pass


@dataclass(frozen=True)
class Pipe:
    left: Any
    right: Any


@dataclass(frozen=True)
class Comma:
    left: Any
    right: Any


@dataclass(frozen=True)
class Array:
    expression: Any


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def current(self) -> Token:
        return self.tokens[self.position]

    def take(self, kind: str) -> Token:
        token = self.current()
        if token.kind != kind:
            raise ParseError(f"expected {kind}")
        self.position += 1
        return token

    def parse(self) -> Any:
        expression = self.parse_comma()
        self.take("EOF")
        return expression

    def parse_comma(self) -> Any:
        expression = self.parse_pipe()
        while self.current().kind == ",":
            self.position += 1
            expression = Comma(expression, self.parse_pipe())
        return expression

    def parse_pipe(self) -> Any:
        expression = self.parse_primary()
        while self.current().kind == "|":
            self.position += 1
            expression = Pipe(expression, self.parse_primary())
        return expression

    def parse_primary(self) -> Any:
        token = self.current()
        if token.kind == ".":
            self.position += 1
            if self.current().kind == "WORD":
                expression: Any = Field(self.tokens[self.position].text)
                self.position += 1
            else:
                expression = Identity()
        elif token.kind == "LITERAL":
            self.position += 1
            expression = Literal(json.loads(token.text))
        elif token.kind == "STRING":
            self.position += 1
            expression = Literal(json.loads(token.text))
        elif token.kind == "[":
            self.position += 1
            expression = Array(self.parse_comma())
            self.take("]")
        else:
            raise ParseError("unexpected token")
        if self.current().kind == "[":
            self.position += 1
            self.take("]")
            expression = Iterate()
        return expression


def parse(source: str) -> Any:
    return Parser(tokenize(source)).parse()
