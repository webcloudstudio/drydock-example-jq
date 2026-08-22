"""Lexical boundary for jq source text."""

from dataclasses import dataclass
from enum import Enum, auto

from .errors import CompileError


class TokenKind(Enum):
    IDENTITY = auto()
    END = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    position: int


def tokenize(source: str) -> list[Token]:
    """Tokenize the foundation syntax, preserving source positions."""
    tokens: list[Token] = []
    for position, character in enumerate(source):
        if character.isspace():
            continue
        if character == ".":
            tokens.append(Token(TokenKind.IDENTITY, character, position))
            continue
        raise CompileError(f"unexpected character at position {position}")
    tokens.append(Token(TokenKind.END, "", len(source)))
    return tokens
