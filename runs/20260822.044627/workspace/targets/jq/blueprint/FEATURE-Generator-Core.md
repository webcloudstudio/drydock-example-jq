# FEATURE: Generator Core

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Evaluate jq filters as ordered streams of zero or more values. |
| Depends On  | FEATURE-Declaration-Parser.md |
| Provides    | ordered generator evaluation, empty, iteration, range |
| Consumes    | AST for filter expressions |

Every filter shall evaluate against an input value as an ordered generator. The evaluator shall preserve zero, one, and multiple outputs, backtracking, identity, array/object iteration, recursive descent support, `range`, and `empty`. Output order and multiplicity are semantic requirements.

## Programmatic Acceptance

=== AC core-001-generators ===
Intent: Identity, iteration, empty, and range generator behavior is implemented.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "[., range(2)]"],
    input="7\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == [7, 0, 1]

=== END AC core-001-generators ===

=== AC core-001-ordering ===
Intent: Generator output order and multiplicity are preserved.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", ".[] , .[]"],
    input="[1, 2]\n",
    capture_output=True,
    text=True,
)
values = [json.loads(line) for line in result.stdout.splitlines()]
assert result.returncode == 0
assert values == [1, 2, 1, 2]

=== END AC core-001-ordering ===

## User Acceptance

- None.

## Guardrails

- Treat generators and backtracking as the evaluation model, not an optimization.
- Preserve partial output before a later runtime failure.
- Do not shell out to another jq implementation.
