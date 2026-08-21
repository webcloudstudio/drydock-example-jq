# FEATURE: Compile-Time Rejection and Static Validation

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Reject invalid jq programs during compilation with exit status 3. |
| Depends On  | FEATURE-FRONTEND-002.md |
| Provides    | compile-time validation, exit status 3 |
| Consumes    | jq parser and AST |

## Scope

The compiler rejects malformed syntax, invalid module declarations, undefined bindings and labels, invalid object keys, and other static errors. Compile failures write diagnostics to standard error and return status 3 without evaluating the program.

## Programmatic Acceptance

=== AC frontend-003-module-errors ===
Intent: The implementation passes the executing conformance cases for invalid module syntax.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"module|include|%::|^\{|^\}"
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
=== END AC frontend-003-module-errors ===

=== AC frontend-003-static-errors ===
Intent: The implementation passes the executing conformance cases for undefined symbols and invalid syntax.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"break|as \$foo|^\.$|^\}"
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
=== END AC frontend-003-static-errors ===

## User Acceptance

- None.

## Guardrails

- Do not shell out to a system jq executable.
- Do not accept runtime failure as a substitute for compile-time rejection.
- Preserve exit status 3 for compile failures.
