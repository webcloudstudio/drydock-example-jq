"""Lexer for jq source text.

The lexer deliberately retains source positions and leaves filter interpolation
as source fragments for the parser.  This keeps lexical validation (especially
JSON escapes and delimiter matching) separate from expression semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import re

from .diagnostics import CompileError


@dataclass(frozen=True)
class Token:
    kind: str
    value: object
    position: int
    line: int = 1
    column: int = 1


_WORDS = {"as", "import", "include", "module", "def", "if", "then", "else",
          "elif", "and", "or", "end", "reduce", "foreach", "try", "catch",
          "label", "break", "true", "false", "null", "empty", "error"}
_OPERATORS = ("//=", "?//", "|=", "+=", "-=", "*=", "/=", "%=", "==", "!=",
              "<=", ">=", "..", "//")
_SINGLE = set(".?=;,,:|+-*/%<>()[]{}@$!")
_IDENT = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_NUMBER = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def _loc(source: str, offset: int) -> tuple[int, int]:
    line = source.count("\n", 0, offset) + 1
    last = source.rfind("\n", 0, offset)
    return line, offset - last


def _token(kind: str, value: object, source: str, position: int) -> Token:
    line, column = _loc(source, position)
    return Token(kind, value, position, line, column)


def _quoted(source: str, start: int) -> tuple[object, int]:
    """Read a jq quoted string, returning a plain string or template parts."""
    i = start + 1
    plain: list[str] = []
    parts: list[tuple[str, str]] = []
    while i < len(source):
        if source[i] == '"':
            if parts:
                if plain:
                    parts.append(("text", "".join(plain)))
                return parts, i + 1
            return "".join(plain), i + 1
        if source[i] == "\\" and i + 1 < len(source) and source[i + 1] == "(":
            if plain:
                parts.append(("text", "".join(plain)))
                plain = []
            depth, j = 1, i + 2
            quote = False
            while j < len(source) and depth:
                c = source[j]
                if c == "\\":
                    j += 2
                    continue
                if c == '"':
                    quote = not quote
                elif not quote and c == "(":
                    depth += 1
                elif not quote and c == ")":
                    depth -= 1
                j += 1
            if depth:
                raise CompileError(f"unterminated interpolation at position {i}")
            parts.append(("expr", source[i + 2:j - 1]))
            i = j
            continue
        if source[i] == "\\":
            if i + 1 >= len(source):
                raise CompileError(f"invalid escape at position {i}")
            if source[i + 1] == "u":
                raw = source[i:i + 6]
                if len(raw) != 6 or not re.fullmatch(r"\\u[0-9a-fA-F]{4}", raw):
                    raise CompileError(f"invalid escape at position {i}")
                end = i + 6
            else:
                end = i + 2
                if source[i + 1] not in '"\\/bfnrt':
                    raise CompileError(f"invalid escape at position {i}")
            try:
                plain.append(json.loads('"' + source[i:end] + '"'))
            except json.JSONDecodeError as exc:
                raise CompileError(f"invalid escape at position {i}") from exc
            i = end
            continue
        plain.append(source[i])
        i += 1
    raise CompileError(f"unterminated string at position {start}")


def tokenize(program: str) -> list[Token]:
    tokens: list[Token] = []
    stack: list[str] = []
    i = 0
    while i < len(program):
        c = program[i]
        if c.isspace():
            i += 1
            continue
        if c == '#':
            i += 1
            while i < len(program):
                if program[i] == "\\" and i + 1 < len(program) and program[i + 1] in "\r\n":
                    i += 2
                elif program[i] in "\r\n":
                    break
                else:
                    i += 1
            continue
        if c == '"':
            start = i
            value, i = _quoted(program, i)
            tokens.append(_token("STRING", value, program, start))
            continue
        match = _NUMBER.match(program, i)
        if match:
            raw = match.group(0)
            # jq accepts the shorthand `.5`; JSON's decoder requires `0.5`.
            tokens.append(_token("NUMBER", json.loads("0" + raw if raw.startswith(".") else raw), program, i))
            i = match.end()
            continue
        if c == '@':
            match = re.match(r"@[A-Za-z0-9_]+", program[i:])
            if not match:
                raise CompileError(f"invalid format at position {i}")
            raw = match.group(0)
            tokens.append(_token("FORMAT", raw[1:], program, i)); i += len(raw); continue
        if c == '$':
            match = re.match(r"\$([A-Za-z_][A-Za-z_0-9]*(?:::[A-Za-z_][A-Za-z_0-9]*)*)", program[i:])
            if not match:
                raise CompileError(f"invalid binding at position {i}")
            raw = match.group(1)
            tokens.append(_token("BINDING", raw, program, i)); i += len(match.group(0)); continue
        if c == '.' and i + 1 < len(program) and (program[i + 1].isalpha() or program[i + 1] == '_'):
            match = _IDENT.match(program, i + 1); assert match
            tokens.append(_token("FIELD", match.group(0), program, i)); i = match.end(); continue
        match = _IDENT.match(program, i)
        if match:
            raw = match.group(0); tokens.append(_token("IDENT", raw, program, i)); i = match.end(); continue
        op = next((x for x in _OPERATORS if program.startswith(x, i)), None)
        if op:
            tokens.append(_token(op, op, program, i)); i += len(op); continue
        if c in _SINGLE:
            if c in "([{": stack.append({"(": ")", "[": "]", "{": "}"}[c])
            elif c in ")]}":
                if not stack or stack.pop() != c: raise CompileError(f"mismatched delimiter at position {i}")
            tokens.append(_token(c, c, program, i)); i += 1; continue
        raise CompileError(f"invalid character at position {i}")
    if stack:
        raise CompileError("unterminated delimiter")
    tokens.append(_token("EOF", None, program, len(program)))
    return tokens
