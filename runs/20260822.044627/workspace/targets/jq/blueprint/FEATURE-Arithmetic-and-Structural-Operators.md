# FEATURE: Arithmetic and Structural Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq arithmetic, structural combination, repetition, splitting, and negation operators. |
| Depends On  | FEATURE-Type-And-Numeric-Primitives.md, FEATURE-Composition-And-Cartesian-Evaluation.md, FEATURE-Errors-And-Optional-Evaluation.md |
| Provides    | +, -, *, /, %, unary negation, recursive object merge, string repetition and splitting |
| Consumes    | jq value model, generator evaluation, comparison semantics |

## Intent

Implement jq's typed arithmetic and structural operators. Operators evaluate both operands as filters over the same input and preserve Cartesian generator behavior.

## Behavior

- Numbers use jq-compatible arithmetic.
- Arrays concatenate with `+` and subtract matching elements with `-`.
- Strings concatenate with `+`, repeat with numeric `*`, and split with `/`.
- Objects merge with `+`; `*` recursively merges nested objects.
- `null` is additive with any value.
- Division and remainder by zero raise runtime errors.
- Unary negation accepts numbers only and preserves partial output semantics.

## Programmatic Acceptance

=== AC flow-001-conformance ===
Intent: The arithmetic and structural operator implementation passes representative declared arithmetic and structural behaviors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess

jq = os.path.join(os.getcwd(), "jq")

addition = subprocess.run(
    [jq, "-c", "1 + 2"],
    capture_output=True,
    text=True,
)
assert addition.returncode == 0
assert json.loads(addition.stdout) == 3

merge = subprocess.run(
    [jq, "-c", '{"a":{"x":1}} * {"a":{"y":2}}'],
    capture_output=True,
    text=True,
)
assert merge.returncode == 0
assert json.loads(merge.stdout) == {"a": {"x": 1, "y": 2}}

=== END AC flow-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not perform implicit cross-type conversions.
- Preserve operator precedence, generator multiplicity, and runtime errors.
- Do not shell out to another jq implementation.
