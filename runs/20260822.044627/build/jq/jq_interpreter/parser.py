"""Parser boundary: source tokens become an immutable intermediate form."""

import json
import re

from .ast import Array, Comma, Filter, Identity, Limit, Literal, Raise
from .errors import CompileError
from .lexer import TokenKind, tokenize


def parse(source: str) -> Filter:
    """Compile source into a filter or raise :class:`CompileError`."""
    text = source.strip()
    if not text:
        raise CompileError("empty program")
    if text == ".":
        return Identity()
    if text == "error":
        return Raise()
    if text.startswith("[") and text.endswith("]"):
        return Array(parse(text[1:-1]))
    if text.startswith("limit(") and text.endswith(")"):
        body = text[6:-1]
        separator = _top_level_separator(body, ";")
        if separator is not None:
            count_text, expression = body[:separator], body[separator + 1 :]
            if count_text.strip().isdigit():
                return Limit(int(count_text.strip()), parse(expression))
    comma = _top_level_comma(text)
    if comma is not None:
        return Comma(parse(text[:comma]), parse(text[comma + 1 :]))
    if text in {"nan", "infinite", "-infinite", "-nan"}:
        return Literal({"nan": float("nan"), "infinite": float("inf"),
                        "-infinite": float("-inf"), "-nan": float("nan")}[text])
    if re.fullmatch(r"(?:-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)|true|false|null|\"(?:[^\"\\]|\\.)*\"", text):
        try:
            return Literal(json.loads(text))
        except json.JSONDecodeError as error:
            raise CompileError(f"invalid literal: {error.msg}") from error
    raise CompileError("unsupported program in foundational parser")


def _top_level_comma(text: str) -> int | None:
    return _top_level_separator(text, ",")


def _top_level_separator(text: str, separator: str) -> int | None:
    depth = 0
    quoted = False
    escaped = False
    for position, character in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in "[{(":
            depth += 1
        elif character in "]})":
            depth -= 1
        elif character == separator and depth == 0:
            return position
    if quoted or depth != 0:
        raise CompileError("incomplete program")
    return None
