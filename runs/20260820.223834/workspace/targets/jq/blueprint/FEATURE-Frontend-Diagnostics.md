# FEATURE: Front End Diagnostics

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Reject invalid jq programs at compile time with the required exit status. |
| Depends On | FEATURE-Frontend-Parser.md |
| Provides | compile exit status 3 |
| Consumes | jq AST and filter grammar |

## Scope

Compilation failures are distinct from runtime failures. Invalid syntax and other invalid frontend forms are rejected without filesystem access, with diagnostics on standard error.

## Programmatic Acceptance

=== AC diagnostics-conformance ===
Intent: The selected compile-diagnostic corpus slice executes and passes.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(module|include|%::|break|Invalid escape)"
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
=== END AC diagnostics-conformance ===

=== AC diagnostics-exit-code ===
Intent: A syntactically invalid program returns the compile-error exit status.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(["./jq", "-c", "{"], input="null\n", capture_output=True, text=True)
assert result.returncode == 3
assert result.stderr is not None
=== END AC diagnostics-exit-code ===

=== AC diagnostics-runtime-distinction ===
Intent: A syntactically valid program is not classified as a compile failure.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(["./jq", "-c", "error"], input="null\n", capture_output=True, text=True)
assert result.returncode != 3
assert result.stderr is not None
=== END AC diagnostics-runtime-distinction ===

## User Acceptance

- None.

## Guardrails

- Do not read module files while rejecting invalid module grammar.
- Do not shell out to a system jq executable.
- Do not reproduce or compare diagnostic wording.
