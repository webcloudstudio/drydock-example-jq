# FEATURE: Path Discovery

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq path discovery, path filtering, and projection operations. |
| Depends On  | FEATURE-Slices-And-Iteration.md, FEATURE-Destructuring-Patterns.md, FEATURE-Recursive-Generators.md |
| Provides    | path, paths, pick, path projections |
| Consumes    | Accessors, iteration, generator evaluation |

## Purpose

Implement jq's path-oriented filters for discovering, filtering, and projecting nested array and object locations.

## Implementation Requirements

- Implement `path(expression)` for exact and pattern path expressions.
- Implement `paths` and `paths(filter)` with stable traversal order.
- Represent paths as arrays containing string object keys and integer array indexes.
- Exclude the root path from `paths`.
- Implement `pick(path-expressions)` while preserving missing projected fields as `null`.
- Raise runtime errors for invalid path expressions.
- Preserve path behavior through recursive descent and generators.

## Programmatic Acceptance

=== AC path-discovery-conformance ===
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
=== END AC path-discovery-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not emit paths in traversal order different from jq's generator order.
- Do not confuse a projected value with its path representation.
- Do not silently accept invalid path expressions.
