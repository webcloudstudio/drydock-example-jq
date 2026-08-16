"""Small lexical boundary; the parser owns jq grammar decisions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    kind: str
    text: str


class LexError(ValueError):
    pass


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    index = 0
    while index < len(source):
        char = source[index]
        if char.isspace():
            index += 1
        elif char in ".[]|,():{}$":
            tokens.append(Token(char, char))
            index += 1
        elif char == '"':
            end = index + 1
            escaped = False
            while end < len(source):
                if source[end] == '"' and not escaped:
                    break
                escaped = source[end] == "\\" and not escaped
                if source[end] != "\\":
                    escaped = False
                end += 1
            if end >= len(source):
                raise LexError("unterminated string")
            tokens.append(Token("STRING", source[index : end + 1]))
            index = end + 1
        else:
            end = index
            while end < len(source) and not source[end].isspace() and source[end] not in ".[]|,():{}$\"":
                end += 1
            text = source[index:end]
            if text in {"true", "false", "null"}:
                kind = "LITERAL"
            elif text.replace(".", "", 1).replace("-", "", 1).isdigit():
                kind = "LITERAL"
            else:
                kind = "WORD"
            tokens.append(Token(kind, text))
            index = end
    tokens.append(Token("EOF", ""))
    return tokens
