# FEATURE: User-Defined Functions and Lexical Scope

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Support jq function definitions, arguments, recursion, closures, and lexical scope. |
| Depends On  | FEATURE-FRONTEND-003.md, FEATURE-CORE-001.md |
| Provides    | def functions, filter arguments, value arguments, closures, recursion, lexical scope |
| Consumes    | jq parser, AST evaluator, generator runtime |

## Scope

Implement arity-sensitive `def` declarations and calls, filter and value arguments, recursive definitions, redefinition, closures, and lexical visibility for functions and variables.

## Programmatic Acceptance

=== AC frontend-004-definitions ===
Intent: The implementation passes the executing conformance cases containing user-defined function definitions.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"^def "
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
=== END AC frontend-004-definitions ===

=== AC frontend-004-scope-and-recursion ===
Intent: The implementation passes executing function cases covering arguments, closures, and recursion.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"^def |closure|recursion|recursive"
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
=== END AC frontend-004-scope-and-recursion ===

## User Acceptance

- None.

## Guardrails

- Function arguments must retain jq filter-versus-value argument semantics.
- Function and variable bindings must remain lexically scoped.
- Preserve generator ordering and multiplicity through function calls.
