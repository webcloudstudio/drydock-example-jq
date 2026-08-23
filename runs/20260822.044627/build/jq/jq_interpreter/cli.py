"""Executable boundary for ``jq -c '<program>'``."""

import argparse
import json
import math
import sys
from collections.abc import Iterator

from .diagnostics import report_compile_error, report_runtime_error
from .errors import CompileError, FLOW_RUNTIME_ERRORS, HaltError, RuntimeError
from .interpreter import Interpreter, parse_input_records

# The conformance corpus deliberately exercises jq's deep-value limit with
# values around ten thousand levels deep.  Python's default limit is lower
# than that and would turn valid jq processing into an uncaught RecursionError
# while encoding an intermediate value.
sys.setrecursionlimit(100000)


def _inputs() -> Iterator[object]:
    yield from parse_input_records(sys.stdin.read())


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
        for output in interpreter.run_records(_inputs()):
            from .evaluator import _deep_json_dumps
            print(_deep_json_dumps(output), flush=True)
    except HaltError as error:
        from .evaluator import _raw_diagnostic
        sys.stderr.write(_raw_diagnostic(error.value))
        sys.stderr.flush()
        return error.exit_code
    except FLOW_RUNTIME_ERRORS + (json.JSONDecodeError,) as error:
        return report_runtime_error(RuntimeError(str(error)))
    return 0
