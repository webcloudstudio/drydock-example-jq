# FEATURE: JSON Input and Compact Output

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Reads JSON input streams and serializes generated values as ordered compact lines. |
| Depends On  | FEATURE-EXEC-002.md |
| Provides    | JSON stdin reader, ordered JSON-lines serializer |
| Consumes    | ./jq -c '<program>' |

## Intent

Read JSON values from standard input in the format exercised by the supplied corpus. Evaluate each input in order and emit every generated output as one compact JSON value per line, preserving order and multiplicity.

## Programmatic Acceptance

=== AC multiple-input-values ===
Intent: Multiple JSON input values are processed in order and emitted one per line.

import subprocess

inputs = "1\n2\n3\n"
result = subprocess.run(
    ["./jq", "-c", "."],
    input=inputs,
    capture_output=True,
    text=True,
)
expected = inputs.splitlines()
actual = result.stdout.splitlines()
assert result.returncode == 0
assert actual == expected
=== END AC multiple-input-values ===

=== AC generator-line-output ===
Intent: Multiple outputs generated from one input preserve order and multiplicity.

import subprocess

input_text = "[1,2,3]\n"
result = subprocess.run(
    ["./jq", "-c", ".[]"],
    input=input_text,
    capture_output=True,
    text=True,
)
expected = ["1", "2", "3"]
assert result.returncode == 0
assert result.stdout.splitlines() == expected
=== END AC generator-line-output ===

=== AC compact-json-output ===
Intent: Generated objects are serialized as single-line JSON values.

import json
import subprocess

input_text = '{"a": 1, "b": [2, 3]}\n'
result = subprocess.run(
    ["./jq", "-c", "."],
    input=input_text,
    capture_output=True,
    text=True,
)
decoded = json.loads(input_text)
actual = json.loads(result.stdout)
assert result.returncode == 0
assert actual == decoded
assert len(result.stdout.splitlines()) == 1
=== END AC compact-json-output ===

## User Acceptance

- None.

## Guardrails

- Emit one JSON value per output line.
- Preserve generator order and multiplicity.
- Do not pretty-print or combine separate generated values.
