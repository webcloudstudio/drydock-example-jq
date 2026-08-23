"""Application-facing interpreter orchestration."""

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from .evaluator import evaluate
from .parser import parse
from .runtime import InputNumber, JsonValue


class _InputInteger(int):
    """An input integer whose literal spelling remains available to jq."""


@dataclass(frozen=True)
class InputRecord:
    value: JsonValue
    filename: str = '<stdin>'
    line_number: int = 1


class Interpreter:
    """Compile once, then evaluate each JSON input in order."""

    def __init__(self, program: str) -> None:
        self._compiled = parse(program)

    def run(self, inputs: Iterable[JsonValue]) -> Iterator[JsonValue]:
        """Yield every output, preserving input and generator ordering."""
        from .evaluator import EvaluationContext
        stream = iter(InputRecord(value, line_number=index)
                      for index, value in enumerate(inputs, start=1))
        context = EvaluationContext(stream)
        for record in stream:
            context.current = record
            yield from evaluate(self._compiled, record.value, context)

    def run_records(self, records: Iterable[InputRecord]) -> Iterator[JsonValue]:
        """Evaluate records while retaining their source metadata."""
        from .evaluator import EvaluationContext
        stream = iter(records)
        context = EvaluationContext(stream)
        for record in stream:
            context.current = record
            yield from evaluate(self._compiled, record.value, context)


def parse_input(line: str) -> JsonValue:
    """Decode one JSON input value."""
    return json.loads(line.lstrip("\ufeff"), parse_constant=_parse_json_constant)


def parse_inputs(text: str) -> Iterator[JsonValue]:
    """Decode every whitespace-separated JSON value in an input stream.

    ``jq`` accepts JSON values separated by arbitrary whitespace, so a value may
    span multiple physical lines.  ``raw_decode`` preserves the boundary
    between successive values without requiring a non-standard JSON parser.
    """
    yield from (record.value for record in parse_input_records(text))


def parse_input_records(text: str) -> Iterator[InputRecord]:
    """Decode values and retain the line on which each value starts."""
    import re
    text = re.sub(r'(?<![A-Za-z_])-(?:nan|infinite|NaN|Infinity)(?![A-Za-z_])', lambda m: '-NaN' if 'nan' in m.group(0).lower() else '-Infinity', text)
    text = re.sub(r'(?<![A-Za-z_])(?:nan|infinite|NaN|Infinity)(?![A-Za-z_])', lambda m: 'NaN' if m.group(0).lower() == 'nan' else 'Infinity', text)
    text = re.sub(r'(?<![A-Za-z_])-NaN(?![A-Za-z_])', 'NaN', text)
    def parse_integer(text: str) -> int | float:
        integer = int(text)
        return InputNumber(text) if abs(integer) > 2**53 else _InputInteger(integer)

    decoder = json.JSONDecoder(parse_constant=_parse_json_constant,
                               parse_int=parse_integer, parse_float=InputNumber)
    position = 0
    while True:
        while position < len(text) and text[position].isspace():
            position += 1
        if position >= len(text):
            return
        if position == 0 and text.startswith("\ufeff"):
            position += 1
            continue
        start = position
        value, position = decoder.raw_decode(text, position)
        yield InputRecord(value, line_number=text.count('\n', 0, start) + 1)


def _parse_json_constant(value: str) -> float:
    """Decode jq's accepted non-standard numeric constants."""
    return {"NaN": float("nan"), "nan": float("nan"),
            "Infinity": float("inf"), "infinite": float("inf"),
            "-Infinity": float("-inf"), "-infinite": float("-inf"),
            "-NaN": float("nan"), "-nan": float("nan")} [value]
