# FEATURE: CLI Entrypoint

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines the executable jq command and its compact JSON stdin/stdout contract. |
| Depends On  | ARCHITECTURE.md |
| Provides    | ./jq -c, compact JSON output stream |
| Consumes    | interpreter runtime |

## Workflow

The root-level executable accepts `-c` followed by one jq program. It reads JSON values from standard input, evaluates the program independently for each input value, and emits every resulting value as one compact JSON line. Input order and generator output order are preserved.

The executable must support multiple newline-delimited JSON inputs and must not add presentation formatting to compact output.

## Programmatic Acceptance

=== AC cli-input-output ===
Intent: The executable evaluates a jq program against stdin and emits compact JSON values.

import json
import subprocess

program = ". + 1"
input_value = 41
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = input_value + 1
assert actual == [expected]
=== END AC cli-input-output ===

=== AC cli-multiple-inputs ===
Intent: Each newline-delimited JSON input is processed and emitted in order.

import json
import subprocess

program = "."
input_values = [1, 2, 3]
payload = "".join(json.dumps(value) + "\n" for value in input_values)
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == input_values
=== END AC cli-multiple-inputs ===

=== AC cli-generator-output ===
Intent: Multiple values produced by one filter are emitted as separate compact JSON lines.

import json
import subprocess

program = ".[]"
input_value = ["a", "b", "c"]
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == input_value
=== END AC cli-generator-output ===

## User Acceptance

- None.

## Guardrails

- The only exercised command-line option is `-c`.
- Output is compact JSON, one value per line.
- The executable is located at the application root and is executable.
- The wrapper must not alter generator ordering or discard prior outputs.
