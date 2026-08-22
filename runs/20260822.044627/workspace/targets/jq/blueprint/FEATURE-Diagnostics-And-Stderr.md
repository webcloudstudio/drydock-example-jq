# FEATURE: Diagnostics and Stderr

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implement jq diagnostic, stderr, debug, and halt-error behavior. |
| Depends On  | FEATURE-Process-Contract.md, FEATURE-JSON-IO-Boundary.md, FEATURE-Errors-And-Optional-Evaluation.md |
| Provides    | debug, stderr, halt_error |
| Consumes    | process exit contract, JSON serialization, runtime error flow |

## Intent

Implement `debug`, `stderr`, and `halt_error` with correct output channels, raw diagnostic behavior, exit codes, and partial-output handling. Standard output must contain only filter-produced JSON values.

## Programmatic Acceptance

=== AC io-002-conformance ===
Intent: The implementation passes the authoritative diagnostics and stderr corpus slice.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"debug|stderr|halt_error"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC io-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Diagnostics belong on standard error and must never contaminate JSON output.
- Preserve values emitted before a halt or runtime failure.
- Do not assert or depend on exact diagnostic prose.
