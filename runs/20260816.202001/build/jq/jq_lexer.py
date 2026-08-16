"""Lexer for the jq language.

The scanner follows the token spellings and string rules in ``sources/lexer.l``.
Tokens retain both an absolute offset and a one-based line/column location so
the parser can produce useful diagnostics without reparsing source text.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int
    line: int = 1
    column: int = 1

    @property
    def text(self) -> str:
        """Compatibility alias for callers that call token spelling ``text``."""
        return self.value


class LexError(ValueError):
    """Raised when source cannot be converted into jq tokens."""


_KEYWORDS = {
    "as", "def", "if", "then", "else", "elif", "end", "reduce", "foreach",
    "and", "or", "try", "catch", "label", "break", "import", "include", "module",
}
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_QUALIFIED = re.compile(r"(?:[A-Za-z_][A-Za-z0-9_]*::)*[A-Za-z_][A-Za-z0-9_]*")
_NUMBER = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_FORMATS = re.compile(r"@[A-Za-z0-9_]+")
_OPERATORS = (
    "?//", "//=", "|=", "+=", "-=", "*=", "/=", "%=", "==", "!=", "<=", ">=", "..", "//",
)
_SINGLE = set(".?=;,|:+-*/%<>()[]{}")
_ESCAPES = set('"\\/bfnrt')


def _location(source: str, position: int) -> tuple[int, int]:
    line = source.count("\n", 0, position) + 1
    prior = source.rfind("\n", 0, position)
    return line, position - prior


def _token(kind: str, value: str, source: str, position: int) -> Token:
    line, column = _location(source, position)
    return Token(kind, value, position, line, column)


def _decode_string(raw: str, source: str, position: int) -> str:
    try:
        return json.loads('"' + raw + '"')
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise LexError(f"invalid string escape at position {position}") from exc


def _interpolation_end(source: str, start: int) -> int:
    """Return the index of the ')' closing an interpolation starting at *start*."""
    depth = 0
    i = start
    while i < len(source):
        if source[i] == '"':
            i = _quoted_end(source, i)
            continue
        if source[i] == "#":
            newline = source.find("\n", i)
            i = len(source) if newline < 0 else newline + 1
            continue
        if source[i] == "(":
            depth += 1
        elif source[i] == ")":
            if depth == 0:
                return i
            depth -= 1
        i += 1
    raise LexError(f"unterminated string interpolation at position {start - 2}")


def _quoted_end(source: str, opening: int) -> int:
    i = opening + 1
    while i < len(source):
        if source[i] == "\\":
            i += 2
        elif source[i] == '"':
            return i + 1
        else:
            i += 1
    raise LexError(f"unterminated string at position {opening}")


def _scan_string(source: str, opening: int) -> tuple[list[Token], int, bool]:
    """Scan a quoted string, returning tokens, next offset, and interpolation flag."""
    i = opening + 1
    text_start = i
    parts: list[Token] = []
    interpolated = False
    while i < len(source):
        char = source[i]
        if char == '"':
            if interpolated or i != text_start:
                if i > text_start:
                    parts.append(_token("qqstring_text", _decode_string(source[text_start:i], source, text_start), source, text_start))
            if interpolated:
                parts.append(_token("qqstring_end", '"', source, i))
                return parts, i + 1, True
            return [_token("string", _decode_string(source[text_start:i], source, text_start), source, opening)], i + 1, False
        if char == "\\" and i + 1 < len(source) and source[i + 1] == "(":
            if not interpolated:
                parts.append(_token("qqstring_start", '"', source, opening))
            if i > text_start:
                parts.append(_token("qqstring_text", _decode_string(source[text_start:i], source, text_start), source, text_start))
            end = _interpolation_end(source, i + 2)
            parts.append(_token("interpolation_start", "\\(", source, i))
            parts.extend(tokenize(source[i + 2:end], _offset=i + 2)[:-1])
            parts.append(_token("interpolation_end", ")", source, end))
            interpolated = True
            i = end + 1
            text_start = i
            continue
        if char == "\\":
            if i + 1 >= len(source):
                raise LexError(f"invalid string escape at position {i}")
            if source[i + 1] == "u":
                if not re.match(r"[0-9A-Fa-f]{4}", source[i + 2:i + 6]):
                    raise LexError(f"invalid unicode escape at position {i}")
                i += 6
            elif source[i + 1] in _ESCAPES:
                i += 2
            else:
                raise LexError(f"invalid string escape at position {i}")
        else:
            if ord(char) < 0x20:
                raise LexError(f"unescaped control character at position {i}")
            i += 1
    raise LexError(f"unterminated string at position {opening}")


def tokenize(source: str, *, _offset: int = 0) -> list[Token]:
    """Tokenize jq source, raising :class:`LexError` on lexical errors."""
    if _offset:
        # Interpolation token positions are absolute in the original source.
        local = tokenize(source, _offset=0)
        return [Token(t.kind, t.value, t.position + _offset, t.line, t.column + _offset) for t in local]
    tokens: list[Token] = []
    delimiters: list[str] = []
    i = 0
    while i < len(source):
        c = source[i]
        if c.isspace():
            i += 1
            continue
        if c == "#":
            while True:
                newline = source.find("\n", i)
                if newline < 0:
                    i = len(source)
                    break
                backslashes = 0
                cursor = newline - 1
                while cursor >= i and source[cursor] == "\\":
                    backslashes += 1
                    cursor -= 1
                i = newline + 1
                if backslashes % 2 == 0:
                    break
            continue
        if c == '"':
            string_tokens, i, _ = _scan_string(source, i)
            tokens.extend(string_tokens)
            continue
        match = _FORMATS.match(source, i)
        if match:
            tokens.append(_token("format", match.group()[1:], source, i)); i = match.end(); continue
        match = _NUMBER.match(source, i)
        if match:
            value = match.group(); tokens.append(_token("number", value, source, i)); i = match.end(); continue
        if c == "." and i + 1 < len(source) and (source[i + 1].isalpha() or source[i + 1] == "_"):
            match = _NAME.match(source, i + 1); assert match
            value = match.group(); tokens.append(_token("field", value, source, i)); i = match.end(); continue
        if c == "$":
            match = _QUALIFIED.match(source, i + 1)
            if not match:
                raise LexError(f"invalid binding at position {i}")
            value = match.group(); tokens.append(_token("binding", value, source, i)); i = match.end(); continue
        match = _QUALIFIED.match(source, i)
        if match:
            value = match.group(); tokens.append(_token("word", value, source, i)); i = match.end(); continue
        operator = next((op for op in _OPERATORS if source.startswith(op, i)), None)
        if operator:
            tokens.append(_token("operator", operator, source, i)); i += len(operator); continue
        if c in _SINGLE:
            if c in "([{": delimiters.append({"(": ")", "[": "]", "{": "}"}[c])
            elif c in ")]}":
                if not delimiters or delimiters.pop() != c:
                    raise LexError(f"mismatched closing delimiter at position {i}")
            tokens.append(_token("delimiter" if c in "()[]{}" else "operator", c, source, i)); i += 1; continue
        raise LexError(f"unexpected character at position {i}")
    if delimiters:
        raise LexError("unterminated delimiter")
    tokens.append(_token("eof", "", source, len(source)))
    return tokens
