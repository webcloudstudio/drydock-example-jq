# FEATURE: Flow Reduce

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq reduce and foreach accumulation over generator streams. |
| Depends On  | FEATURE-Flow-Bindings.md, FEATURE-Flow-Control-Errors.md |
| Provides    | reduce and foreach |
| Consumes    | lexical bindings, control flow |

## Purpose

Implement `reduce` and `foreach` with generator sources, destructuring patterns, accumulator updates, intermediate extraction, nested output streams, and label-based early termination.

## Programmatic Acceptance

=== AC flow-reduce-suite ===
Intent: The implementation passes conformance cases for reduce expressions and accumulator updates.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\breduce\b"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-reduce-suite ===

=== AC flow-foreach-suite ===
Intent: The implementation passes conformance cases for foreach extraction and stream order.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\bforeach\b"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-foreach-suite ===

## User Acceptance

- None.

## Guardrails

- Accumulator updates must process generator outputs in order.
- Destructuring must bind each reduction item according to jq pattern semantics.
- Foreach extraction must expose each intermediate accumulator state exactly once per source output.
