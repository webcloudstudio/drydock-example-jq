# FEATURE: Sorting And Grouping

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq structural sorting, grouping, uniqueness, and extremum builtins. |
| Depends On  | FEATURE-Truthiness-And-Comparison.md, FEATURE-Collection-Transformations.md |
| Provides    | sort, sort_by, group_by, unique, unique_by, min, max, min_by, max_by |
| Consumes    | comparison and ordering semantics, collection transformations |

## Workflow

Implement structural ordering across jq values, including null, booleans, numbers, strings, arrays, and objects. Implement keyed sorting and grouping, duplicate removal, and minimum/maximum selection. Filter arguments may produce multiple values and must be compared in jq's prescribed lexicographic order.

## Programmatic Acceptance

=== AC data-002-conformance ===
Intent: The authoritative corpus slice covering sorting, grouping, uniqueness, and extrema executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"sort|group_by|unique|min|max"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
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
=== END AC data-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Equality and ordering must remain consistent with jq numeric equivalence.
- Object key order must not affect structural equality.
- Preserve stable output ordering where the jq semantics require it.
