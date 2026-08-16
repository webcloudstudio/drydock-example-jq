# FEATURE: jq Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implements jq arithmetic, Boolean, defined-or, equality, ordering, and type operations. |
| Depends On  | FEATURE-Core-Values.md |
| Provides    | arithmetic, logical, defined-or, equality, ordering, type operations |
| Consumes    | core values and generator evaluator |

## Intent

Implement jq's type-sensitive operators and comparisons, including numeric behavior, array/string/object operations, truthiness, short-circuiting, and defined-or semantics.

## Scope

- Addition, subtraction, multiplication, division, and remainder.
- Unary negation.
- Equality, inequality, and jq type ordering.
- `and`, `or`, `not`, and `//`.
- Type-sensitive errors and numeric edge cases.

## Programmatic Acceptance

=== AC operators-suite ===
Intent: Operator behavior passes its authoritative conformance slice.
Suite: scoped

import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"(==|!=|[<>]=?|\+|\-|\*|/|%|//)"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC operators-suite ===

=== AC operators-arithmetic ===
Intent: Arithmetic applies the declared operation to supplied numeric input.

import json
import subprocess

left = 7
right = 5
program = f". + {right}"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(left) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == left + right
=== END AC operators-arithmetic ===

=== AC operators-definedor ===
Intent: Defined-or selects the fallback for a null input.

import json
import subprocess

fallback = {"fallback": True}
program = f". // {json.dumps(fallback, separators=(',', ':'))}"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == fallback
=== END AC operators-definedor ===

## User Acceptance

- None.

## Guardrails

- Do not equate booleans with numbers.
- Preserve jq truthiness: only false and null are false.
- Division and remainder by zero must raise runtime errors.
