# FEATURE: Arithmetic Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define jq arithmetic, structural combination, repetition, splitting, and negation operators. |
| Depends On  | FEATURE-Type-and-Numeric-Builtins.md |
| Provides    | plus, minus, multiply, divide, modulo, negation, recursive object merge, string repetition and splitting |
| Consumes    | type and numeric builtins, jq generator evaluation |

## Intent

Arithmetic operators apply jq's type-directed operations while preserving generator Cartesian products, immutable values, and runtime error behavior.

## Behavior

- Numeric operators perform arithmetic with jq-compatible numeric handling.
- `+` combines numbers, arrays, strings, objects, and null as specified.
- `-` subtracts numbers or removes matching array elements.
- `*` supports numeric multiplication, string repetition, and recursive object merge.
- `/` supports numeric division and string splitting.
- `%` performs numeric remainder.
- Unary negation applies only to numbers.
- Division, remainder, invalid combinations, and excessive string repetition raise runtime errors with exit status 5 when uncaught.

## Programmatic Acceptance

=== AC flow-001-conformance ===
Intent: Numeric and structural arithmetic operators produce jq-compatible results.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "1+2, 7-3, 4*5, 7/2, 7%4, -6, [1,2]+[3], \"ab\"*2, \"a,b\"/\",\""],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [3, 4, 20, 3.5, 3, -6, [1, 2, 3], "abab", ["a", "b"]]
assert actual == expected
=== END AC flow-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Operators must preserve output order and multiplicity.
- Values remain immutable; assignment semantics are outside this capability.
- Do not implement structural operations through implicit Python type coercion.
