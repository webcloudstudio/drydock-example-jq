# FEATURE: Boolean and Alternative Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define jq boolean, negation, defined-or, and defined-or assignment semantics. |
| Depends On  | FEATURE-Arithmetic-Operators.md, FEATURE-Truthiness-and-Comparison.md |
| Provides    | and, or, not, defined-or, defined-or assignment |
| Consumes    | jq truthiness, comparison, and generator evaluation |

## Intent

This capability implements jq's boolean and fallback operators with false/null truthiness, generator-aware output, and short-circuit behavior.

## Behavior

- Only `false` and `null` are falsey.
- `and` and `or` produce boolean results for each relevant generator combination.
- `not` produces the inverse truth value.
- `//` emits non-false/non-null left outputs, otherwise all right outputs.
- `//=` updates defined-or paths while preserving immutable assignment behavior.
- Boolean and alternative expressions preserve generator ordering and short-circuit errors where jq requires them.

## Programmatic Acceptance

=== AC flow-002-conformance ===
Intent: Boolean, negation, and defined-or operators follow jq truthiness and fallback semantics.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "(true and false), (true or false), (false|not), (null // 7), (3 // 7)"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [False, True, True, 7, 3]
assert actual == expected
=== END AC flow-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not use Python truthiness in place of jq truthiness.
- `//` must not be reduced to ordinary boolean `or`.
- Preserve generator multiplicity and fallback evaluation semantics.
