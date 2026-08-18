# FEATURE: Conditionals

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implements jq conditional, boolean, defined-or, and optional execution semantics. |
| Depends On  | FEATURE-Arithmetic-Comparison.md |
| Provides    | if/then/elif/else/end, and, or, not, //, optional execution |
| Consumes    | ordered filter generators |

## Intent

Conditional filters evaluate each condition result independently. jq treats only `false` and `null` as false, while empty results produce no branch output. Boolean operators emit boolean values, and `//` selects non-null, non-false generator results.

## Programmatic Acceptance

=== AC conditionals-corpus ===
Intent: The implementation passes the conformance cases covering conditionals, boolean operators, defined-or, and optional execution.
Suite: scoped

import os
import subprocess
import sys

selector = r"if | and | or | //|not|\?"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC conditionals-corpus ===

=== AC conditional-generators ===
Intent: The selected conditional corpus slice executes generator-valued conditions and branches successfully.
Suite: scoped

import os
import subprocess
import sys

selector = r"if .*then|//| and | or "
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC conditional-generators ===

## User Acceptance

- None.

## Guardrails

- Preserve jq truthiness: only `false` and `null` are false.
- Preserve generator ordering and multiplicity across all branches.
