# FEATURE: Arithmetic and Type-Dependent Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implement jq arithmetic, merge, repetition, division, modulo, and negation semantics. |
| Depends On  | FEATURE-Values-Model.md, FEATURE-Eval-Cartesian.md |
| Provides    | arithmetic, merge, string, and array operators |
| Consumes    | JSON value model, ordered generator evaluator |

## Intent

Arithmetic operators evaluate both operands as jq filters over the same input and preserve generator ordering. Operators dispatch by jq value type: numeric arithmetic, array concatenation/subtraction, string concatenation/repetition/splitting, shallow object addition, recursive object multiplication, and null identity behavior.

Invalid type combinations and division or remainder by zero raise runtime errors without losing values already emitted.

## Behaviors

- `+`, `-`, `*`, `/`, `%`, and unary `-` follow jq's type-dependent rules.
- Object multiplication recursively merges nested objects.
- String multiplication and division implement repetition and splitting.
- Array subtraction removes matching elements.
- Numeric overflow, NaN, infinity, and negative zero follow the selected jq-compatible representation.
- Runtime diagnostics are emitted through the evaluator's structured error channel.

## Programmatic Acceptance

=== AC arithmetic-operators ===
Intent: The implementation passes the authoritative arithmetic and numeric operator corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^[^#].*(\+|\-|\*|/|%|negat|arithmetic|modulo)"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC arithmetic-operators ===

=== AC arithmetic-types ===
Intent: The implementation passes the authoritative type-dependent string, array, and object operator corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "recursive object merge|string repetition|string splitting|array subtraction|type-dependent"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC arithmetic-types ===

=== AC arithmetic-errors ===
Intent: The implementation passes the authoritative arithmetic runtime-error corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "divided because|cannot be added|cannot be subtracted|Repeat string result too long"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC arithmetic-errors ===

## User Acceptance

- None.

## Guardrails

- Do not perform implicit type conversions.
- Do not shell out for arithmetic or delegate semantics to another jq implementation.
- Preserve outputs emitted before a later arithmetic error.
