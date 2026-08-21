# FEATURE: Remaining Structural Helpers

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides recursive structural helpers, projections, joins, membership tests, and binary search. |
| Depends On  | FEATURE-BUILTINS-007.md |
| Provides    | walk, pick, INDEX, JOIN, IN, bsearch |
| Consumes    | structural builtins, paths, generators |

## Purpose

Implement the remaining jq structural helpers defined by the manual and reference builtin library.

## Behavior

- `walk(f)` recursively transforms arrays and objects before applying `f`.
- `pick(paths)` projects selected paths while preserving their structure.
- `INDEX` and `JOIN` build and query object indexes from generators.
- `IN` tests membership in a generator or source stream.
- `bsearch(x)` returns an existing index or the encoded insertion point.
- Helpers preserve jq generator ordering and runtime error behavior.

## Programmatic Acceptance

=== AC builtins-008-structural ===
Intent: The authoritative corpus slice covering walk, pick, INDEX, JOIN, IN, and bsearch passes completely.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"walk|pick|INDEX|JOIN|IN\(|bsearch"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC builtins-008-structural ===

=== AC builtins-008-stream-membership ===
Intent: The authoritative corpus slice for stream membership and structural helpers executes non-empty cases without failures.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"INDEX|JOIN|IN\(|bsearch|walk"
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
=== END AC builtins-008-stream-membership ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not shell out to a system jq or use a third-party jq implementation.
- Preserve immutable values, generator ordering, multiplicity, and runtime errors.
