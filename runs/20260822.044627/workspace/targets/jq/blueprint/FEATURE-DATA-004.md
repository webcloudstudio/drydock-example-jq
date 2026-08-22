# FEATURE: Index and Membership Utilities

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq index-search, binary-search, quantifier, and SQL-style membership utilities. |
| Depends On  | ARCHITECTURE.md, FEATURE-DATA-003.md |
| Provides    | indices, index, rindex, bsearch, all, any, isempty, IN |
| Consumes    | collection transformations, comparison and generator evaluation |

## Workflow

Implement substring and subarray occurrence searches, first and last index lookup, binary search insertion results, stream-aware `all` and `any`, emptiness detection, and SQL-style `IN` variants. Preserve short-circuiting and Cartesian generator behavior.

## Programmatic Acceptance

=== AC data-004-conformance ===
Intent: The index, membership, quantifier, and emptiness slice executes matching corpus cases and passes all selected cases.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"indices|index\(|rindex|bsearch|any|all|IN\("
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
=== END AC data-004-conformance ===

## User Acceptance

- None.

## Guardrails

- `all` and `any` must short-circuit without consuming unnecessary generator outputs.
- Index utilities must preserve jq's behavior for overlapping matches, empty matches, and insertion points.
