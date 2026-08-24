# FEATURE: Sorting and Grouping Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq sorting, grouping, uniqueness, and extrema builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-DATA-001.md |
| Provides    | sort, sort_by, group_by, unique, unique_by, min, max, min_by, max_by |
| Consumes    | jq comparison and ordering |

## Workflow

Implement collection ordering according to jq's total value ordering: null, booleans, numbers, strings, arrays, and objects. Support key-generating filters, grouping, duplicate removal, minimum, maximum, and keyed extrema while retaining generator-derived key ordering.

## Programmatic Acceptance

=== AC data-002-conformance ===
Intent: The sorting, grouping, uniqueness, and extrema slice executes matching corpus cases and passes all selected cases.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"sort|group_by|unique|min|max"
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
=== END AC data-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Comparisons must follow jq's structural type ordering and numeric equivalence.
- Keyed operations must evaluate their filter arguments with jq generator semantics.
