# FEATURE: Flow Control Errors

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq conditionals, error handling, optional filters, labels, and breaks. |
| Depends On  | FEATURE-Core-Values-Operators.md, FEATURE-Flow-Functions.md |
| Provides    | if, then, elif, else, try, catch, optional filters, labels, break |
| Consumes    | generator evaluator |

## Purpose

Implement jq truthiness and conditional branching, `try`/`catch`, `?`, `error`, `halt`, `halt_error`, lexical labels, and `break`. Runtime failures must preserve values already emitted and map to the required runtime status.

## Programmatic Acceptance

=== AC flow-conditionals-suite ===
Intent: The implementation passes conformance cases for conditionals, truthiness, and logical control flow.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\bif\b|\bthen\b|\belif\b|\belse\b|\bend\b|truth"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-conditionals-suite ===

=== AC flow-errors-suite ===
Intent: The implementation passes conformance cases for errors, try/catch, optional filters, labels, and breaks.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\btry\b|\bcatch\b|error|label|break|\?"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-errors-suite ===

## User Acceptance

- None.

## Guardrails

- Only `false` and `null` are false in jq conditionals.
- Runtime errors must remain distinct from compile errors.
- `break` must resolve only to a lexically visible label.
