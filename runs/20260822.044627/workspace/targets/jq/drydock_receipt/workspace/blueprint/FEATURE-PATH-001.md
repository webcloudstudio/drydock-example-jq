# FEATURE: Path Discovery and Projection

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq path discovery and projection filters. |
| Depends On  | FEATURE-FUNC-004.md |
| Provides    | path, paths, pick |
| Consumes    | field and index access, recursive generators, destructuring |

## Purpose

Implement filters that discover paths through JSON values and construct projections from selected paths.

## Behavior

- `path` emits path arrays for exact and filtered path expressions.
- `paths` emits non-empty paths to values, optionally filtered by a predicate.
- Recursive descent preserves traversal order.
- `pick` creates a projection containing the requested paths and preserves missing branches as `null` where jq specifies.
- Invalid path expressions raise runtime errors.

## Programmatic Acceptance

=== AC path-001-conformance ===
Intent: The authoritative corpus slice covering path discovery and projection executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"path\(|paths|pick\("
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
=== END AC path-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Path arrays contain only valid string keys and numeric indices.
- Path discovery must preserve generator ordering and multiplicity.
- Projection and discovery must not mutate the source value.
