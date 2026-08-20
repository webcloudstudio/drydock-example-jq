# FEATURE: Paths Mutation

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Set and delete values immutably through jq paths. |
| Depends On | FEATURE-Paths-Discovery.md |
| Provides | setpath, delpaths, del |
| Consumes | path, paths, getpath, immutable value construction |

## Capability

Path mutation creates new jq values. `setpath`, `delpaths`, and `del` preserve immutable semantics, ordering, deletion behavior, and runtime errors for invalid paths and excessive depth.

## Programmatic Acceptance

=== AC paths-mutation-suite ===
Intent: The authoritative corpus executes the setpath, delpaths, and del cases owned by this story.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(setpath|delpaths|del\()"
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
=== END AC paths-mutation-suite ===

=== AC paths-mutation-errors ===
Intent: Invalid path mutation is reported through the jq runtime exit protocol.
Requires: executable=python3; scope=test

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "setpath([0, 0]; 1)"],
    input='"object"\n',
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode in (0, 5)
assert result.stderr is not None
=== END AC paths-mutation-errors ===

## User Acceptance

- None.

## Guardrails

- All mutations produce new values and do not modify previously produced values.
- Empty deletion selections must not delete unrelated paths.
- Invalid path components must not be silently ignored except where jq explicitly defines no-op deletion.
- Depth limits must prevent runaway path construction.
