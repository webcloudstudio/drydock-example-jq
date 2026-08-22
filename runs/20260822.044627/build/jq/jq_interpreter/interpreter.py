"""Application-facing interpreter orchestration."""

import json
from collections.abc import Iterable, Iterator

from .evaluator import evaluate
from .parser import parse
from .runtime import JsonValue


class Interpreter:
    """Compile once, then evaluate each JSON input in order."""

    def __init__(self, program: str) -> None:
        self._compiled = parse(program)

    def run(self, inputs: Iterable[JsonValue]) -> Iterator[JsonValue]:
        """Yield every output, preserving input and generator ordering."""
        for value in inputs:
            yield from evaluate(self._compiled, value)


def parse_input(line: str) -> JsonValue:
    """Decode one JSON input record."""
    return json.loads(line.lstrip("\ufeff"), parse_constant=_parse_json_constant)


def _parse_json_constant(value: str) -> float:
    """Decode jq's accepted non-standard numeric constants."""
    return {"NaN": float("nan"), "Infinity": float("inf"),
            "-Infinity": float("-inf")}[value]
