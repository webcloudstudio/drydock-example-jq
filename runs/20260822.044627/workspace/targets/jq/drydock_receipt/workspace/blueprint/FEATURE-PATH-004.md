# FEATURE: Complex Assignment Edge Cases

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Completes jq assignment behavior for iterated, invalid, and deep paths. |
| Depends On  | FEATURE-PATH-003.md |
| Provides    | iterated assignment, empty updates, array expansion, invalid and deep paths |
| Consumes    | deletion and assignment operators |

## Purpose

Handle complex assignment cases involving iterated paths, empty updates, array expansion, invalid indices, NaN indices, string slices, and depth limits.

## Behavior

- Assignments through iterated and filtered paths update every selected location in jq order.
- Empty updates remove selected array or object members.
- Assignments beyond an array's current length expand it with `null` values where specified.
- Negative, fractional, and NaN indices follow jq's access and mutation rules.
- String slices cannot be updated when jq forbids string mutation.
- Path, containment, comparison, serialization, and merge depth limits are enforced.

## Programmatic Acceptance

=== AC path-004-conformance ===
Intent: The authoritative corpus slice covering complex assignment edge cases executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"negative|NaN|depth|empty"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC path-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Reject invalid mutations with runtime errors rather than corrupting values.
- Preserve partial output before runtime failure.
- Enforce documented depth limits without recursion runaway.
