# FEATURE: Paths Access

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq path discovery and path-based value access. |
| Depends On  | ARCHITECTURE.md, FEATURE-Core-Operators.md |
| Provides    | path, paths, getpath |
| Consumes    | generator evaluator, jq values, jq operators |

## Intent

This feature implements exact and pattern path expressions, path discovery through arrays and objects, filtered recursive paths, and retrieval of values from nested paths including missing values.

## Programmatic Acceptance

=== AC paths-access-conformance ===
Intent: The interpreter passes the authoritative corpus cases covering path discovery and getpath access.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"\b(?:path|paths|getpath)\s*\("
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
=== END AC paths-access-conformance ===

## User Acceptance

- None.

## Guardrails

- Path results must retain traversal order.
- Missing values must follow jq's null and absent-path semantics.
- Invalid path expressions must raise runtime errors with exit status 5.
