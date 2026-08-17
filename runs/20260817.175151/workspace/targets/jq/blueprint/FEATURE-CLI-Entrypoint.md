# FEATURE: CLI Entrypoint

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines the executable jq command-line interface for JSON filter evaluation. |
| Depends On  | — |
| Provides    | executable jq, stdin JSON reader, compact JSON output |
| Consumes    | — |

## Intent

The application root contains an executable named `jq`. It accepts `-c` followed by a jq program, reads JSON values from standard input, evaluates the program, and writes every produced value as one compact JSON value per line. The implementation uses only Python standard-library facilities.

## Programmatic Acceptance

=== AC cli-entrypoint-roundtrip ===
Intent: The executable reads stdin JSON and emits the same JSON value through the identity filter.

import json
import os
import subprocess
import sys

payload = {"name": "jq", "items": [1, 2, 3]}
result = subprocess.run(
    ["./jq", "-c", "."],
    input=json.dumps(payload) + "\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == payload
=== END AC cli-entrypoint-roundtrip ===

=== AC cli-entrypoint-stream ===
Intent: The executable emits one output line for each input JSON value.

import json
import os
import subprocess

values = [1, {"a": 2}, [3, 4]]
result = subprocess.run(
    ["./jq", "-c", "."],
    input="".join(json.dumps(value) + "\n" for value in values),
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == values
=== END AC cli-entrypoint-stream ===

## User Acceptance

- None.

## Guardrails

- The executable must not require network access, package installation, third-party runtime dependencies, or a system jq executable.
- The supplied `sources/` assets remain read-only.
