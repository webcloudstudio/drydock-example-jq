"""Lexical scanner for jq source text."""

from dataclasses import dataclass
from enum import Enum, auto
import re

from .errors import CompileError


class TokenKind(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    FIELD = auto()
    BINDING = auto()
    FORMAT = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    DELIMITER = auto()
    INTERPOLATION_START = auto()
    INTERPOLATION_END = auto()
    END = auto()
    IDENTITY = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    text: str
    position: int


_KEYWORDS = {"as", "def", "module", "import", "include", "if", "then", "else", "elif", "and", "or", "end", "reduce", "foreach", "try", "catch", "label", "break"}
_OPERATORS = ("//=", "?//", "!=", "==", "|=", "+=", "-=", "*=", "/=", "%=", "<=", ">=", "..", "//")
_DELIMITERS = set(".?!=;,,:|+-*/%$<>{}[]()")
_NUMBER = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_QUALIFIED_NAME = re.compile(r"(?:[A-Za-z_][A-Za-z_0-9]*::)*[A-Za-z_][A-Za-z_0-9]*")


def _error(source: str, position: int, message: str) -> CompileError:
    line = source.count("\n", 0, position) + 1
    line_start = source.rfind("\n", 0, position) + 1
    return CompileError(f"{message} at line {line}, column {position - line_start + 1}")


def _scan_string(source: str, start: int) -> tuple[list[Token], int]:
    tokens = [Token(TokenKind.STRING, '"', start)]
    position = start + 1
    text_start = position
    while position < len(source):
        character = source[position]
        if character == "\\":
            if position + 1 >= len(source):
                raise _error(source, position, "unterminated string")
            if source[position + 1] == "(":
                if text_start < position:
                    tokens.append(Token(TokenKind.STRING, source[text_start:position], text_start))
                tokens.append(Token(TokenKind.INTERPOLATION_START, "\\(", position))
                expression_start = position + 2
                cursor = expression_start
                depth = 1
                quoted_expression = False
                escaped_expression = False
                while cursor < len(source):
                    current = source[cursor]
                    if quoted_expression:
                        if escaped_expression:
                            escaped_expression = False
                        elif current == "\\":
                            escaped_expression = True
                        elif current == '"':
                            quoted_expression = False
                    elif current == '"':
                        quoted_expression = True
                    elif current == "(":
                        depth += 1
                    elif current == ")":
                        depth -= 1
                        if depth == 0:
                            inner = tokenize(source[expression_start:cursor])
                            tokens.extend(inner[:-1])
                            tokens.append(Token(TokenKind.INTERPOLATION_END, ")", cursor))
                            position = cursor + 1
                            text_start = position
                            break
                    cursor += 1
                else:
                    raise _error(source, position, "unterminated interpolation")
                continue
            if source[position + 1] == "u":
                escape = source[position + 2:position + 6]
                if len(escape) != 4 or not re.fullmatch(r"[0-9A-Fa-f]{4}", escape):
                    raise _error(source, position, "invalid unicode escape")
                position += 6
            else:
                if source[position + 1] not in '"\\/bfnrt':
                    raise _error(source, position, "invalid escape")
                position += 2
            continue
        if character == '"':
            if text_start < position:
                tokens.append(Token(TokenKind.STRING, source[text_start:position], text_start))
            tokens.append(Token(TokenKind.STRING, '"', position))
            return tokens, position + 1
        if ord(character) < 0x20:
            raise _error(source, position, "control character in string")
        position += 1
    raise _error(source, start, "unterminated string")


def tokenize(source: str) -> list[Token]:
    """Tokenize jq source, retaining offsets and rejecting lexical errors."""
    tokens: list[Token] = []
    position = 0
    while position < len(source):
        character = source[position]
        if character.isspace():
            position += 1
            continue
        if character == "#":
            newline = source.find("\n", position)
            position = len(source) if newline < 0 else newline + 1
            continue
        if character == '"':
            string_tokens, position = _scan_string(source, position)
            tokens.extend(string_tokens)
            continue
        number = _NUMBER.match(source, position)
        if number:
            tokens.append(Token(TokenKind.NUMBER, number.group(), position))
            position = number.end()
            continue
        if character == "." and position + 1 < len(source) and source[position + 1].isalpha():
            name = _NAME.match(source, position + 1)
            assert name is not None
            tokens.append(Token(TokenKind.FIELD, source[position:name.end()], position))
            position = name.end()
            continue
        if character == "$":
            name = _QUALIFIED_NAME.match(source, position + 1)
            if not name:
                raise _error(source, position, "invalid binding")
            tokens.append(Token(TokenKind.BINDING, source[position:name.end()], position))
            position = name.end()
            continue
        if character == "@":
            name = _NAME.match(source, position + 1)
            if not name:
                raise _error(source, position, "invalid format")
            tokens.append(Token(TokenKind.FORMAT, source[position:name.end()], position))
            position = name.end()
            continue
        qualified = _QUALIFIED_NAME.match(source, position)
        if qualified:
            text = qualified.group()
            kind = TokenKind.KEYWORD if text in _KEYWORDS else TokenKind.IDENTIFIER
            tokens.append(Token(kind, text, position))
            position = qualified.end()
            continue
        operator = next((value for value in _OPERATORS if source.startswith(value, position)), None)
        if operator:
            tokens.append(Token(TokenKind.OPERATOR, operator, position))
            position += len(operator)
            continue
        if character in _DELIMITERS:
            kind = TokenKind.IDENTITY if character == "." else TokenKind.DELIMITER
            tokens.append(Token(kind, character, position))
            position += 1
            continue
        raise _error(source, position, "unexpected character")
    tokens.append(Token(TokenKind.END, "", len(source)))
    return tokens
