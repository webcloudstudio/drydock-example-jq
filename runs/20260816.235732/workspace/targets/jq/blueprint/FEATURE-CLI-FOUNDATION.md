# FEATURE: CLI Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Executable jq entry point for compact JSON filtering and documented process outcomes. |
| Depends On  | ARCHITECTURE.md |
| Provides    | executable jq, compact JSON output, compile/runtime exit codes |
| Consumes    | interpreter module boundaries |

## Purpose

Provide the application-root executable `jq` and the `./jq -c '<program>'` process contract.

## Workflow

1. Validate the exercised `-c` invocation and obtain the jq program.
2. Read JSON input values from stdin.
3. Compile the program once for the process.
4. Evaluate the filter for each input value as a generator.
5. Emit every result as compact JSON on its own stdout line.
6. Send diagnostics to stderr and return the documented status.

The implementation must support multiple newline-delimited JSON inputs and preserve output order and multiplicity.

## Error Behavior

Compilation or static errors return status `3`. Runtime errors return status `5`, while retaining outputs produced before the error. Successful execution returns status `0`.

## Programmatic Acceptance

=== AC cli-identity ===
Intent: The executable accepts compact mode, reads JSON stdin, and emits a compact JSON result.

import json
import subprocess

value = {"name": "jq", "items": [1, 2, 3]}
payload = json.dumps(value) + "\n"
expected = json.dumps(value, separators=(",", ":")) + "\n"
result = subprocess.run(
    ["./jq", "-c", "."],
    input=payload,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert result.stdout == expected
=== END AC cli-identity ===

=== AC cli-generator-output ===
Intent: The executable emits one compact line for each generated array element in source order.

values = [3, 1, 4]
import json
import subprocess

payload = json.dumps(values) + "\n"
expected = "".join(json.dumps(item, separators=(",", ":")) + "\n" for item in values)
result = subprocess.run(
    ["./jq", "-c", ".[]"],
    input=payload,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert result.stdout == expected
=== END AC cli-generator-output ===

=== AC cli-compile-error ===
Intent: A syntactically invalid jq program returns the documented compile-error status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 3
=== END AC cli-compile-error ===

=== AC cli-runtime-error ===
Intent: A compiled program that raises at runtime returns the documented runtime-error status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "1 / 0"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 5
=== END AC cli-runtime-error ===

## User Acceptance

- None.

## Guardrails

- Do not alter the supplied conformance harness or corpus.
- Do not shell out to another jq implementation.
- Emit results only as compact JSON lines on stdout.
