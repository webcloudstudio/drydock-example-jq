# FEATURE: Structural Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provide jq type, collection, containment, ordering, and structural builtins. |
| Depends On  | FEATURE-Assignments.md |
| Provides    | type and structural collection builtins, containment, sorting, grouping, uniqueness, flattening, combinations, transpose, walk |
| Consumes    | assignments, paths, reducers, functions |

## Purpose

Implement jq's standard structural and collection-oriented filters.

## Behavior

Support type selectors, `type`, `length`, `keys`, `keys_unsorted`, `has`, `in`, `inside`, `contains`, `to_entries`, `from_entries`, `with_entries`, `map`, `map_values`, `add`, `sort`, `sort_by`, `group_by`, `unique`, `unique_by`, `min`, `max`, `min_by`, `max_by`, `flatten`, `combinations`, `transpose`, `reverse`, `bsearch`, `walk`, and related structural helpers.

These builtins must preserve jq's type ordering, Unicode key ordering, containment recursion, generator multiplicity, stable grouping semantics, null handling, and specified runtime errors.

## Programmatic Acceptance

=== AC structural-builtins-suite ===
Intent: The implementation passes the authoritative conformance cases for structural and collection builtins.
Suite: scoped

import os
import subprocess
import sys

selector = r"(type|length|keys|has\\(|contains\\(|inside\\(|to_entries|from_entries|with_entries|map\\(|map_values|sort|group_by|unique|flatten|combinations|transpose|walk|bsearch|add)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC structural-builtins-suite ===

=== AC structural-ordering ===
Intent: The implementation passes authoritative cases for jq structural ordering, grouping, uniqueness, and containment.
Suite: scoped

import os
import subprocess
import sys

selector = r"(sort|group_by|unique|contains|inside|bsearch)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC structural-ordering ===

## User Acceptance

- None.

## Guardrails

- Match jq's total ordering across null, booleans, numbers, strings, arrays, and objects.
- Preserve object key semantics and recursive containment.
- Do not silently coerce unsupported input types.
- Preserve generator ordering and multiplicity for all collection filters.
