# FEATURE: Input Streams

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq controls for consuming additional JSON input values. |
| Depends On  | FEATURE-Date-and-Time.md, FEATURE-Json-IO.md |
| Provides    | input, inputs, input_filename, input_line_number |
| Consumes    | executable JSON input boundary |

## Intent

Implement `input` and `inputs` over the fixed stdin interface, preserving the distinction between the initially filtered value and remaining values. Provide the available filename and line-number metadata without adding unsupported command-line options.

## Programmatic Acceptance

=== AC io-001-conformance ===
Intent: The input filter consumes the next JSON value from stdin.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "input"],
    input="1\n2\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == 2

=== END AC io-001-conformance ===

=== AC io-001-execution ===
Intent: The inputs filter emits all remaining JSON values in order.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "inputs"],
    input="1\n2\n3\n",
    capture_output=True,
    text=True,
)
values = [json.loads(line) for line in result.stdout.splitlines()]
assert result.returncode == 0
assert values == [2, 3]

=== END AC io-001-execution ===

## User Acceptance

- None.

## Guardrails

- Do not add command-line options beyond the fixed `-c` interface.
- Preserve input ordering and stream multiplicity.
- Use only the supplied stdin boundary and standard-library runtime.
