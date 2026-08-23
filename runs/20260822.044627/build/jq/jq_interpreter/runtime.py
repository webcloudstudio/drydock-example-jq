"""Runtime value and stream contracts."""

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TypeAlias

JsonValue: TypeAlias = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
ValueStream: TypeAlias = Iterator[JsonValue]


class InputNumber(float):
    """A JSON number retaining its source spelling until it is transformed."""

    def __new__(cls, value: str) -> "InputNumber":
        instance = super().__new__(cls, float(value))
        instance.source = value
        return instance

    source: str


@dataclass
class EvaluationContext:
    """Per-input state for lexical bindings and runtime options."""

    bindings: dict[str, JsonValue] = field(default_factory=dict)


def identity_stream(value: JsonValue) -> ValueStream:
    """Yield one value, retaining the stream contract used by the evaluator."""
    yield value
