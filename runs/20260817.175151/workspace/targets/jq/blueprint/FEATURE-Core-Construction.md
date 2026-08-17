# FEATURE: Core Construction

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Construct arrays and objects by collecting and expanding generator results. |
| Depends On  | FEATURE-Core-Generators.md, FEATURE-Core-Indexing.md, FEATURE-Core-Values-Operators.md |
| Provides    | array and object constructors |
| Consumes    | generator evaluator, jq indexing |

## Intent

Implement jq array and object construction. Array expressions collect every output from their generator expression. Object expressions evaluate value generators against the same input, producing one object per Cartesian combination, with support for literal keys, identifier shorthand, variable keys, and parenthesized dynamic keys.

## Behavioral Contract

- `[]` constructs an empty array.
- Array constructors preserve generator order and collect zero or more outputs.
- Object value generators expand into ordered output objects.
- Object keys must resolve to strings.
- Shorthand keys read the corresponding field from the current input.

## Programmatic Acceptance

=== AC construction-array-collection ===
Intent: Array construction collects all outputs from a generator in order.

import json
import os
import subprocess

program = "[.[]]"
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
assert json.loads(result.stdout) == input_value
=== END AC construction-array-collection ===

=== AC construction-empty-array ===
Intent: The empty array constructor returns an empty array.

import json
import os
import subprocess

program = "[]"
payload = "null\n"
expected = []
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC construction-empty-array ===

=== AC construction-object-values ===
Intent: Object construction evaluates fields against the current input.

import json
import os
import subprocess

program = "{name: .name, count: .items | length}"
input_value = {"name": "example", "items": [1, 2]}
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
assert actual["name"] == input_value["name"]
assert actual["count"] == len(input_value["items"])
=== END AC construction-object-values ===

=== AC construction-object-generator-expansion ===
Intent: A multi-output object value produces one object for each generated value.

import json
import os
import subprocess

program = "{value: .[]}"
input_value = [4, 5]
payload = json.dumps(input_value) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [{"value": value} for value in input_value]
=== END AC construction-object-generator-expansion ===

=== AC construction-dynamic-key ===
Intent: A parenthesized key expression creates a string-keyed object field.

import json
import os
import subprocess

program = "{(.key): .value}"
input_value = {"key": "chosen", "value": 9}
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
assert actual == {input_value["key"]: input_value["value"]}
=== END AC construction-dynamic-key ===

## User Acceptance

- None.

## Guardrails

- Preserve generator order and Cartesian-product multiplicity in object construction.
- Reject non-string constant object keys during compilation.
- Do not mutate the source input while constructing arrays or objects.
