"""Process boundary for the standalone jq executable."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from jq_parser import ParseError, parse
from jq_runtime import RuntimeFailure, evaluate


def _arguments(arguments: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="jq")
    parser.add_argument("-c", dest="program", required=True)
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> int:
    """Run jq's compact stdin/stdout protocol and return its process status."""
    try:
        options = _arguments(sys.argv[1:] if arguments is None else arguments)
        program = parse(options.program)
    except (ParseError, ValueError, SystemExit) as error:
        if isinstance(error, SystemExit):
            return int(error.code or 0)
        print(f"jq: compile error: {error}", file=sys.stderr)
        return 3

    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            value: Any = json.loads(line)
            for result in evaluate(program, value):
                print(json.dumps(result, separators=(",", ":"), ensure_ascii=False))
    except (json.JSONDecodeError, RuntimeFailure, TypeError, ValueError) as error:
        print(f"jq: runtime error: {error}", file=sys.stderr)
        return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
