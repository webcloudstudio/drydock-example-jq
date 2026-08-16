"""Command-line boundary and jq-compatible compile/runtime exit mapping."""

from __future__ import annotations

import sys

from jq_evaluator import RuntimeErrorJq, evaluate
from jq_parser import ParseError, parse
from jq_values import encode_compact, parse_json


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "-c":
        print("usage: jq -c PROGRAM", file=sys.stderr)
        return 3
    try:
        program = parse(argv[1])
    except (ParseError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 3
    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            value = parse_json(line)
            for result in evaluate(program, value):
                print(encode_compact(result))
    except (RuntimeErrorJq, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
