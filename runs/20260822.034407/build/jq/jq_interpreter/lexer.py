"""Lexical analysis for jq source programs."""

from dataclasses import dataclass
import re

from .ast import SourceLocation
from .errors import CompileError


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    location: SourceLocation


# Keep the sign as a separate jq operator.  The upstream lexer accepts the
# same decimal spellings as its flex rule, including a decimal point without
# following digits and leading zeroes; semantic validation belongs later.
_NUMBER = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_NAMESPACE = re.compile(r"(?:[A-Za-z_][A-Za-z_0-9]*::)*[A-Za-z_][A-Za-z_0-9]*")
_ESCAPES = set('"\\/bfnrt')
_KEYWORDS = {name: name.upper() for name in (
    "as import include module def if then else elif and or end reduce foreach try catch label break"
).split()}
_KEYWORDS["elif"] = "ELSE_IF"
_OPERATORS = {
    "//=": "SETDEFINEDOR", "?//": "ALTERNATION", "//": "DEFINEDOR", "!=": "NEQ", "==": "EQ", "|=": "SETPIPE",
    "+=": "SETPLUS", "-=": "SETMINUS", "*=": "SETMULT", "/=": "SETDIV", "%=": "SETMOD",
    "<=": "LESSEQ", ">=": "GREATEREQ", "..": "REC",
}
_SINGLE = {"|":"PIPE", ",":"COMMA", ".":"DOT", "?":"QUESTION", "=":"EQUAL", ";":"SEMICOLON",
           ":":"COLON", "+":"PLUS", "-":"MINUS", "*":"MULT", "/":"DIV", "%":"MOD", "$":"DOLLAR",
           "<":"LESS", ">":"GREATER", "(":"LPAREN", ")":"RPAREN", "[":"LBRACKET", "]":"RBRACKET",
           "{":"LBRACE", "}":"RBRACE"}


def _advance(text: str, line: int, column: int) -> tuple[int, int]:
    parts = text.split("\n")
    return (line + len(parts) - 1, len(parts[-1]) + 1) if len(parts) > 1 else (line, column + len(text))


def _string_end(source: str, start: int) -> int:
    index = start + 1
    while index < len(source):
        char = source[index]
        if char == '"':
            return index + 1
        if ord(char) < 0x20:
            raise CompileError("invalid control character in string")
        if char == "\\":
            index += 1
            if index >= len(source) or source[index] not in _ESCAPES | {"u", "("}:
                raise CompileError("invalid string escape")
            if source[index] == "u":
                digits = source[index + 1:index + 5]
                if len(digits) != 4 or not re.fullmatch(r"[0-9A-Fa-f]{4}", digits):
                    raise CompileError("invalid unicode escape")
                index += 5
            else:
                index += 1
        else:
            index += 1
    raise CompileError("unterminated string")


def _interpolation_end(source: str, start: int) -> int:
    """Return the index after the closing paren of ``\\(`` at *start*.

    Parentheses inside the expression are balanced, and quoted jq strings
    are skipped so a paren in a nested string cannot terminate the
    interpolation.  This mirrors the lexer state's delimiter handling
    without attempting to parse the expression here.
    """
    depth = 1
    index = start + 2
    while index < len(source):
        char = source[index]
        if char == '"':
            index = _string_end(source, index)
            continue
        if char == "#":
            while index < len(source) and source[index] != "\n":
                index += 1
            continue
        if char == "\\":
            index += 2
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    raise CompileError("unterminated string interpolation")


def _has_interpolation(source: str, start: int) -> bool:
    index = start + 1
    while index < len(source):
        if source[index] == '"':
            return False
        if source[index] == "\\":
            if index + 1 < len(source) and source[index + 1] == "(":
                return True
            index += 2
            continue
        index += 1
    return False


