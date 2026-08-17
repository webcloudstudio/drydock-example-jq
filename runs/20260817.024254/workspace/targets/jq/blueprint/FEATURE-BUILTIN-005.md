# FEATURE: Streaming, I/O, Debugging, and SQL-Style Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide jq streaming, remaining-input, debugging, and SQL-style builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-BUILTIN-001.md, FEATURE-BUILTIN-004.md, FEATURE-CLI-001.md |
| Provides    | input, inputs, debug, stderr, tostream, fromstream, truncate_stream, INDEX, JOIN, IN |
| Consumes    | stdin JSON stream, generator evaluator, data and path operations |

## Purpose

Implement the exercised I/O and streaming builtins while preserving the CLI's remaining-input state. `input` consumes one subsequent JSON value and `inputs` consumes the remaining values. `debug` and `stderr` write diagnostics to stderr without contaminating stdout. Streaming helpers must preserve jq path/value stream structure. `INDEX`, `JOIN`, and `IN` must evaluate generators in jq order and retain multiplicity.

## Programmatic Acceptance

=== AC builtin-005-streaming ===
Intent: The implementation passes the authoritative corpus cases for streaming and remaining-input behavior.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", r"^(input|inputs|tostream|fromstream|truncate_stream)"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC builtin-005-streaming ===

=== AC builtin-005-sql-debug ===
Intent: The implementation passes the authoritative corpus cases for debugging and SQL-style builtins.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", r"^(debug|INDEX|JOIN|IN)"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC builtin-005-sql-debug ===

## User Acceptance

- None.

## Guardrails

- Keep diagnostic side effects on stderr; never use stdout for diagnostics.
- Preserve input-stream state across filters and input documents.
- Do not modify supplied conformance assets.
