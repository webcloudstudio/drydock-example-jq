"""Executable boundary: arguments, JSON lines, output, and exit status."""

import argparse
import json
import sys
from collections.abc import Iterable
from typing import Any, TextIO

from .errors import COMPILE_ERROR, RUNTIME_ERROR, CompileError, RuntimeErrorJq
from .evaluator import evaluate
from .parser import parse


def _read_inputs(stream: TextIO) -> Iterable[Any]:
    for line in stream:
        if line.strip():
            try:
                yield json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeErrorJq("invalid JSON input") from error


def run(arguments: list[str], stdin: TextIO, stdout: TextIO, stderr: TextIO) -> int:
    """Run one CLI invocation and return the documented process status."""

    parser = argparse.ArgumentParser(prog="jq", add_help=False)
    parser.add_argument("-c", action="store_true")
    parser.add_argument("program", nargs="?")
    options = parser.parse_args(arguments)
    if not options.c or options.program is None:
        stderr.write("usage: jq -c PROGRAM\n")
        return COMPILE_ERROR
    try:
        program = parse(options.program)
    except CompileError as error:
        stderr.write(f"compile error: {error}\n")
        return COMPILE_ERROR
    try:
        for input_value in _read_inputs(stdin):
            for output_value in evaluate(program, input_value):
                stdout.write(json.dumps(output_value, separators=(",", ":")) + "\n")
    except RuntimeErrorJq as error:
        stderr.write(f"runtime error: {error}\n")
        return RUNTIME_ERROR
    return 0


def main() -> None:
    raise SystemExit(run(sys.argv[1:], sys.stdin, sys.stdout, sys.stderr))
