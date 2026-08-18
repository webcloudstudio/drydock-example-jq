# FEATURE: Streaming and I/O Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provides jq streaming transforms, additional-input filters, environment access, and diagnostic output. |
| Depends On  | FEATURE-Generator-Core.md, FEATURE-Executable-Contract.md |
| Provides    | tostream, fromstream, truncate_stream, input, inputs, debug, stderr, env, $ENV |
| Consumes    | generator evaluation, executable stdin and stderr |

## Purpose

Implement jq's streaming representation and process I/O builtins while preserving the executable's input and output contracts.

## Behavior

- `tostream`, `fromstream`, and `truncate_stream` convert between jq values and stream events.
- `input` consumes one additional JSON input and `inputs` consumes all remaining inputs.
- `env` and `$ENV` expose the process environment.
- `debug` writes diagnostic data to stderr while preserving the input value.
- `stderr` writes raw compact data to stderr and preserves jq's documented flow.
- Runtime I/O failures use exit status 5.

## Programmatic Acceptance

=== AC io-conformance ===
Intent: The implementation passes the authoritative corpus cases for streaming, environment, input, and diagnostic builtins.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select",
     r"(^|[^A-Za-z])(tostream|fromstream|truncate_stream|input|inputs|debug|stderr|env|\$ENV)\b"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC io-conformance ===

=== AC io-stream-status ===
Intent: A valid input-consuming program completes with the documented success status.
import subprocess

program = "input"
payload = "null\n1\n"
result = subprocess.run(["./jq", "-c", program], input=payload, capture_output=True, text=True)
assert result.returncode == 0
=== END AC io-stream-status ===

## User Acceptance

- None.

## Guardrails

- Diagnostics may be written only to stderr.
- Do not invoke external commands or access the network.
