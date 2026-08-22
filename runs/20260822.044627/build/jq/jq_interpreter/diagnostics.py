"""Process diagnostics and exit-code policy."""

import sys
from typing import TextIO

from .errors import CompileError, RuntimeError

COMPILE_EXIT = 3
RUNTIME_EXIT = 5


def report_compile_error(error: CompileError, stream: TextIO = sys.stderr) -> int:
    print(f"jq: compile error: {error}", file=stream)
    return COMPILE_EXIT


def report_runtime_error(error: RuntimeError, stream: TextIO = sys.stderr) -> int:
    print(f"jq: runtime error: {error}", file=stream)
    return RUNTIME_EXIT
