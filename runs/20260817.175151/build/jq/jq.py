"""Importable implementation module for the root ``jq`` executable."""

from pathlib import Path
import sys


_ROOT = Path(__file__).parent
_EXECUTABLE = _ROOT / "jq"

# The executable is the authoritative runtime. Loading it this way keeps the
# test interface dependency-free while allowing the user-facing file to retain
# its conventional name.
_namespace: dict[str, object] = {"__name__": "jq_runtime", "__file__": str(_EXECUTABLE)}
exec(compile(_EXECUTABLE.read_text(encoding="utf-8"), str(_EXECUTABLE), "exec"), _namespace)

run = _namespace["run"]
