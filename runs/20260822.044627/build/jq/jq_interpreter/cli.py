"""Executable boundary for ``jq -c '<program>'``."""

import argparse
import json
import math
import sys
from collections.abc import Iterator

from .diagnostics import report_compile_error, report_runtime_error
from .errors import CompileError, RuntimeError
from .interpreter import Interpreter, parse_inputs


def _inputs() -> Iterator[object]:
    yield from parse_inputs(sys.stdin.read())


def _json_output(value: object) -> object:
    """Convert jq's non-finite numbers to its JSON output representation.

    jq represents NaN and infinities as ``null`` when emitting JSON.  Doing this
    recursively also covers values nested in arrays and objects.
    """
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, list):
        return [_json_output(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_output(item) for key, item in value.items()}
    return value


def main(argv: list[str] | None = None) -> int:
    arguments = argparse.ArgumentParser(prog="jq")
    arguments.add_argument("-c", action="store_true")
    arguments.add_argument("program")
    options = arguments.parse_args(argv)
    try:
        interpreter = Interpreter(options.program)
    except CompileError as error:
        return report_compile_error(error)
    try:
        for output in interpreter.run(_inputs()):
            print(
                json.dumps(_json_output(output), separators=(",", ":"), ensure_ascii=False),
                flush=True,
            )
    except (RuntimeError, ValueError, TypeError, json.JSONDecodeError) as error:
        return report_runtime_error(RuntimeError(str(error)))
    return 0
