# FEATURE: Executable Contract

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implements the jq executable process, JSON stream, output, and exit-status contract. |
| Depends On  | ARCHITECTURE.md |
| Provides    | `./jq -c`, stdin JSON stream processing, compact JSON line output, exit codes `0`, `3`, and `5` |
| Consumes    | Interpreter architecture |

## Interface

The executable accepts `./jq -c '<program>'`. It reads one or more JSON values from standard input, evaluates the program for each value in order, and emits every result as one compact JSON value per line.

## Programmatic Acceptance

=== AC executable-stream ===
Intent: The executable evaluates a valid filter over multiple JSON inputs and preserves output order.

import json
import os
import subprocess

inputs = [1, 2, 3]
payload = "".join(json.dumps(value) + "\n" for value in inputs)
result = subprocess.run(
    ["./jq", "-c", "."],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == inputs
=== END AC executable-stream ===

=== AC executable-compile-status ===
Intent: A syntactically invalid jq program returns the declared compile-failure status.

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
=== END AC executable-compile-status ===

=== AC executable-runtime-status ===
Intent: A compiled program that raises at runtime returns the declared runtime-failure status.

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 5
=== END AC executable-runtime-status ===

## User Acceptance

- None.

## Guardrails

- Only `-c` is required and exercised.
- Diagnostics go to standard error.
- Output is compact JSON, one value per line.
- Compile and runtime failures must remain distinguishable.
