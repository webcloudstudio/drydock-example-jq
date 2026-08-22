# FEATURE: jq Declarations and Control Syntax

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse jq declarations, bindings, control constructs, and module grammar. |
| Depends On  | ARCHITECTURE.md, FEATURE-PARSE-003.md |
| Provides    | declarations, conditionals, try/catch, reductions, foreach, labels, bindings, modules grammar |
| Consumes    | expression AST |

## Scope

Implement parsing for `def`, function parameters, `as` bindings, destructuring patterns, `if`/`elif`/`else`, `try`/`catch`, `reduce`, `foreach`, `label`/`break`, and module directives. Module syntax must be validated sufficiently to reject invalid metadata, interpolation in import paths, invalid escapes, and unsupported tokens without loading module files.

## Programmatic Acceptance

=== AC parse-004-conformance ===
Intent: The executable passes every selected corpus case covering declarations, control syntax, bindings, reductions, labels, and required compile failures.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"%%FAIL|if |try |reduce |foreach |def | as |label |module|include"
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC parse-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Compile failures must exit 3 and runtime failures must remain distinct.
- Do not resolve imports or read excluded module fixtures in this story.
- Preserve lexical scope and syntax needed by later evaluator stories.
