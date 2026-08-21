# FEATURE: Structural and Collection Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides jq structural, collection, sorting, containment, and mapping builtins. |
| Depends On  | FEATURE-CONTROL-003.md, FEATURE-PATHS-003.md |
| Provides    | type, length, keys, has, contains, inside, entries, map, select, map_values, flatten, sort, sort_by, group_by, unique, unique_by, join |
| Consumes    | core filters, generators, path mutation |

## Purpose

Implement the structural and collection builtin family described by the jq manual and reference library.

## Behavior

- Type selectors and `type` report jq value categories.
- `length`, `keys`, `keys_unsorted`, and `has` operate on supported arrays, objects, strings, numbers, and null.
- `map`, `map_values`, and `select` preserve generator semantics and deletion through empty.
- `contains` and `inside` perform recursive structural containment.
- `to_entries`, `from_entries`, and `with_entries` convert and transform objects.
- `flatten`, `sort`, `sort_by`, `group_by`, `unique`, and `unique_by` use jq ordering.
- `join` converts supported scalar elements and treats null as an empty field.

## Programmatic Acceptance

=== AC builtins-001-structure ===
Intent: The authoritative corpus slice exercising types, lengths, keys, containment, entries, and mapping executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"type|length|keys|contains|inside|entries|from_entries|map_values|select"
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
=== END AC builtins-001-structure ===

=== AC builtins-001-collections ===
Intent: The authoritative corpus slice exercising flattening, sorting, grouping, uniqueness, and joining executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"flatten|sort|group_by|unique|join"
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
=== END AC builtins-001-collections ===

## User Acceptance

- None.

## Guardrails

- Match jq's type ordering and structural comparison semantics.
- Preserve object keys and array ordering where the builtin requires it.
- Do not convert unsupported composite values implicitly in `join`.
