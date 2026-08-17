# FEATURE: Flow Functions

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides user-defined jq functions, parameters, recursion, and lexical closures. |
| Depends On  | FEATURE-Flow-Bindings.md |
| Provides    | def functions, filter arguments, value arguments, arity, closures, recursion |
| Consumes    | lexical bindings |

## Purpose

Implement `def` declarations and calls with filter parameters, value parameters, multiple arities, lexical function scope, redefinition, recursion, and closures. Function arguments must retain jq's filter-versus-value semantics.

## Programmatic Acceptance

=== AC flow-functions-suite ===
Intent: The implementation passes the conformance cases for user-defined functions and function arguments.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"\bdef\b|function|closure|arity|argument"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-functions-suite ===

=== AC flow-recursive-functions ===
Intent: The implementation passes conformance cases for recursive function calls and function redefinition.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"recursion|recursive|redefinition|def f|def g"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC flow-recursive-functions ===

## User Acceptance

- None.

## Guardrails

- Function parameters must preserve filter and value argument distinctions.
- Function scope and redefinition must remain lexical and arity-specific.
- Recursive calls must preserve generator ordering and terminate when the filter terminates.
