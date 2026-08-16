"""Lexer for the jq frontend.

The lexer deliberately keeps string tokens intact; interpolation is parsed by
the parser because its contents are jq expressions rather than JSON text.
"""
from dataclasses import dataclass
import json
import re


@dataclass(frozen=True)
class Token:
    kind: str
    text: str


class LexError(ValueError):
    pass


KEYWORDS = {
    "as", "import", "include", "module", "def", "if", "then", "else",
    "elif", "and", "or", "end", "reduce", "foreach", "try", "catch",
    "label", "break",
}
OPERATORS = (
    "//=", "?//", "|=", "+=", "-=", "*=", "/=", "%=", "==", "!=",
    "<=", ">=", "..",
)
SINGLE = set(".?=,;:|+-*/%()[]{}$<>")
NUMBER = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")
WORD = re.compile(r"(?:[A-Za-z_][A-Za-z_0-9]*::)*[A-Za-z_][A-Za-z_0-9]*\Z")


def _string_end(source: str, start: int) -> int:
    index = start + 1
    while index < len(source):
        if source[index] == '"':
            backslashes = 0
            cursor = index - 1
            while cursor >= start and source[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                raw = source[start:index + 1]
                try:
                    # Validate ordinary JSON escapes now.  \( is jq
                    # interpolation and is intentionally validated later.
                    json.loads(raw.replace("\\(", "\\\\(")) if "\\(" in raw else json.loads(raw)
                except json.JSONDecodeError as error:
                    raise LexError("invalid string escape") from error
                return index + 1
        if source[index] == "\n" or source[index] == "\r":
            raise LexError("unterminated string")
        index += 1
    raise LexError("unterminated string")


def tokenize(source: str) -> list[Token]:
    result: list[Token] = []
    index = 0
    while index < len(source):
        char = source[index]
        if char.isspace():
            index += 1
            continue
        if char == "#":
            index += 1
            while index < len(source):
                if source[index] in "\r\n":
                    index += 1
                    break
                # An odd trailing backslash continues the comment line.
                if source[index] == "\\" and index + 1 < len(source) and source[index + 1] == "\n":
                    index += 2
                    continue
                index += 1
            continue
        if char == '"':
            end = _string_end(source, index)
            result.append(Token("STRING", source[index:end]))
            index = end
            continue
        if char == "@":
            match = re.match(r"@[A-Za-z0-9_]+", source[index:])
            if not match:
                raise LexError("invalid format token")
            text = match.group(0)
            result.append(Token("FORMAT", text[1:]))
            index += len(text)
            continue
        operator = next((value for value in OPERATORS if source.startswith(value, index)), None)
        if operator is not None:
            result.append(Token(operator, operator))
            index += len(operator)
            continue
        if char == "." and index + 1 < len(source) and re.match(r"[A-Za-z_]", source[index + 1]):
            match = re.match(r"\.[A-Za-z_][A-Za-z_0-9]*", source[index:])
            assert match is not None
            text = match.group(0)
            result.append(Token("FIELD", text[1:]))
            index += len(text)
            continue
        if char == "$":
            match = re.match(r"\$(?:[A-Za-z_][A-Za-z_0-9]*::)*[A-Za-z_][A-Za-z_0-9]*", source[index:])
            if not match:
                result.append(Token("$", "$"))
                index += 1
            else:
                text = match.group(0)
                result.append(Token("BINDING", text[1:]))
                index += len(text)
            continue
        if char in SINGLE:
            result.append(Token(char, char))
            index += 1
            continue
        end = index
        while end < len(source) and not source[end].isspace() and source[end] not in SINGLE and source[end] != '"' and source[end] != "#":
            if any(source.startswith(op, end) for op in OPERATORS):
                break
            end += 1
        text = source[index:end]
        if not text:
            raise LexError(f"invalid character: {source[index]!r}")
        if text in {"true", "false", "null"} or NUMBER.fullmatch(text):
            kind = "LITERAL"
        elif WORD.fullmatch(text):
            kind = text if text in KEYWORDS else "IDENT"
        else:
            raise LexError(f"invalid token: {text}")
        result.append(Token(kind, text))
        index = end
    result.append(Token("EOF", ""))
    return result
