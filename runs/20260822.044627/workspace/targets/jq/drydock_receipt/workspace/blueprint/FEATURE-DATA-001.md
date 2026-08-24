# FEATURE: Collection Transformation Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq collection transformation builtins with generator-preserving semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-PATH-004.md |
| Provides    | map, map_values, select, add, flatten, transpose, combinations, walk |
| Consumes    | ordered generator evaluator, assignment operators |

## Workflow

Collection filters transform arrays, objects, and nested values while preserving jq stream ordering and multiplicity. Implement `map`, `map_values`, `select`, `add`, `flatten`, `transpose`, `combinations`, and `walk`, including empty streams, bounded flattening, recursive traversal, and immutable updates.

## Programmatic Acceptance

=== AC data-001-conformance ===
Intent: The collection transformation slice executes matching corpus cases and passes all selected cases.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"map|flatten|transpose|combinations|walk"
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
=== END AC data-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering, multiplicity, backtracking, and immutable-value semantics.
- Use only Python standard-library facilities.
