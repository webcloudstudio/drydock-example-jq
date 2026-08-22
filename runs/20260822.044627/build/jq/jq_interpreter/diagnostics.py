"""Process diagnostics and exit-code policy."""

import sys
from typing import TextIO

from .errors import CompileError, RuntimeError
from .architecture import COMPILE_EXIT, RUNTIME_EXIT


def report_compile_error(error: CompileError, stream: TextIO = sys.stderr) -> int:
    print(f"jq: compile error: {error}", file=stream)
    return COMPILE_EXIT


def report_runtime_error(error: RuntimeError, stream: TextIO = sys.stderr) -> int:
    print(f"jq: runtime error: {error}", file=stream)
    return RUNTIME_EXIT
