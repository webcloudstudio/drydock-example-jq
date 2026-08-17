# FEATURE: Core Generators

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Evaluate jq identity, literals, pipes, comma expressions, and empty as ordered generators. |
| Depends On  | FEATURE-Front-Validation.md |
| Provides    | generator evaluator, identity, literals, pipes, comma, empty |
| Consumes    | jq parser and AST |

## Intent

Implement jq's stream evaluation model. Every filter receives one input and may produce zero, one, or many ordered outputs. Pipes run downstream filters once per upstream result; comma concatenates streams; empty produces no results.

## Behavioral Contract

- Identity returns the exact input value.
- Comma preserves left-to-right output order and multiplicity.
- Pipes preserve Cartesian expansion across generated values.
- Empty emits no JSON value.

## Programmatic Acceptance

=== AC generators-identity ===
Intent: Identity returns the input value without changing its structure.

import json
import os
import subprocess

program = "."
input_value = {"items": [1, 2], "ok": True}
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == input_value
=== END AC generators-identity ===

=== AC generators-comma-order ===
Intent: Comma expressions emit all values in source order, including duplicates.

import json
import os
import subprocess

program = "1,1,2"
payload = "null\n"
expected = [1, 1, 2]
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == expected
=== END AC generators-comma-order ===

=== AC generators-pipe-expansion ===
Intent: A pipe evaluates its right side once for every value generated on the left.

import json
import os
import subprocess

program = ".[] | ."
input_value = [1, 2, 3]
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == input_value
=== END AC generators-pipe-expansion ===

=== AC generators-empty ===
Intent: The empty generator produces no output and still completes successfully.

import os
import subprocess

program = "empty"
payload = "null\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert result.stdout == ""
=== END AC generators-empty ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering, multiplicity, backtracking, and partial-output behavior.
- Do not collapse a filter stream into a single value.
- Use only Python standard-library/runtime facilities.
