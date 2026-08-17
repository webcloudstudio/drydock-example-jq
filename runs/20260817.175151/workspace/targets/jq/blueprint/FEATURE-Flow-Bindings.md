# FEATURE: Flow Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides lexical variable bindings and destructuring alternatives for jq programs. |
| Depends On  | FEATURE-Core-Construction.md |
| Provides    | lexical bindings, array patterns, object patterns, destructuring alternatives |
| Consumes    | generator evaluator |

## Purpose

Implement jq's lexical `as` bindings, array and object destructuring, lexical scope, and `?//` destructuring alternatives. Bindings are immutable, scoped to the expression on their right, and must preserve generator multiplicity and backtracking.

## Programmatic Acceptance

=== AC flow-bindings-suite ===
Intent: The implementation passes the conformance cases for lexical bindings and destructuring.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\bas\s+\$|destructur|\\?//"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-bindings-suite ===

=== AC flow-binding-scope ===
Intent: The implementation passes conformance cases exercising variable scope and repeated bindings.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\$[A-Za-z_][A-Za-z_0-9]*"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-binding-scope ===

## User Acceptance

- None.

## Guardrails

- Bindings must not leak outside their lexical scope.
- Destructuring alternatives must preserve generator ordering and runtime backtracking.
- Undefined bindings must remain compile-time errors.
