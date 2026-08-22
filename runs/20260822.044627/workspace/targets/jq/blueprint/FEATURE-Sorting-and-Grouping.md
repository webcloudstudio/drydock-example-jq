# FEATURE: Sorting and Grouping

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq ordering, sorting, grouping, uniqueness, and extrema builtins. |
| Depends On  | FEATURE-Collection-Transforms.md, FEATURE-Truthiness-and-Comparison.md |
| Provides    | sort, sort_by, group_by, unique, unique_by, min, max, min_by, max_by |
| Consumes    | jq comparison semantics, generator evaluation, collection transforms |

## Scope

This feature implements collection ordering according to jq's type order: `null`, booleans, numbers, strings, arrays, and objects. Keyed variants evaluate their filter arguments as ordered generator projections.

## Behavior

- `sort` orders arrays using jq structural ordering.
- `sort_by` orders by one or more generated keys.
- `group_by` sorts and groups equal keys.
- `unique` and `unique_by` remove structural or keyed duplicates.
- `min`, `max`, `min_by`, and `max_by` return extrema, including `null` for empty arrays where jq specifies it.

## Programmatic Acceptance

=== AC data-002-conformance ===
Intent: The authoritative corpus slice containing sorting, grouping, uniqueness, and extrema syntax executes and passes without failures or errors.

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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC data-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Use jq structural comparison rather than Python's boolean-number equivalence.
- Preserve stable ordering for equal generated keys.
- Do not modify files under `sources/`.
