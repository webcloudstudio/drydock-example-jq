# FEATURE: Functions, Bindings, and Destructuring

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | User-defined functions, lexical bindings, closures, recursion, and destructuring behave according to jq semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-FRONTEND-002.md |
| Provides    | def functions, filter arguments, value arguments, lexical bindings, closures, destructuring |
| Consumes    | jq parser, AST |

## Intent

This capability extends the parsed jq language with executable lexical scope. Functions may accept filter arguments or value arguments, refer to earlier definitions, recurse, and capture bindings. Binding patterns support scalar variables, arrays, objects, and destructuring alternatives.

## Behavior

- `def` definitions are lexically scoped and support zero or more arguments.
- Filter arguments are re-evaluated against the current input; value arguments preserve the evaluated value.
- Bindings are immutable and visible only to the expression on their right.
- Recursive functions and closures preserve generator ordering and backtracking.
- Array and object patterns bind missing values as `null`.
- `?//` tries subsequent destructuring alternatives when an earlier pattern or downstream expression fails.

## Programmatic Acceptance

=== AC frontend-003-functions ===
Intent: The implementation passes the authoritative corpus cases for user-defined functions, arguments, closures, and recursion.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"def |function|closure|recursion|recursive|addvalue|Many arguments|test multiple function arities"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC frontend-003-functions ===

=== AC frontend-003-bindings ===
Intent: The implementation passes the authoritative corpus cases for lexical bindings and destructuring.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"Variables|Destructuring| as \$|closures and lexical scoping|destructuring"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC frontend-003-bindings ===

=== AC frontend-003-alternatives ===
Intent: The implementation passes the authoritative corpus cases for destructuring alternatives and generator backtracking through functions.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"\?//|backtracking through function calls|Destructuring with alternation"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC frontend-003-alternatives ===

## User Acceptance

- None.

## Guardrails

- Do not implement bindings as mutable global variables.
- Do not evaluate filter arguments only once at function definition time.
- Preserve generator multiplicity and lexical scope across recursive calls.
