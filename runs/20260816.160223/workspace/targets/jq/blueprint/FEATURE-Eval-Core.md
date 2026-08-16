# FEATURE: Eval Core

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implement jq's core composition, construction, iteration, and indexing operations. |
| Depends On  | ARCHITECTURE.md, FEATURE-Eval-Stream.md |
| Provides    | identity, literals, pipes, commas, iteration, collection, empty, indexing, slicing |
| Consumes    | ordered generator evaluator |

## Intent

The core evaluator executes the AST operations shared by all later jq features. It must implement identity and literals, composition, collection, iteration over arrays and objects, field and computed indexing, optional access, and array or string slices.

## Core Behaviors

- Identity returns the current value.
- Pipes feed every left-hand output into the right-hand filter.
- Commas concatenate output streams.
- Array collection gathers all outputs into one array.
- Iteration emits array elements or object values.
- Missing object fields produce null.
- Slices use jq's inclusive-start, exclusive-end behavior and support omitted or negative bounds.

## Programmatic Acceptance

=== AC eval-core-identity ===
Intent: Identity and literal filters return their input-derived and constant values.

import json
import subprocess

input_value = {"x": 7}
result = subprocess.run(
    ["./jq", "-c", "., 3"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [input_value, 3]
=== END AC eval-core-identity ===

=== AC eval-core-collection ===
Intent: Collection gathers all outputs of a generator into one array.

import json
import subprocess

input_value = [1, 2, 3]
result = subprocess.run(
    ["./jq", "-c", "[.[]]"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == input_value
=== END AC eval-core-collection ===

=== AC eval-core-indexing ===
Intent: Field, computed index, and iteration access the corresponding input values.

import json
import subprocess

input_value = {"items": [4, 5], "name": "jq"}
source = "[.name, .items[1], [.items[]]]"
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0] == input_value["name"]
assert actual[1] == input_value["items"][1]
assert actual[2] == input_value["items"]
=== END AC eval-core-indexing ===

=== AC eval-core-slices ===
Intent: Array and string slicing follows jq's bounds and ordering semantics.

import json
import subprocess

array_value = [0, 1, 2, 3, 4]
result = subprocess.run(
    ["./jq", "-c", ".[1:4]"],
    input=json.dumps(array_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == array_value[1:4]

text_value = "abcdef"
result = subprocess.run(
    ["./jq", "-c", ".[-2:]"],
    input=json.dumps(text_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == text_value[-2:]
=== END AC eval-core-slices ===

## User Acceptance

- None.

## Guardrails

- Preserve jq stream ordering when collecting or iterating.
- Optional access suppresses access errors without suppressing valid values.
- Do not mutate input values during indexing or collection.
