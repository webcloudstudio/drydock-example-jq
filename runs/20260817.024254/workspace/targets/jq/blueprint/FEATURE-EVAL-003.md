# FEATURE: Generator Control Constructs

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | jq reductions, bounded generators, recursive loops, labels, and breaks preserve stream control semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-002.md, FEATURE-FRONTEND-003.md |
| Provides    | reduce, foreach, limit, skip, first, last, nth, while, until, repeat, labels, breaks |
| Consumes    | generator evaluator, functions, error handling |

## Intent

This capability implements jq constructs whose meaning depends on controlled traversal of generator streams. It must support reductions and intermediate extraction, bounded consumption, recursive iteration, short-circuiting, lexical labels, and partial-output behavior.

## Behavior

- `reduce` accumulates every generator output in order.
- `foreach` exposes each intermediate accumulator through its extraction filter.
- `limit`, `skip`, `first`, `last`, and `nth` consume only the required stream values.
- `while`, `until`, and `repeat` recurse with jq's stream semantics.
- Labels and breaks terminate the corresponding lexical generator scope.
- Control constructs preserve cartesian products, short-circuiting, and runtime errors.

## Programmatic Acceptance

=== AC eval-003-reduction ===
Intent: The implementation passes the authoritative corpus cases for reduce and foreach.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"reduce|foreach|intermediate|accumul"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-003-reduction ===

=== AC eval-003-bounds ===
Intent: The implementation passes the authoritative corpus cases for limit, skip, first, last, and nth.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"limit|skip|first\(|last\(|nth\("
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-003-bounds ===

=== AC eval-003-recursion ===
Intent: The implementation passes the authoritative corpus cases for while, until, repeat, labels, breaks, and recursive generators.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"while|until|repeat|label|break|Recursion|recurse"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC eval-003-recursion ===

## User Acceptance

- None.

## Guardrails

- Do not materialize unbounded generators unnecessarily.
- Ensure bounded constructs stop consuming input after their contract is satisfied.
- Keep labels lexical and prevent breaks from escaping their visible scope.