def _tokenize_qqstring(source: str, start: int) -> tuple[list[Token], int]:
    """Tokenize a jq string containing zero or more interpolations."""
    tokens: list[Token] = [Token("QQSTRING_START", '"', SourceLocation(0, 0))]
    index = start + 1
    text_start = index
    while index < len(source):
        char = source[index]
        if char == '"':
            if text_start < index:
                tokens.append(Token("QQSTRING_TEXT", source[text_start:index], SourceLocation(0, 0)))
            tokens.append(Token("QQSTRING_END", '"', SourceLocation(0, 0)))
            return tokens, index + 1
        if char == "\\" and index + 1 < len(source) and source[index + 1] == "(":
            if text_start < index:
                tokens.append(Token("QQSTRING_TEXT", source[text_start:index], SourceLocation(0, 0)))
            end = _interpolation_end(source, index)
            tokens.append(Token("QQSTRING_INTERP_START", "\\(", SourceLocation(0, 0)))
            tokens.extend(tokenize(source[index + 2:end])[:-1])
            tokens.append(Token("QQSTRING_INTERP_END", ")", SourceLocation(0, 0)))
            index = end + 1
            text_start = index
            continue
        if char == "\\":
            if index + 1 >= len(source) or source[index + 1] not in _ESCAPES | {"u", "("}:
                raise CompileError("invalid string escape")
            if source[index + 1] == "u":
                digits = source[index + 2:index + 6]
                if len(digits) != 4 or not re.fullmatch(r"[0-9A-Fa-f]{4}", digits):
                    raise CompileError("invalid unicode escape")
                index += 6
                continue
            index += 2
        else:
            if ord(char) < 0x20:
                raise CompileError("invalid control character in string")
            index += 1
    raise CompileError("unterminated string")


def tokenize(source: str) -> list[Token]:
    """Tokenize jq source, rejecting malformed lexical input."""
    tokens: list[Token] = []
    index, line, column = 0, 1, 1

    def add(kind: str, value: str, at_line: int, at_column: int) -> None:
        tokens.append(Token(kind, value, SourceLocation(at_line, at_column)))

    while index < len(source):
        char = source[index]
        if char.isspace():
            line, column = _advance(char, line, column)
            index += 1
            continue
        if char == "#":
            while index < len(source):
                if source[index] == "\n":
                    preceding = 0
                    cursor = index - 1
                    while cursor >= 0 and source[cursor] == "\\":
                        preceding += 1
                        cursor -= 1
                    index += 1
                    line, column = line + 1, 1
                    if preceding % 2 == 0:
                        break
                else:
                    index += 1
                    column += 1
            continue
        at_line, at_column = line, column
        operator = next((op for op in sorted(_OPERATORS, key=len, reverse=True) if source.startswith(op, index)), None)
        if operator:
            add(_OPERATORS[operator], operator, at_line, at_column)
            index += len(operator); column += len(operator); continue
        if source.startswith("$__loc__", index):
            add("LOC", "$__loc__", at_line, at_column)
            index += 8; column += 8; continue
        if char == "@":
            match = re.match(r"@[A-Za-z0-9_]+", source[index:])
            if not match:
                raise CompileError(f"invalid character at {line}:{column}")
            value = match.group(0)
            add("FORMAT", value[1:], at_line, at_column)
            index += len(value); column += len(value); continue
        if char == '"':
            end = _string_end(source, index) if not _has_interpolation(source, index) else None
            if end is not None:
                value = source[index:end]
                add("STRING", value, at_line, at_column)
            else:
                qq_tokens, end = _tokenize_qqstring(source, index)
                cursor = index
                for token in qq_tokens:
                    if token.kind == "QQSTRING_START":
                        position = index
                    else:
                        position = source.find(token.value, cursor, end)
                        if position < 0:
                            position = cursor
                    token_line, token_column = _advance(
                        source[index:position], at_line, at_column
                    )
                    add(token.kind, token.value, token_line, token_column)
                    cursor = position + len(token.value)
            line, column = _advance(source[index:end], line, column); index = end; continue
        number = _NUMBER.match(source, index)
        if number:
            value = number.group(0)
            add("NUMBER", value, at_line, at_column)
            index += len(value); column += len(value); continue
        if char == "." and index + 1 < len(source) and (source[index + 1].isalpha() or source[index + 1] == "_"):
            match = _NAME.match(source, index + 1); assert match is not None
            value = match.group(0)
            add("FIELD", value, at_line, at_column)
            index = match.end(); column += len(value) + 1; continue
        if char == "$":
            match = _NAMESPACE.match(source, index + 1)
            if match:
                value = match.group(0)
                add("BINDING", value, at_line, at_column)
                index = match.end(); column += len(value) + 1; continue
        name = _NAMESPACE.match(source, index)
        if name:
            value = name.group(0)
            kind = _KEYWORDS.get(value, "ATOM" if value in {"true", "false", "null"} else "IDENT")
            add(kind, value, at_line, at_column)
            index = name.end(); column += len(value); continue
        if char in _SINGLE:
            add(_SINGLE[char], char, at_line, at_column)
            index += 1; column += 1; continue
        raise CompileError(f"invalid character at {line}:{column}")
    tokens.append(Token("EOF", "", SourceLocation(line, column)))
    return tokens
