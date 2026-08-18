# FEATURE: Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implements jq variable bindings, destructuring patterns, and destructuring alternatives. |
| Depends On  | FEATURE-Functions.md |
| Provides    | as bindings, array/object patterns, ?// alternatives |
| Consumes    | jq parser and generator evaluator |

## Intent

Bindings are immutable lexical values scoped over the expression to their right. Array and object patterns bind nested values, using `null` for missing array elements or unmatched fields. `?//` tries alternative patterns and exposes the bindings from the successful alternative.

## Programmatic Acceptance

=== AC bindings-corpus ===
Intent: The implementation passes conformance cases covering scalar bindings, array and object destructuring, lexical scope, and ?// alternatives.
Suite: scoped

import os
import subprocess
import sys

selector = r" as \$| as \[| as \{|\\?//"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC bindings-corpus ===

=== AC bindings-alternatives ===
Intent: The selected corpus slice executes nested destructuring alternatives and exposes null for unavailable bindings.
Suite: scoped

import os
import subprocess
import sys

selector = r"\?//"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC bindings-alternatives ===

## User Acceptance

- None.

## Guardrails

- Bindings are lexically scoped and immutable.
- Alternative matching must preserve the successful branch's bindings.
- Missing pattern values resolve according to jq's null-binding semantics.
