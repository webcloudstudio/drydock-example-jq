# FEATURE: Core Utilities

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Implement jq generator utilities with correct short-circuiting and backtracking. |
| Depends On | FEATURE-Core-Errors.md |
| Provides | range, while, until, repeat, first, last, nth, limit, skip, any, all, combinations, transpose |
| Consumes | runtime exit status 5, try/catch, optional filters, empty, defined-or |

## Scope

Implement generator utilities from the jq standard library while preserving generator multiplicity and required short-circuit behavior.

## Programmatic Acceptance

=== AC utilities-conformance ===
Intent: The selected generator-utility corpus slice executes and passes.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(range|while|until|repeat|first|last|nth|limit|skip|any|all|combinations|transpose)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC utilities-conformance ===

=== AC utilities-range ===
Intent: Range generation produces values derived from supplied bounds.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(["./jq", "-c", "[range(2;5)]"], input="null\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [2, 3, 4]
=== END AC utilities-range ===

=== AC utilities-limit-skip ===
Intent: Limit and skip select corresponding positions from generated values.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(["./jq", "-c", "[limit(2; .[])]"], input="[4,5,6,7]\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [4, 5]
result = subprocess.run(["./jq", "-c", "[skip(2; .[])]"], input="[4,5,6,7]\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [6, 7]
=== END AC utilities-limit-skip ===

## User Acceptance

- None.

## Guardrails

- Preserve utility generator ordering and multiplicity.
- Implement short-circuiting without evaluating discarded branches.
- Reject unsupported negative limits and skips with runtime errors.
