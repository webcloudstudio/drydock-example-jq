# FEATURE: Language Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implements jq variables, destructuring, user-defined functions, closures, and lexical scoping. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-CONTROL.md |
| Provides    | jq bindings, patterns, user-defined functions, lexical closures |
| Consumes    | generator evaluator, jq control flow |

## Scope

Implement `as` bindings, scalar variables, array and object destructuring, `?//` alternatives, user-defined functions and parameters, recursive definitions, closures, lexical scope, and generator-valued function arguments.

Bindings must be immutable and scoped over the remainder of their expression. Function arguments must remain filters when declared as regular parameters and values when declared as binding parameters.

## Programmatic Acceptance

=== AC bindings-and-patterns ===
Intent: The authoritative corpus passes scalar bindings, array/object destructuring, and destructuring alternatives.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r" as \$|^\.\s+as |^\.\[\]\s+as |^\.\s+as \[|^\.\s+as \{"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC bindings-and-patterns ===

=== AC functions-and-closures ===
Intent: The authoritative corpus passes user-defined functions, recursion, closures, and generator-valued arguments.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^def |^def .*;.*def |closures|recursion|backtracking"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC functions-and-closures ===

=== AC binding-compile-errors ===
Intent: Undefined variables and malformed binding patterns are rejected at compile time.

import subprocess

undefined = subprocess.run(
    ["./jq", "-c", ". as $x | $missing"],
    input="null\n",
    capture_output=True,
    text=True,
)
malformed = subprocess.run(
    ["./jq", "-c", ". as [] | null"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert undefined.returncode == 3
assert malformed.returncode == 3
=== END AC binding-compile-errors ===

## User Acceptance

- None.

## Guardrails

- Preserve lexical scope and immutable bindings.
- Preserve generator-valued function argument semantics.
- Reject undefined variables and invalid destructuring at compile time.
