# FEATURE: Eval Stream

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Evaluate jq filters as ordered zero-, one-, or many-valued streams. |
| Depends On  | ARCHITECTURE.md, FEATURE-Frontend-Parser.md, FEATURE-Frontend-Validation.md |
| Provides    | ordered generator evaluator |
| Consumes    | parser and AST |

## Intent

The evaluator's fundamental contract is stream evaluation. Every filter receives one input and may produce zero, one, or many outputs. Downstream filters run once for each upstream output, preserving jq ordering and outputs emitted before a later runtime error.

## Stream Semantics

The evaluator must support:

- empty streams;
- ordered comma streams;
- pipeline fan-out;
- nested collection of streams;
- independent processing of multiple JSON inputs;
- runtime failure after earlier outputs without losing those outputs.

## Programmatic Acceptance

=== AC eval-stream-fanout ===
Intent: A generator pipeline preserves every upstream value and its order.

import json
import subprocess

input_value = [1, 2, 3]
source = ".[]"
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == input_value
=== END AC eval-stream-fanout ===

=== AC eval-stream-pipeline ===
Intent: Downstream filters execute once for each upstream generator output.

import json
import subprocess

input_value = [1, 2, 3]
source = ".[] | . * 2"
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [value * 2 for value in input_value]
assert actual == expected
=== END AC eval-stream-pipeline ===

=== AC eval-stream-empty ===
Intent: The empty filter produces no output while completing successfully.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "empty"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout == ""
=== END AC eval-stream-empty ===

=== AC eval-stream-order ===
Intent: Comma composition preserves left-to-right stream order.

import json
import subprocess

input_value = [10, 20]
source = ".[] as $x | ($x, $x + 1)"
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [item for value in input_value for item in (value, value + 1)]
assert actual == expected
=== END AC eval-stream-order ===

## User Acceptance

- None.

## Guardrails

- Do not collapse streams into a single value.
- Preserve output ordering and values emitted before runtime errors.
- Do not implement evaluation by delegating to a system jq binary.
