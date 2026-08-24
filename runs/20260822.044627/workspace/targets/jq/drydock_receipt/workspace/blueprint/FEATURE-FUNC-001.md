# FEATURE: Lexical Variable Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq lexical value bindings and variable lookup. |
| Depends On  | ARCHITECTURE.md, FEATURE-FLOW-006.md |
| Provides    | as bindings, variable lookup, lexical scope, shadowing |
| Consumes    | generator evaluator, parser AST |

## Workflow

Bindings evaluate the left-hand filter as a generator, bind each produced value lexically, and run the remainder of the expression with the original input and the active binding environment.

- `EXP as $name | REST` supports multiple generated bindings.
- Bindings are immutable and lexically scoped.
- Nested bindings may shadow outer names without mutating them.
- Keyword identifiers may be used as binding names.
- Array and object patterns bind missing members as `null`.

## Programmatic Acceptance

=== AC func-001-conformance ===
Intent: The executable passes the authoritative conformance cases exercising lexical bindings and variable lookup.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r" as \$|\$[A-Za-z]"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
tally = report["summary"]
assert sum(tally.values()) > 0
assert tally["fail"] == 0 and tally["error"] == 0
assert result.returncode == 0
=== END AC func-001-conformance ===

## User Acceptance

- Variable values remain available only within their lexical scope and preserve generator backtracking.

## Guardrails

- Do not implement bindings as mutable global variables.
- Do not leak nested or out-of-scope bindings.
