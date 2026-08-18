# FEATURE: Functions

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implements jq user-defined functions, parameters, recursion, closures, and lexical scope. |
| Depends On  | FEATURE-Runtime-Errors.md |
| Provides    | def functions, filter parameters, value parameters, recursion, lexical closures |
| Consumes    | jq parser and generator evaluator |

## Intent

Function definitions support zero or more filter or value parameters, lexical visibility, recursive calls, redefinition by arity, closures, and generator backtracking. Filter parameters are evaluated against the current input whenever invoked.

## Programmatic Acceptance

=== AC functions-corpus ===
Intent: The implementation passes conformance cases covering function definitions, parameters, recursion, closures, redefinition, and function backtracking.
Suite: scoped

import os
import subprocess
import sys

selector = r"def |function|closure|recursion|backtracking|arity"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC functions-corpus ===

=== AC functions-definitions ===
Intent: The selected corpus slice executes user-defined zero-argument and parameterized definitions.
Suite: scoped

import os
import subprocess
import sys

selector = r"^def "
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC functions-definitions ===

## User Acceptance

- None.

## Guardrails

- Preserve lexical scoping and definition order.
- Preserve generator multiplicity when invoking filter parameters.
- Recursive calls must retain captured lexical bindings.
