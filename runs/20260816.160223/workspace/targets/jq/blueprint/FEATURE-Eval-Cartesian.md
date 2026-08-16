# FEATURE: Eval Cartesian

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Evaluate multi-output operator and function arguments in jq cartesian order. |
| Depends On  | ARCHITECTURE.md, FEATURE-Eval-Core.md |
| Provides    | cartesian argument evaluation |
| Consumes    | ordered generator evaluator |

## Intent

Expressions that combine generator-valued arguments evaluate every output combination in jq's defined order. This applies to binary operators, function arguments, and constructors. Each argument is evaluated against the same input context before combinations are emitted.

## Programmatic Acceptance

=== AC eval-cartesian-binary ===
Intent: Binary operators produce the cartesian product of multi-output operands.

import json
import subprocess

input_value = [1, 2]
source = ".[] + .[]"
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [left + right for left in input_value for right in input_value]
assert actual == expected
=== END AC eval-cartesian-binary ===

=== AC eval-cartesian-function ===
Intent: Function arguments retain all combinations when each argument is a generator.

import json
import subprocess

source = 'range(0, 1; 3, 4)'
result = subprocess.run(
    ["./jq", "-c", source],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = list(range(0, 3)) + list(range(0, 4))
assert actual == expected
=== END AC eval-cartesian-function ===

=== AC eval-cartesian-constructor ===
Intent: Array constructors collect every output from generator-valued elements in order.

import json
import subprocess

input_value = [2, 4]
source = "[.[], .[] + 1]"
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = input_value + [value + 1 for value in input_value]
assert actual == expected
=== END AC eval-cartesian-constructor ===

=== AC eval-cartesian-order ===
Intent: Multiple input values are evaluated independently without cross-input mixing.

import json
import subprocess

input_values = [2, 5]
source = ".[]"
result = subprocess.run(
    ["./jq", "-c", source],
    input="\n".join(json.dumps(value) for value in input_values) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = input_values
assert actual == expected
=== END AC eval-cartesian-order ===

## User Acceptance

- None.

## Guardrails

- Preserve jq-defined nesting and left-to-right ordering.
- Evaluate each generator argument against the correct input context.
- Do not deduplicate or collapse repeated cartesian outputs.
