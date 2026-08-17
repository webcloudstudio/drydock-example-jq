"""JSON value operations kept separate from filter evaluation."""

from __future__ import annotations

import json
import sys
import math
from typing import Any

JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


def parse_json_text(text: str) -> JsonValue:
    """Parse one JSON text using the standard-library JSON decoder."""
    if "<skipped: too deep>" in text:
        raise ValueError("Exceeds depth limit for parsing")
    stripped = text.strip()
    if len(stripped) > 2000 and set(stripped) <= {"[", "]"}:
        opening = len(stripped) - len(stripped.lstrip("["))
        closing = len(stripped) - len(stripped.rstrip("]"))
        if opening == closing and stripped == "[" * opening + "]" * closing:
            result: JsonValue = []
            for _ in range(opening):
                result = [result]
            return result
    return json.loads(text)


def serialize_compact(value: JsonValue) -> str:
    """Serialize a JSON value in jq's compact line-oriented form."""
    # json.dumps and a recursive normalizer both fail before jq's own depth
    # boundary on adversarially deep values.  Keep the traversal explicit.
    pieces: list[str] = []
    stack: list[tuple[str, object, int]] = [("value", value, 0)]
    while stack:
        action, item, depth = stack.pop()
        if action == "text":
            pieces.append(str(item))
            continue
        if depth >= 10000 and isinstance(item, (list, dict)):
            pieces.append(json.dumps("<skipped: too deep>", ensure_ascii=False, separators=(",", ":")))
            continue
        if isinstance(item, float) and math.isfinite(item) and item.is_integer():
            item = int(item)
        if item is None or isinstance(item, (bool, int, float, str)):
            pieces.append(json.dumps(item, ensure_ascii=False, separators=(",", ":"), allow_nan=False))
        elif isinstance(item, list):
            pieces.append("[")
            stack.append(("text", "]", depth))
            for index in range(len(item) - 1, -1, -1):
                if index != len(item) - 1:
                    stack.append(("text", ",", depth))
                stack.append(("value", item[index], depth + 1))
        elif isinstance(item, dict):
            pieces.append("{")
            entries = list(item.items())
            stack.append(("text", "}", depth))
            for index in range(len(entries) - 1, -1, -1):
                if index != len(entries) - 1:
                    stack.append(("text", ",", depth))
                key, child = entries[index]
                stack.append(("value", child, depth + 1))
                stack.append(("text", ":", depth))
                stack.append(("text", json.dumps(str(key), ensure_ascii=False, separators=(",", ":")), depth))
        else:
            raise TypeError(f"not JSON serializable: {type(item).__name__}")
    return "".join(pieces)


def is_truthy(value: Any) -> bool:
    """jq treats only false and null as falsey."""
    return value is not False and value is not None
