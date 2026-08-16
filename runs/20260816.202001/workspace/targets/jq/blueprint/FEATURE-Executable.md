# FEATURE: Executable jq Entry Point

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Deliver the executable jq command-line interface and its JSON stream contract. |
| Depends On  | FEATURE-IO-Streaming.md, FEATURE-SQL-Introspection.md |
| Provides    | ./jq -c '<program>', compact JSON result stream, exit codes 0/3/5 |
| Consumes    | complete jq interpreter |

## Interface

The repository root contains an executable named `jq`. It accepts the exercised `-c '<program>'` form, reads JSON documents from stdin, emits one compact JSON result per line, and uses exit status 0 for completion, 3 for compilation failure, and 5 for uncaught runtime failure.

## Programmatic Acceptance

=== AC executable-stream ===
Intent: The executable accepts -c and emits one compact result per generated value.

import json
import subprocess

source = "[.[] | . + 1]"
value = [1, 2, 3]
result = subprocess.run(["./jq", "-c", source], input=json.dumps(value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = [item + 1 for item in value]
assert actual == expected
assert all("\n" not in line.strip() for line in result.stdout.splitlines())
=== END AC executable-stream ===

=== AC executable-compile-status ===
Intent: A syntactically invalid program exits with status 3.

import subprocess

result = subprocess.run(["./jq", "-c", "{"], input="null\n", capture_output=True, text=True)
assert result.returncode == 3
=== END AC executable-compile-status ===

=== AC executable-runtime-status ===
Intent: An uncaught runtime failure exits with status 5 after compilation succeeds.

import subprocess

result = subprocess.run(["./jq", "-c", "1 / 0"], input="null\n", capture_output=True, text=True)
assert result.returncode == 5
=== END AC executable-runtime-status ===

## User Acceptance

- None.

## Guardrails

- Keep stdout exclusively for compact JSON result values.
- Keep diagnostics exclusively on stderr.
- Do not shell out to another jq implementation.
- Do not require network access, package installation, or third-party runtime dependencies.
