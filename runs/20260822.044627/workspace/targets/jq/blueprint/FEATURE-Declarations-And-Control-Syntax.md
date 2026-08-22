# FEATURE: Declarations and Control Syntax

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse jq declarations, control constructs, bindings, module grammar, and destructuring syntax. |
| Depends On  | FEATURE-Filter-Grammar.md |
| Provides    | def, module and import grammar, conditionals, try/catch, reductions, foreach, labels, and patterns |
| Consumes    | jq filter grammar, lexer, interpreter architecture |

## Scope

The front end shall parse function definitions, module and import directives, conditionals, exception flow, reductions, foreach, labels, variable bindings, and destructuring patterns. Module syntax shall be validated sufficiently to reject invalid metadata and paths without loading excluded module fixtures.

## Programmatic Acceptance

=== AC declarations-control-conformance ===
Intent: The authoritative corpus slice exercising declarations, control syntax, bindings, reductions, foreach, labels, and module grammar executes and passes with no failures or errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"%%FAIL|\bif\b|\btry\b|\breduce\b|\bforeach\b|\bdef\b| as |\blabel\b|\bmodule\b|\binclude\b"
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
=== END AC declarations-control-conformance ===

=== AC declarations-compile-rejections ===
Intent: The selected invalid declaration and control programs are rejected as compile failures by the authoritative harness.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"%%FAIL|\bmodule\b|\binclude\b|\blabel\b|\bdef\b"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC declarations-compile-rejections ===

## User Acceptance

- None.

## Guardrails

- Invalid module metadata, import paths, and unresolved labels must fail at compile time.
- Module grammar validation must not access excluded module fixtures.
- Preserve lexical scope and declaration ordering for later evaluation.
