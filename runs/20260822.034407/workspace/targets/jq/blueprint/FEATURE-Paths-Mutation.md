# FEATURE: Paths Mutation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements immutable jq path updates and deletion operations. |
| Depends On  | FEATURE-Paths-Access.md |
| Provides    | setpath, delpaths, del |
| Consumes    | path, paths, getpath |

## Intent

This feature implements nested path creation and replacement, deletion of object fields and array elements or ranges, invalid-path handling, and protection against excessive path depth.

## Programmatic Acceptance

=== AC paths-mutation-conformance ===
Intent: The interpreter passes the authoritative corpus cases covering setpath, delpaths, and del mutation semantics.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"\b(?:setpath|delpaths|del)\s*\(|(?:^|[^\w])del\s*\("
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
=== END AC paths-mutation-conformance ===

## User Acceptance

- None.

## Guardrails

- Updates must be immutable and must not mutate unrelated branches.
- Deletion of missing paths must follow jq semantics.
- Invalid paths and excessive depth must produce runtime errors rather than silent corruption.
