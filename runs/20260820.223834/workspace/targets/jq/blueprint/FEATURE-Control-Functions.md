# FEATURE: Control Functions

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Defines user-defined jq functions, parameters, lexical definitions, and recursion. |
| Depends On | FEATURE-Control-Bindings.md |
| Provides | `def` functions, filter parameters, value parameters, recursion |
| Consumes | lexical bindings, generator evaluation, parser function definitions |

## Purpose

Implement jq function definitions and invocation, preserving filter parameters, value parameters, lexical scope, overloading, closures, generators, and recursion.

## Programmatic Acceptance

=== AC control-functions-conformance ===
Intent: The scoped authoritative corpus cases covering function definitions, parameters, closures, redefinition, and recursion execute and pass.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"^def "
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
=== END AC control-functions-conformance ===

## User Acceptance

- None.

## Guardrails

- Filter arguments must not be eagerly evaluated as values.
- Function scope and redefinition must follow lexical jq semantics.
- Recursive calls must preserve stream ordering and multiplicity.
- No third-party jq implementation or binding may be used.
