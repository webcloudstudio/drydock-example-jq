"""Process boundary for the compact jq executable contract."""

from __future__ import annotations

import argparse
import sys
sys.setrecursionlimit(1000000)

from .data_model import parse_json_text, serialize_compact
from .diagnostics import CompileError
from .evaluator import evaluate
from .parser import parse


def _report(error: BaseException, fallback: str) -> None:
    """Write a useful diagnostic without ever contaminating stdout."""
    message = str(error).strip() or fallback
    print(message, file=sys.stderr)


def _arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="jq")
    parser.add_argument("-c", dest="program", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _arguments(sys.argv[1:] if argv is None else argv)
        filter_ast = parse(arguments.program)
    except CompileError as exc:
        _report(exc, "filter compilation failed")
        return 3

    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            input_value = parse_json_text(line)
            for output in evaluate(filter_ast, input_value):
                print(serialize_compact(output), flush=True)
    except Exception as exc:
        _report(exc, "runtime evaluation failed")
        return 5
    return 0
