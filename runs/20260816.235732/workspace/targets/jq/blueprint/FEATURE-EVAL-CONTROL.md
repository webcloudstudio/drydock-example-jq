# FEATURE: Control Flow and Runtime Errors

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implements jq control flow, reductions, recursive generators, labels, and error handling. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-GENERATOR.md, FEATURE-EVAL-VALUES.md |
| Provides    | jq control flow, try/catch, labels, reductions, recursive generators |
| Consumes    | generator evaluator, jq value operations |

## Scope

Implement conditionals and `elif`, `//`, `try` and `catch`, optional expressions, labels and breaks, `reduce`, `foreach`, `limit`, `skip`, `first`, `last`, `nth`, `while`, `until`, `repeat`, and `recurse`.

Control constructs must operate over streams, preserve partial output before runtime failure, short-circuit where jq specifies it, and distinguish caught errors from uncaught runtime errors.

## Programmatic Acceptance

=== AC control-flow ===
Intent: The authoritative corpus passes conditionals, alternatives, try/catch, and optional-expression cases.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^if |^try |^\.foo \?\?|^empty //|^\[\.\\[.*\]\?"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC control-flow ===

=== AC reductions-and-loops ===
Intent: The authoritative corpus passes reductions, foreach, bounded generators, and recursive control constructs.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^reduce |^foreach |^limit\(|^skip\(|^first\(|^nth\(|^while\(|^until\(|^recurse"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC reductions-and-loops ===

=== AC control-runtime-status ===
Intent: An uncaught control-expression runtime failure uses the documented runtime exit status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "limit(-1; .)"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC control-runtime-status ===

## User Acceptance

- None.

## Guardrails

- Preserve short-circuiting and label/break scope.
- Preserve values emitted before a runtime error.
- Do not convert caught errors into process failures.
