# FEATURE: CLI Executable

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides the executable jq command interface and its stdin, stdout, and exit-code contract. |
| Depends On  | FEATURE-Builtins-Extended.md |
| Provides    | executable jq, -c program interface, JSON stdin/stdout protocol, exit codes 0/3/5 |
| Consumes    | complete evaluator |

## Intent

Deliver an executable named `jq` at the application root. It accepts `-c` and one jq program, reads JSON values from standard input, emits every generated result as one compact JSON value per line, writes diagnostics only to standard error, and distinguishes successful completion, compilation failure, and runtime failure with exit codes 0, 3, and 5.

## Programmatic Acceptance

=== AC cli-executable-stream ===
Intent: The executable reads supplied JSON input and emits the same generated values as compact JSON lines.
Requires: executable=python3; scope=test

import json
import subprocess

input_value = {"items": [1, 2, 3]}
source = json.dumps(input_value, separators=(",", ":")) + "\n"
result = subprocess.run(
    ["./jq", "-c", ".items[]"],
    input=source,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = input_value["items"]
assert actual == expected

=== END AC cli-executable-stream ===

=== AC cli-executable-exit-codes ===
Intent: The executable distinguishes compile failures from runtime failures.
Requires: executable=python3; scope=test

import subprocess

compile_result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
runtime_result = subprocess.run(
    ["./jq", "-c", "1 / 0"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert compile_result.returncode == 3
assert runtime_result.returncode == 5

=== END AC cli-executable-exit-codes ===

## User Acceptance

- None.

## Guardrails

- The only required command-line option is `-c`.
- Do not shell out to a system jq executable.
- Diagnostics must not be emitted as ordinary JSON results on stdout.
