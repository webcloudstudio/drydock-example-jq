# FEATURE: Functions Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq lexical variable bindings, destructuring patterns, and destructuring alternatives. |
| Depends On  | ARCHITECTURE.md, FEATURE-Control-Recursion.md |
| Provides    | lexical variables, bindings, array/object patterns, ?// destructuring |
| Consumes    | jq AST, generator evaluator, control flow |

## Behavior

`as` binds each generated value lexically while preserving the original input for the continuation. Bindings are immutable and scoped to the remainder of their expression. Array and object patterns bind matching fields and use `null` for absent array positions or fields as jq specifies. `?//` tries destructuring alternatives with backtracking and exposes the resulting bindings to the continuation.

## Programmatic Acceptance

=== AC functions-bindings-suite ===
Intent: Execute conformance cases covering lexical bindings, variable scope, and array/object destructuring.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

select = r" as \\$|\\. as \\[|\\. as \\{"
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
=== END AC functions-bindings-suite ===

=== AC functions-alternation-suite ===
Intent: Execute conformance cases covering destructuring alternative backtracking.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

assert Path("jq").is_file()

select = r"\\?//"
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
=== END AC functions-alternation-suite ===

## User Acceptance

- None.

## Guardrails

- Variable scope must not leak outside its lexical expression.
- Each generated binding value must run the continuation with the original input.
- Failed destructuring alternatives must backtrack without leaking partial bindings.
