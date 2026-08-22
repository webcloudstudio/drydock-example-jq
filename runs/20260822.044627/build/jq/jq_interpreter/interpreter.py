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
    """Decode one JSON input value."""
    return json.loads(line.lstrip("\ufeff"), parse_constant=_parse_json_constant)


def parse_inputs(text: str) -> Iterator[JsonValue]:
    """Decode every whitespace-separated JSON value in an input stream.

    ``jq`` accepts JSON values separated by arbitrary whitespace, so a value may
    span multiple physical lines.  ``raw_decode`` preserves the boundary
    between successive values without requiring a non-standard JSON parser.
    """
    decoder = json.JSONDecoder(parse_constant=_parse_json_constant)
    position = 0
    while True:
        while position < len(text) and text[position].isspace():
            position += 1
        if position >= len(text):
            return
        if position == 0 and text.startswith("\ufeff"):
            position += 1
            continue
        value, position = decoder.raw_decode(text, position)
        yield value


def _parse_json_constant(value: str) -> float:
    """Decode jq's accepted non-standard numeric constants."""
    return {"NaN": float("nan"), "Infinity": float("inf"),
            "-Infinity": float("-inf")}[value]
