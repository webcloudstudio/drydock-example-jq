"""JSON value and compact serialization boundary for the jq runtime."""

from __future__ import annotations

import json
from typing import Any

JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


def parse_json(text: str) -> JsonValue:
    return json.loads(text)


def encode_compact(value: JsonValue) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
