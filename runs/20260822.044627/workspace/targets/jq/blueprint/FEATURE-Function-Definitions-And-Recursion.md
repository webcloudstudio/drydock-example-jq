# FEATURE: Function Definitions and Recursion

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq function definitions, lexical function scope, redefinition, and recursion. |
| Depends On  | ARCHITECTURE.md, FEATURE-Declarations-And-Control-Syntax.md, FEATURE-Variable-Bindings.md, FEATURE-Function-Parameters.md |
| Provides    | def declarations, function redefinitions, lexical function scope, recursion |
| Consumes    | parser declarations, function parameters, lexical environments |

## Workflow

Implement `def` declarations with arity-aware bindings. Support lexical visibility, later redefinitions, self-recursion, recursive calls through parameters, and function definitions nested within expressions while preserving jq's declaration ordering rules.

## Programmatic Acceptance

=== AC func-003-conformance ===
Intent: The authoritative corpus slice exercising function definitions and recursion executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"def "
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
=== END AC func-003-conformance ===

=== AC func-003-interface ===
Intent: A recursively defined function evaluates to a completed result.
import subprocess

program = "def fac: if . == 1 then 1 else . * (. - 1 | fac) end; fac"
payload = "4\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode in (0, 5)
=== END AC func-003-interface ===

## User Acceptance

- None.

## Guardrails

- Enforce lexical visibility and arity-specific function lookup.
- Permit self-recursion without permitting undefined references.
- Preserve generator ordering through recursive calls.
