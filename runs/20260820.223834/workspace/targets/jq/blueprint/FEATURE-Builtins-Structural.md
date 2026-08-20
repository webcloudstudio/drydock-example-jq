# FEATURE: Builtins Structural

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Defines jq's collection, structural, mapping, ordering, and containment builtins. |
| Depends On | FEATURE-Control-Functions.md |
| Provides | type predicates, collection builtins, mapping, sorting, grouping, uniqueness, entries, walking |
| Consumes | generator evaluation, functions, paths, immutable values |

## Purpose

Implement structural and collection builtins specified by the jq manual and reference builtin definitions, preserving jq ordering, generator multiplicity, and immutable values.

## Programmatic Acceptance

=== AC builtins-structural-conformance ===
Intent: The scoped authoritative corpus cases covering structural and collection builtins execute and pass.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(map|sort|group_by|unique|entries|flatten|contains|inside|walk|keys|length)"
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
=== END AC builtins-structural-conformance ===

## User Acceptance

- None.

## Guardrails

- Builtins must preserve generator multiplicity and ordering.
- Structural comparisons must distinguish booleans from numbers.
- Mapping and deletion behavior must preserve jq's immutable-value semantics.
- No third-party runtime dependency may be introduced.
