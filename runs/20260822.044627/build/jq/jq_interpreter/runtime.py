"""Runtime value and stream contracts."""

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TypeAlias

JsonValue: TypeAlias = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
ValueStream: TypeAlias = Iterator[JsonValue]


@dataclass
class EvaluationContext:
    """Per-input state for lexical bindings and runtime options."""

    bindings: dict[str, JsonValue] = field(default_factory=dict)


def identity_stream(value: JsonValue) -> ValueStream:
    """Yield one value, retaining the stream contract used by the evaluator."""
    yield value
