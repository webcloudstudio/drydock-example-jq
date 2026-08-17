"""Process boundary for the compact jq executable contract."""

from __future__ import annotations

import argparse
import sys

from .data_model import parse_json_text, serialize_compact
from .diagnostics import CompileError, RuntimeJqError
from .evaluator import evaluate
from .parser import parse


def _arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="jq")
    parser.add_argument("-c", dest="program", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _arguments(sys.argv[1:] if argv is None else argv)
        filter_ast = parse(arguments.program)
    except (CompileError, SystemExit) as exc:
        if isinstance(exc, SystemExit):
            return int(exc.code)
        print(str(exc), file=sys.stderr)
        return 3

    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            input_value = parse_json_text(line)
            for output in evaluate(filter_ast, input_value):
                print(serialize_compact(output), flush=True)
    except (RuntimeJqError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 5
    return 0
