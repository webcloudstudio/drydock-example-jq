# FEATURE: Boolean and Alternative Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq Boolean operators, truthiness-aware alternatives, and defined-or assignment. |
| Depends On  | FEATURE-Truthiness-And-Comparison.md, FEATURE-Arithmetic-And-Structural-Operators.md |
| Provides    | and, or, not, //, //= |
| Consumes    | jq truthiness, generator core, arithmetic operators |

## Intent

Implement strict Boolean operators and jq's value-selection alternative operators. Boolean operators produce Boolean values, while `//` selects non-null and non-false generator outputs.

## Behavior

- Only `false` and `null` are falsey.
- `and`, `or`, and `not` produce Boolean results with generator-valued operands evaluated according to jq semantics.
- `a // b` emits all non-false, non-null values from `a`; otherwise it evaluates `b`.
- `//=` updates defined-or paths using jq assignment semantics.
- Short-circuiting must prevent unnecessary error-producing branches where jq requires it.

## Programmatic Acceptance

=== AC flow-002-conformance ===
Intent: The Boolean and alternative operator implementation passes representative declared Boolean and fallback behaviors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess

jq = os.path.join(os.getcwd(), "jq")

boolean = subprocess.run(
    [jq, "-c", "true and (1 == 1)"],
    capture_output=True,
    text=True,
)
assert boolean.returncode == 0
assert json.loads(boolean.stdout) is True

alternative = subprocess.run(
    [jq, "-c", "null // 7"],
    capture_output=True,
    text=True,
)
assert alternative.returncode == 0
assert json.loads(alternative.stdout) == 7

=== END AC flow-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not treat empty strings, arrays, or objects as falsey.
- Preserve generator multiplicity and alternative fallback semantics.
- Do not evaluate fallback branches when jq semantics select the left stream.
