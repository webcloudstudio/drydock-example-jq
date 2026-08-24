# FEATURE: Executable jq Entry Point

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides the executable jq command and its basic stdin-to-stdout filter interface. |
| Depends On  | ARCHITECTURE.md |
| Provides    | ./jq -c program execution |
| Consumes    | interpreter parser and evaluator |

## Workflow

1. Start the executable at the application root as `./jq`.
2. Accept the exercised `-c '<program>'` interface.
3. Read JSON input from standard input.
4. Compile and evaluate the jq program for each input value.
5. Emit each generated result as one compact JSON line.
6. Exit successfully after all inputs complete.

The implementation must support multiple input values and preserve output order. The executable may delegate to modular Python files beside it, but the delivered command remains the root-level executable named `jq`.

## Interface

| Input | Contract |
|---|---|
| Arguments | `-c` followed by one jq program string. |
| Standard input | JSON values in the corpus input format. |
| Standard output | One compact JSON value per generated result line. |
| Standard error | Diagnostics only. |
| Success status | `0`. |

## Programmatic Acceptance

=== AC exec-001-conformance ===
Intent: The executable runs the basic identity interface successfully.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["./jq", "-c", "."],
    input="true\nfalse\nnull\n1\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout.splitlines() == ["true", "false", "null", "1"]

=== END AC exec-001-conformance ===

=== AC exec-001-process ===
Intent: The executable accepts the declared -c interface and completes a supplied identity filter successfully.

import json
import subprocess

payload = "null\n"
result = subprocess.run(
    ["./jq", "-c", "."],
    input=payload,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
assert result.stdout.splitlines() == [payload.strip()]
=== END AC exec-001-process ===

## User Acceptance

- None.

## Guardrails

- The delivered command is exactly `jq` at the application root.
- The implementation accepts the exercised `-c` interface.
- Output is compact and line-oriented.
- The executable does not invoke another jq implementation.
- Diagnostics are not written to standard output.
