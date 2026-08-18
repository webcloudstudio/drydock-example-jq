# FEATURE: Reducers

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implements jq reducers, ranges, iterator helpers, recursion, and aggregate generators. |
| Depends On  | FEATURE-Bindings.md |
| Provides    | reduce, foreach, range, limit, skip, first, last, nth, while, until, repeat, recurse, any, all |
| Consumes    | user-defined functions and bindings |

## Intent

Reducer expressions update accumulator state for every generator result. Iteration helpers preserve ordering, limits, skips, short-circuit behavior, and empty-stream semantics. Recursive generators emit the current value before descendants where jq specifies preorder traversal.

## Programmatic Acceptance

=== AC reducers-corpus ===
Intent: The implementation passes conformance cases covering reduce, foreach, range, limits, skips, nth, and aggregate generators.
Suite: scoped

import os
import subprocess
import sys

selector = r"reduce|foreach|range|limit|skip|nth|first|last|any|all"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC reducers-corpus ===

=== AC reducers-recursion ===
Intent: The implementation passes conformance cases covering while, until, repeat, recurse, and recursive traversal.
Suite: scoped

import os
import subprocess
import sys

selector = r"while|until|repeat|recurse|\.\."
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC reducers-recursion ===

## User Acceptance

- None.

## Guardrails

- Reducers preserve accumulator order and generator multiplicity.
- Short-circuiting helpers must not evaluate unnecessary generator outputs.
- Recursive generators must preserve jq's specified traversal order.
