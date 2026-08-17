"""Lexer for the jq source forms required by the front end."""

from __future__ import annotations

from dataclasses import dataclass
import re


class LexerError(ValueError):
    """Raised when jq source contains an invalid lexical form."""


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    line: int
    column: int


KEYWORDS = {
    "as", "import", "include", "module", "def", "if", "then", "else",
    "elif", "and", "or", "end", "reduce", "foreach", "try", "catch",
    "label", "break",
}
OPERATORS = (
    "//=", "?//", "!=", "==", "|=", "+=", "-=", "*=", "/=", "%=",
    "<=", ">=", "..", "//",
)
SINGLE = set(".?=;,|:+-*/%$<>()[]{}")


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while self.index < len(self.source):
            char = self.source[self.index]
            if char in " \t\r\n":
                self._advance(char)
                continue
            if char == "#":
                self._skip_comment()
                continue
            start_line, start_column = self.line, self.column
            if self.source.startswith('"', self.index):
                tokens.extend(self._string_tokens())
                continue
            operator = next((op for op in OPERATORS if self.source.startswith(op, self.index)), None)
            if operator:
                tokens.append(Token(operator, operator, start_line, start_column))
                self._advance(operator)
                continue
            if char == "@":
                self._advance(char)
                start = self.index
                while self.index < len(self.source) and (self.source[self.index].isalnum() or self.source[self.index] == "_"):
                    self._advance(self.source[self.index])
                if start == self.index:
                    raise LexerError(f"invalid format at {start_line}:{start_column}")
                tokens.append(Token("FORMAT", self.source[start:self.index], start_line, start_column))
                continue
            if char.isdigit() or (char == "." and self.index + 1 < len(self.source) and self.source[self.index + 1].isdigit()):
                tokens.append(self._number())
                continue
            if char.isalpha() or char == "_":
                tokens.append(self._identifier())
                continue
            if char == "." and self.index + 1 < len(self.source) and (self.source[self.index + 1].isalpha() or self.source[self.index + 1] == "_"):
                self._advance(char)
                start = self.index
                while self.index < len(self.source) and (self.source[self.index].isalnum() or self.source[self.index] == "_"):
                    self._advance(self.source[self.index])
                tokens.append(Token("FIELD", self.source[start:self.index], start_line, start_column))
                continue
            if char == "$":
                self._advance(char)
                start = self.index
                while self.index < len(self.source) and (self.source[self.index].isalnum() or self.source[self.index] in "_:"):
                    self._advance(self.source[self.index])
                if start == self.index or not (self.source[start].isalpha() or self.source[start] == "_"):
                    raise LexerError(f"invalid binding at {start_line}:{start_column}")
                tokens.append(Token("BINDING", self.source[start:self.index], start_line, start_column))
                continue
            if char in SINGLE:
                tokens.append(Token(char, char, start_line, start_column))
                self._advance(char)
                continue
            raise LexerError(f"invalid character {char!r} at {start_line}:{start_column}")
        return tokens

    def _advance(self, text: str) -> None:
        for char in text:
            if char == "\n":
                self.line, self.column = self.line + 1, 1
            else:
                self.column += 1
        self.index += len(text)

    def _skip_comment(self) -> None:
        while self.index < len(self.source):
            char = self.source[self.index]
            self._advance(char)
            if char == "\n":
                break

    def _number(self) -> Token:
        start, line, column = self.index, self.line, self.column
        match = re.match(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", self.source[start:])
        if match is None:
            raise LexerError(f"invalid number at {line}:{column}")
        text = match.group(0)
        self._advance(text)
        return Token("LITERAL", text, line, column)

    def _identifier(self) -> Token:
        start, line, column = self.index, self.line, self.column
        while self.index < len(self.source) and (self.source[self.index].isalnum() or self.source[self.index] == "_" or self.source[self.index:self.index + 2] == "::"):
            self._advance(self.source[self.index])
        text = self.source[start:self.index]
        return Token(text.upper() if text in KEYWORDS else "IDENT", text, line, column)

    def _string_tokens(self) -> list[Token]:
        line, column = self.line, self.column
        self._advance('"')
        tokens = [Token("QQSTRING_START", '"', line, column)]
        text_start = self.index
        while self.index < len(self.source):
            char = self.source[self.index]
            if char == "#" and any(token.kind == "QQSTRING_INTERP_END" for token in tokens):
                if self.index > text_start:
                    tokens.append(Token("QQSTRING_TEXT", self.source[text_start:self.index], line, column))
                self._skip_comment()
                tokens.append(Token("QQSTRING_END", '"', self.line, self.column))
                return tokens
            if char == '"':
                if self.index > text_start:
                    tokens.append(Token("QQSTRING_TEXT", self.source[text_start:self.index], line, column))
                self._advance(char)
                tokens.append(Token("QQSTRING_END", '"', self.line, self.column - 1))
                return tokens
            if char == "\\":
                if self.index + 1 >= len(self.source):
                    raise LexerError("unterminated escape")
                escaped = self.source[self.index + 1]
                if escaped == "(":
                    if self.index > text_start:
                        tokens.append(Token("QQSTRING_TEXT", self.source[text_start:self.index], line, column))
                    start_line, start_column = self.line, self.column
                    self._advance("\\(")
                    close = self._interpolation_end()
                    inner = self.source[self.index:close]
                    tokens.append(Token("QQSTRING_INTERP_START", "\\(", start_line, start_column))
                    tokens.extend(Lexer(inner).tokenize())
                    self._advance(self.source[self.index:close])
                    tokens.append(Token("QQSTRING_INTERP_END", ")", self.line, self.column))
                    self._advance(")")
                    text_start = self.index
                    continue
                if escaped == "u":
                    digits = self.source[self.index + 2:self.index + 6]
                    if len(digits) != 4 or any(char not in "0123456789abcdefABCDEF" for char in digits):
                        raise LexerError("invalid unicode escape")
                    self._advance("\\u" + digits)
                elif escaped not in '"\\/bfnrt':
                    raise LexerError(f"invalid escape \\{escaped}")
                else:
                    self._advance("\\" + escaped)
                continue
            if char in "\r\n":
                raise LexerError("newline in string")
            self._advance(char)
        raise LexerError("unterminated string")

    def _interpolation_end(self) -> int:
        depth = 0
        index = self.index
        while index < len(self.source):
            char = self.source[index]
            if char == '"':
                index += 1
                while index < len(self.source) and self.source[index] != '"':
                    index += 2 if self.source[index] == "\\" else 1
            elif char in "([{":
                depth += 1
            elif char in ")]}":
                if char == ")" and depth == 0:
                    return index
                depth -= 1
            index += 1
        raise LexerError("unterminated interpolation")
