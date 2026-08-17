# FEATURE: Core Indexing

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Implement jq field access, dynamic indexing, iteration, optional access, and slicing. |
| Depends On  | FEATURE-Core-Generators.md |
| Provides    | array/object/string indexing, iteration, optional access, slices |
| Consumes    | generator evaluator |

## Intent

Implement access to object fields, array elements, string characters, dynamic keys, iterators, optional access, negative indices, and array or string slices. Missing ordinary object fields yield null; invalid operations raise runtime errors unless optional access suppresses them.

## Behavioral Contract

- `.field` and `.[key]` access object values.
- `.[]` emits array elements or object values in iteration order.
- Negative array indices count from the end.
- Slices use inclusive start and exclusive end bounds and support omitted or negative bounds.
- `?` suppresses indexing and iteration errors.

## Programmatic Acceptance

=== AC indexing-object-field ===
Intent: Object field access returns the value associated with the requested key.

import json
import os
import subprocess

program = ".name"
input_value = {"name": "jq", "version": 1}
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == input_value["name"]
=== END AC indexing-object-field ===

=== AC indexing-iteration ===
Intent: Array iteration emits each element in order.

import json
import os
import subprocess

program = ".[]"
input_value = ["a", "b", "c"]
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
=== END AC indexing-iteration ===

=== AC indexing-negative-index ===
Intent: Negative indexing selects from the end of an array.

import json
import os
import subprocess

program = ".[-1]"
input_value = [10, 20, 30]
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == input_value[-1]
=== END AC indexing-negative-index ===

=== AC indexing-slice ===
Intent: Array slicing returns the requested half-open range.

import json
import os
import subprocess

program = ".[1:3]"
input_value = [0, 1, 2, 3]
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == input_value[1:3]
=== END AC indexing-slice ===

=== AC indexing-optional-access ===
Intent: Optional access suppresses an invalid indexing operation.

import json
import os
import subprocess

program = ".[]?"
input_value = [1, [], {"x": 2}]
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
=== END AC indexing-optional-access ===

## User Acceptance

- None.

## Guardrails

- Preserve null results for missing fields and the documented distinction between missing access and invalid access.
- Do not mutate input values while indexing or slicing.
- Preserve stream order and multiplicity.
