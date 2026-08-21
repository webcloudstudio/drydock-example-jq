# FEATURE: Path Discovery and Access

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Defines jq path discovery, path expressions, filtered paths, and path-based reads. |
| Depends On  | FEATURE-CORE-004.md |
| Provides    | path, paths, getpath, path expressions |
| Consumes    | basic filters, generator evaluation |

## Intent

Implement path tracking for exact and generated path expressions, including `path`, `paths`, filtered paths, and `getpath`. Paths are arrays containing object keys and array indices, and path evaluation preserves generator order.

## Behavior

- Exact path expressions produce paths even when intermediate values are absent where jq permits creation.
- Generated path expressions produce paths for existing matching values.
- `paths` excludes the empty root path.
- `getpath` returns the value at the requested path or null for a missing path.
- Invalid path expressions and invalid path components raise jq runtime errors.

## Programmatic Acceptance

=== AC paths-001-conformance ===
Intent: The path discovery and access corpus slice executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"path|paths|getpath"
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC paths-001-conformance ===

=== AC paths-001-missing-and-invalid ===
Intent: The path slice covers missing values and invalid path-expression handling.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"getpath|try path\("
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC paths-001-missing-and-invalid ===

## User Acceptance

- None.

## Guardrails

- Represent paths as JSON arrays of string keys and numeric indices.
- Do not mutate input values during path discovery or access.
- Preserve path ordering and duplicate behavior defined by generator evaluation.
