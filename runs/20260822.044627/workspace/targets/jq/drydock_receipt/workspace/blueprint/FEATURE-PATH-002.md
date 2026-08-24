# FEATURE: Path Access and Mutation Primitives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq nested path access, update, and deletion primitives. |
| Depends On  | FEATURE-PATH-001.md |
| Provides    | getpath, setpath, delpaths |
| Consumes    | path discovery, jq value model |

## Purpose

Implement immutable access and mutation of nested arrays and objects through explicit path arrays.

## Behavior

- `getpath` reads values at supplied paths and returns `null` for absent paths where specified.
- `setpath` creates missing object and array structure and updates existing values.
- `delpaths` removes all requested paths without mutating the original input.
- Multiple path expressions preserve their generator order.
- Invalid path types, negative indices, and excessive path depth produce jq runtime errors or no-ops according to the specification.

## Programmatic Acceptance

=== AC path-002-conformance ===
Intent: The authoritative corpus slice covering getpath, setpath, and delpaths executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"getpath|setpath|delpaths"
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
=== END AC path-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Values remain immutable from the filter author's perspective.
- Do not treat invalid paths as valid object keys or array indices.
- Enforce the supplied depth and indexing semantics.
