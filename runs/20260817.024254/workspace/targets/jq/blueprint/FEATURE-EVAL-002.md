# FEATURE: Operators and Conditional Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | jq arithmetic, comparison, Boolean, alternative, conditional, optional, and error-handling operators follow jq semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-001.md, FEATURE-FRONTEND-002.md |
| Provides    | arithmetic, comparison, Boolean operators, alternative, conditionals, try/catch |
| Consumes    | generator evaluator, jq AST |

## Intent

This capability evaluates jq's operators and control expressions over generator streams. It distinguishes jq truthiness from host-language truthiness, propagates runtime errors with partial output, and supports recovery through `try`, `catch`, and optional filters.

## Behavior

- Arithmetic dispatches by jq value type and rejects unsupported combinations.
- Comparisons use jq's total value ordering and strict equality semantics.
- `and`, `or`, and `not` use only `false` and `null` as false values.
- `//` selects non-null, non-false outputs and evaluates its fallback when needed.
- Conditionals evaluate the appropriate branch for each condition output.
- `try`, `catch`, and `?` suppress or transform runtime errors while preserving stream behavior.
- Division and remainder by zero are runtime errors.

## Programmatic Acceptance

=== AC eval-002-operators ===
Intent: The implementation passes the authoritative corpus cases for arithmetic, comparison, equality, ordering, and type-dispatched operations.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"Builtin functions|Basic numbers tests|numeric comparison|equality|containment operator|division|remainder"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-002-operators ===

=== AC eval-002-conditionals ===
Intent: The implementation passes the authoritative corpus cases for jq truthiness, Boolean operators, conditionals, and defined-or.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"Conditionals|if-then-else|Alternative operator|short-circuiting| and | or |not"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-002-conditionals ===

=== AC eval-002-errors ===
Intent: The implementation passes the authoritative corpus cases for runtime errors, try/catch, and optional filters.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"Try/catch|try-catch|Error Suppression|optional operator|division by zero|runtime error"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-002-errors ===

## User Acceptance

- None.

## Guardrails

- Do not use Python truthiness in place of jq truthiness.
- Do not convert runtime failures into compile failures.
- Preserve outputs produced before an uncaught runtime error.
