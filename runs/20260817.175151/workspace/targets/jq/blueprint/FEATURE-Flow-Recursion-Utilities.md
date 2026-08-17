# FEATURE: Flow Recursion Utilities

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq range, iteration, stream-limiting, selection, and recursive generator utilities. |
| Depends On  | FEATURE-Flow-Control-Errors.md, FEATURE-Flow-Reduce.md |
| Provides    | range, while, until, repeat, limit, skip, first, last, nth, recurse |
| Consumes    | generator evaluator, control flow |

## Purpose

Implement generator utilities including `range`, `while`, `until`, `repeat`, `limit`, `skip`, `first`, `last`, `nth`, and `recurse`. Preserve stream order, multiplicity, short-circuiting, recursive traversal, and documented negative-argument errors.

## Programmatic Acceptance

=== AC flow-range-utilities ===
Intent: The implementation passes conformance cases for range, limit, skip, first, last, and nth.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\brange\b|\blimit\b|\bskip\b|\bfirst\b|\blast\b|\bnth\b"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-range-utilities ===

=== AC flow-recursion-utilities ===
Intent: The implementation passes conformance cases for while, until, repeat, and recurse generators.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\bwhile\b|\buntil\b|\brepeat\b|\brecurse\b|\.\."],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-recursion-utilities ===

## User Acceptance

- None.

## Guardrails

- Stream utilities must preserve jq generator ordering and multiplicity.
- Negative counts must produce runtime errors where jq specifies them.
- Recursive generators must not emit values after their terminating condition or break.
