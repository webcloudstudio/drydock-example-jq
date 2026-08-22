# FEATURE: Functions Definitions

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq user-defined functions, parameters, lexical function scope, and recursive calls. |
| Depends On  | FEATURE-Functions-Bindings.md |
| Provides    | def declarations, filter arguments, value arguments, recursion, function scope |
| Consumes    | variables and destructuring, jq AST, generator evaluator |

## Behavior

`def` declares functions by name and arity. Regular parameters receive filters, binding parameters receive values, and arguments may generate multiple outputs. Definitions are lexically scoped, later definitions replace earlier definitions for subsequent references, and functions may recurse. Calls preserve generator backtracking through arguments and function bodies.

## Programmatic Acceptance

=== AC functions-definitions-suite ===
Intent: Execute conformance cases covering user-defined functions, arity, parameters, scope, and redefinition.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC functions-definitions-suite ===

=== AC functions-recursion-suite ===
Intent: Execute conformance cases covering recursive user-defined functions and generator backtracking through calls.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r"def .*fac|def .*recurse|def .*\\("
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC functions-recursion-suite ===

## User Acceptance

- None.

## Guardrails

- Function arity and parameter kinds must be enforced at compile time.
- Function arguments remain filters unless declared as value bindings.
- Recursive calls must preserve generator ordering and lexical scope.
