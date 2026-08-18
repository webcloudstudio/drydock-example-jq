# FEATURE: Path Discovery

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provide jq path discovery, path reads, and projection filters. |
| Depends On  | FEATURE-Reducers.md |
| Provides    | path, paths, getpath, pick |
| Consumes    | generator evaluator, indexing, reducers |

## Purpose

Implement jq path expressions and path-oriented read operations over immutable JSON values.

## Behavior

- `path` emits array paths for exact and generated path expressions.
- `paths` emits non-root paths, optionally filtered by a predicate.
- `getpath` reads values at supplied paths and returns null for missing paths where jq specifies it.
- `pick` constructs a projection containing the requested paths.
- Paths preserve object keys and array indices in traversal order.
- Invalid path expressions and invalid path operations raise jq runtime errors.

## Programmatic Acceptance

=== AC path-discovery-suite ===
Intent: The implementation passes the authoritative conformance cases for path discovery.
Suite: scoped

import os
import subprocess
import sys

selector = r"^(path\(|paths(\(|$)|getpath\(|pick\()"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC path-discovery-suite ===

=== AC path-discovery-contract ===
Intent: Path discovery cases execute successfully through the supplied runner.
Suite: scoped

import os
import subprocess
import sys

selector = r"^(path|paths|getpath|pick)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC path-discovery-contract ===

## User Acceptance

- None.

## Guardrails

- Do not mutate the input while discovering or reading paths.
- Preserve generator ordering and distinguish missing paths from invalid path expressions.
