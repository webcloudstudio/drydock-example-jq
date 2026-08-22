# FEATURE: Path Primitives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines nested path lookup, creation, replacement, and deletion primitives. |
| Depends On  | FEATURE-Path-Discovery.md, FEATURE-Field-And-Index-Access.md |
| Provides    | getpath, setpath, delpaths |
| Consumes    | Path discovery, immutable value model |

## Purpose

Implement jq's primitive operations for reading, setting, and deleting values at nested paths.

## Implementation Requirements

- Implement `getpath(paths)` for one or more paths.
- Implement `setpath(path; value)` with nested object and array creation.
- Implement `delpaths(paths)` for multiple nested deletions.
- Preserve immutable input values and return updated copies.
- Handle missing object fields and array positions according to jq semantics.
- Reject invalid path component types and invalid array operations with runtime errors.
- Enforce path depth limits required by the corpus.

## Programmatic Acceptance

=== AC path-primitives-conformance ===
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
=== END AC path-primitives-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not mutate values aliased by another expression.
- Do not convert invalid paths into silent no-ops except where jq specifies that behavior.
- Do not bypass the path depth limit.
