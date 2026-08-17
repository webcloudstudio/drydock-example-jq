"""Lexer for the jq source language.

The parser in this small interpreter consumes a compact token spelling, while
the public lexer retains token kind and source location information for tests
and diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re


class LexError(ValueError):
    """Raised when jq source cannot be lexed."""


@dataclass(frozen=True)
class Token:
    kind: str
    value: str | int | float | None
    start: int
    end: int
    line: int
    column: int


_NUMBER = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_BINDING = re.compile(r"\$([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)")
_FIELD = re.compile(r"\.([A-Za-z_][A-Za-z_0-9]*)")

_KEYWORDS = {
    "as", "import", "include", "module", "def", "if", "then", "else",
    "elif", "and", "or", "end", "reduce", "foreach", "try", "catch",
    "label", "break",
}
_OPERATORS = (
    "//=", "?//", "!=", "==", "|=", "+=", "-=", "*=", "/=", "%=",
    "<=", ">=", "..", "//",
)
_SINGLE = set(".?=;, :|+-*/%<>[]{}()".replace(" ", ""))


class Lexer:
    """Convert jq source into located tokens and validate lexical forms."""

    def __init__(self, source: str) -> None:
        self.source = source

    def tokens(self) -> list[Token]:
        source = self.source
        result: list[Token] = []
        i = 0
        line = 1
        column = 1
        n = len(source)

        def advance(text: str) -> None:
            nonlocal line, column
            pieces = text.splitlines(keepends=True)
            if len(pieces) > 1:
                line += len(pieces) - 1
                column = len(pieces[-1]) + 1
            else:
                column += len(text)

        while i < n:
            ch = source[i]
            if ch in " \t\r\n" or ch == "\ufeff":
                advance(ch)
                i += 1
                continue
            if ch == "#":
                start = i
                while i < n and source[i] not in "\r\n":
                    i += 1
                advance(source[start:i])
                continue
            start, start_line, start_col = i, line, column
            if ch == '"':
                i = self._scan_string(i)
                raw = source[start:i]
                if "\\(" in raw:
                    value = raw
                else:
                    try:
                        value = json.loads(raw)
                    except json.JSONDecodeError as exc:
                        raise LexError(f"invalid string literal at line {start_line}, column {start_col}") from exc
                result.append(Token("STRING", value, start, i, start_line, start_col))
                advance(raw)
                continue
            match = _NUMBER.match(source, i)
            if match:
                raw = match.group(0)
                value: int | float = float(raw) if any(c in raw for c in ".eE") else int(raw)
                i = match.end()
                result.append(Token("NUMBER", value, start, i, start_line, start_col))
                advance(raw)
                continue
            match = _BINDING.match(source, i)
            if match:
                raw = match.group(0)
                i = match.end()
                result.append(Token("BINDING", raw[1:], start, i, start_line, start_col))
                advance(raw)
                continue
            match = _FIELD.match(source, i)
            if match:
                raw = match.group(0)
                i = match.end()
                result.append(Token("FIELD", match.group(1), start, i, start_line, start_col))
                advance(raw)
                continue
            if ch == "@":
                match = _NAME.match(source, i + 1)
                if not match:
                    raise LexError(f"invalid format at line {line}, column {column}")
                raw = source[i:match.end()]
                i = match.end()
                result.append(Token("FORMAT", raw[1:], start, i, start_line, start_col))
                advance(raw)
                continue
            match = _NAME.match(source, i)
            if match:
                raw = match.group(0)
                i = match.end()
                kind = raw.upper() if raw in _KEYWORDS else "IDENT"
                result.append(Token(kind, raw, start, i, start_line, start_col))
                advance(raw)
                continue
            operator = next((op for op in _OPERATORS if source.startswith(op, i)), None)
            if operator is not None:
                i += len(operator)
                result.append(Token(operator, operator, start, i, start_line, start_col))
                advance(operator)
                continue
            if ch in _SINGLE:
                i += 1
                result.append(Token(ch, ch, start, i, start_line, start_col))
                advance(ch)
                continue
            raise LexError(f"invalid character {ch!r} at line {line}, column {column}")
        return result

    def cleaned_source(self) -> str:
        """Return source with comments blanked, preserving string contents."""
        chars = list(self.source)
        for token in self.tokens():
            del token
        in_string = False
        escaped = False
        i = 0
        while i < len(chars):
            if in_string:
                if escaped:
                    escaped = False
                elif chars[i] == "\\":
                    escaped = True
                elif chars[i] == '"':
                    in_string = False
            elif chars[i] == '"':
                in_string = True
            elif chars[i] == '#':
                while i < len(chars) and chars[i] not in "\r\n":
                    chars[i] = ' '
                    i += 1
                continue
            i += 1
        return "".join(chars)

    def _scan_string(self, start: int) -> int:
        source = self.source
        i = start + 1
        while i < len(source):
            if source[i] == '"':
                return i + 1
            if source[i] == "\\":
                if i + 1 >= len(source):
                    raise LexError("unterminated escape in string")
                esc = source[i + 1]
                if esc == "u":
                    if i + 5 >= len(source) or not re.fullmatch(r"[0-9A-Fa-f]{4}", source[i + 2:i + 6]):
                        raise LexError("invalid unicode escape")
                    i += 6
                    continue
                if esc not in '"\\/bfnrt(':
                    raise LexError(f"invalid escape \\{esc}")
                i += 2
                continue
            if ord(source[i]) < 0x20:
                raise LexError("unescaped control character in string")
            i += 1
        raise LexError("unterminated string")
