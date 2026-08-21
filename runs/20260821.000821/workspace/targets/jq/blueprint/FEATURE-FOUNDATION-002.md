# FEATURE: Executable jq Command Contract

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides the executable jq command-line, JSON stream boundary, and documented exit statuses. |
| Depends On  | FEATURE-FOUNDATION-001.md |
| Provides    | executable jq, -c CLI, JSON stdin/stdout boundary, compile exit status 3, runtime exit status 5 |
| Consumes    | staged jq assets |

## Scope

The application root contains an executable named `jq`, invoked as `./jq -c '<program>'`. It reads JSON values from standard input, evaluates the supplied filter for each input value, writes each produced value as one compact JSON value per line, and writes diagnostics to standard error.

Compilation failures return status `3`. Runtime failures return status `5`, while retaining values emitted before the failure. Successful completion returns status `0`.

## Programmatic Acceptance

=== AC cli-round-trip ===
Intent: The executable accepts the exercised -c form and emits each supplied JSON value as compact JSON.

import json
import os
import subprocess

payload_values = [{"a": 1}, [2, 3], "text"]
payload = "\n".join(json.dumps(value) for value in payload_values) + "\n"

result = subprocess.run(
    ["./jq", "-c", "."],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == payload_values
=== END AC cli-round-trip ===

=== AC cli-compile-status ===
Intent: A syntactically invalid jq program returns the documented compile-failure status.

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
=== END AC cli-compile-status ===

=== AC cli-runtime-status ===
Intent: A runtime error returns status 5 after preserving values emitted before the error.

import json
import os
import subprocess

prefix = 1
result = subprocess.run(
    ["./jq", "-c", "1, error"],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 5
assert [json.loads(line) for line in result.stdout.splitlines()] == [prefix]
=== END AC cli-runtime-status ===

## User Acceptance

- The command can be invoked directly as `./jq -c '<program>'` from the application root.

## Guardrails

- Implement the interpreter in Python using only the standard library.
- Do not shell out to a system jq executable or use a third-party jq implementation.
- Diagnostics belong on standard error and are not part of the JSON output stream.
