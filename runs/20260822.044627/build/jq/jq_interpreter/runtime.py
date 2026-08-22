"""Runtime value and stream contracts."""

from collections.abc import Iterator
from typing import TypeAlias

JsonValue: TypeAlias = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
ValueStream: TypeAlias = Iterator[JsonValue]


def identity_stream(value: JsonValue) -> ValueStream:
    """Yield one value, retaining the stream contract used by the evaluator."""
    yield value
