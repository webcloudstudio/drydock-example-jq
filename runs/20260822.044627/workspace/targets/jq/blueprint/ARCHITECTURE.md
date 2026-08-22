# ARCHITECTURE: jq

The standalone `jq` executable is implemented in Python using only the standard library. It parses jq filters, evaluates ordered generators over JSON input, and emits compact JSON values.

## Programmatic Acceptance

=== AC architecture-boundary ===
from pathlib import Path
import ast
entry = Path("jq")
assert entry.is_file()
assert entry.stat().st_mode & 0o111
assert ast.parse(entry.read_text(encoding="utf-8"))
=== END AC architecture-boundary ===
