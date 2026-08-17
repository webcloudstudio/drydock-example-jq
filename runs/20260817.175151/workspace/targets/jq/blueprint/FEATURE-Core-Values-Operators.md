# FEATURE: Core Values and Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Implement jq value semantics, arithmetic, comparisons, logical operators, truthiness, and defined-or. |
| Depends On  | FEATURE-Core-Generators.md |
| Provides    | jq value semantics, arithmetic, comparison, logical operators, defined-or |
| Consumes    | generator evaluator |

## Intent

Implement jq's JSON-compatible values and operators. Values retain their jq type; arithmetic and comparisons follow jq semantics; only false and null are falsey; `and` and `or` return booleans; `//` selects non-null, non-false generator results.

## Behavioral Contract

- Numbers, strings, arrays, objects, booleans, and null retain distinct types.
- Addition supports numeric addition, string concatenation, array concatenation, object merge, and null identity.
- Comparisons are structural and type-aware.
- Division and remainder by zero raise runtime errors.
- Logical operators use jq truthiness.
- Defined-or falls back when all left results are false or null.

## Programmatic Acceptance

=== AC operators-addition ===
Intent: Numeric addition produces the arithmetic sum.

import json
import os
import subprocess

program = ". + 2"
input_value = 3
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == input_value + 2
=== END AC operators-addition ===

=== AC operators-type-distinction ===
Intent: Equality does not equate booleans with numbers.

import json
import os
import subprocess

program = "true == 1"
payload = "null\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) is False
=== END AC operators-type-distinction ===

=== AC operators-truthiness ===
Intent: Conditional truthiness treats only false and null as false.

import json
import os
import subprocess

program = '[null, false, 0, "", []] | map(if . then true else false end)'
input_value = None
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [False, False, True, True, True]
=== END AC operators-truthiness ===

=== AC operators-defined-or ===
Intent: Defined-or returns the fallback for a false or null value.

import json
import os
import subprocess

program = ".missing // 7"
input_value = {}
payload = json.dumps(input_value) + "\n"
fallback = 7
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == fallback
=== END AC operators-defined-or ===

=== AC operators-runtime-error ===
Intent: Division by zero is reported as a runtime failure.

import json
import os
import subprocess

program = "1 / 0"
payload = "null\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 5
=== END AC operators-runtime-error ===

## User Acceptance

- None.

## Guardrails

- Preserve jq type distinctions; do not rely on Python boolean-number equality.
- Keep compile errors distinct from runtime errors.
- Do not silently coerce incompatible operand types.
