# FEATURE: Variable Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides lexical jq value bindings and destructuring scope foundations. |
| Depends On  | FEATURE-Recursive-Generators.md |
| Provides    | as bindings, lexical scope, shadowing, keyword identifiers |
| Consumes    | recursive generator evaluation |

## Workflow

The evaluator binds each output of a left-hand filter to a lexical variable for the following expression. Bindings support nested scopes, shadowing, keyword-shaped names, structural lifetime, and generator backtracking without mutation.

## Programmatic Acceptance

=== AC variable-bindings-scoped ===
Intent: Variable-binding corpus cases execute and pass.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r" as \$|\$[A-Za-z]"
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
=== END AC variable-bindings-scoped ===

=== AC binding-syntax-scoped ===
Intent: Binding and destructuring syntax cases execute and pass.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"\bas\s+\$|\bas\s+\{|\bas\s+\["
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
=== END AC binding-syntax-scoped ===

## User Acceptance

- None.

## Guardrails

- Bindings are immutable and lexically scoped.
- Shadowing must not alter the value visible outside its scope.
- Every generator output must receive its corresponding binding.
