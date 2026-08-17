"""Small lexical boundary for the foundational filter syntax."""

from __future__ import annotations

from dataclasses import dataclass
import json

from .diagnostics import CompileError


@dataclass(frozen=True)
class Token:
    kind: str
    value: object
    position: int


def tokenize(program: str) -> list[Token]:
    """Tokenize literals, dot, comma, and identifiers with source positions."""
    tokens: list[Token] = []
    index = 0
    while index < len(program):
        char = program[index]
        if char.isspace():
            index += 1
        elif char == ".":
            tokens.append(Token("DOT", char, index))
            index += 1
        elif char == ",":
            tokens.append(Token("COMMA", char, index))
            index += 1
        elif char == '"':
            decoder = json.JSONDecoder()
            try:
                value, end = decoder.raw_decode(program[index:])
            except json.JSONDecodeError as exc:
                raise CompileError(f"invalid string at position {index}") from exc
            if not isinstance(value, str):
                raise CompileError(f"invalid string at position {index}")
            tokens.append(Token("LITERAL", value, index))
            index += end
        elif char.isdigit() or char == "-":
            decoder = json.JSONDecoder()
            try:
                value, end = decoder.raw_decode(program[index:])
            except json.JSONDecodeError as exc:
                raise CompileError(f"invalid number at position {index}") from exc
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise CompileError(f"invalid number at position {index}")
            tokens.append(Token("LITERAL", value, index))
            index += end
        elif char.isalpha() or char == "_":
            end = index + 1
            while end < len(program) and (program[end].isalnum() or program[end] == "_"):
                end += 1
            tokens.append(Token("IDENT", program[index:end], index))
            index = end
        else:
            raise CompileError(f"unexpected character at position {index}")
    tokens.append(Token("EOF", None, len(program)))
    return tokens
