# FEATURE: Core Errors

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Implement jq runtime errors, suppression, alternatives, and partial output. |
| Depends On | FEATURE-Core-Expressions.md |
| Provides | runtime exit status 5, try/catch, optional filters, empty, defined-or |
| Consumes | literals, indexing, construction, and core operators |

## Scope

Runtime failures are distinct from compilation failures and return exit status 5. `try`, `catch`, `?`, `empty`, and `//` preserve jq stream semantics and partial output.

## Programmatic Acceptance

=== AC errors-conformance ===
Intent: The selected error-handling corpus slice executes and passes.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(try|catch|\?|//|error|empty)"
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
=== END AC errors-conformance ===

=== AC errors-runtime-status ===
Intent: An uncaught runtime error returns the runtime-error status.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(["./jq", "-c", "error"], input="null\n", capture_output=True, text=True)
assert result.returncode == 5
assert result.stderr is not None
=== END AC errors-runtime-status ===

=== AC errors-partial-output ===
Intent: Values emitted before a runtime error remain available.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(["./jq", "-c", "1, error"], input="null\n", capture_output=True, text=True)
assert result.returncode == 5
assert [json.loads(line) for line in result.stdout.splitlines()] == [1]
=== END AC errors-partial-output ===

## User Acceptance

- None.

## Guardrails

- Preserve output produced before runtime failure.
- `try` and optional evaluation must suppress only the relevant failure.
- Never convert runtime failures into compile exit status 3.
