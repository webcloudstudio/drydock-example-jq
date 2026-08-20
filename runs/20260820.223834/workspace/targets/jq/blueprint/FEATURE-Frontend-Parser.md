# FEATURE: Frontend Parser

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Parses jq programs into executable abstract syntax trees. |
| Depends On | FEATURE-Frontend-Lexer.md |
| Provides | jq AST and filter grammar |
| Consumes | sources/parser.y, sources/lexer.l, sources/jq.test, sources/jq-manual.txt |

## Scope

Implement parser and AST construction for jq precedence and associativity, pipelines, generators, literals, indexing, objects, interpolation, bindings, definitions, modules, conditionals, errors, reductions, labels, and assignments.

## Programmatic Acceptance

=== AC parser-grammar ===
Intent: The parser and dependent frontend execute the corpus slice covering expressions, indexing, construction, grouping, conditionals, bindings, modules, and control syntax.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(\.|\[|\{|\(|if|try|reduce|foreach|def| as |module|include)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC parser-grammar ===

=== AC parser-precedence ===
Intent: The parser preserves jq precedence and associativity for pipelines, commas, arithmetic, comparisons, and assignments.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(\||,|\+|-|\*|/|%|==|!=|<=|>=|=|\|=|\+=|-=|\*=|/=|%=|//)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC parser-precedence ===

## User Acceptance

- None.

## Guardrails

- Keep parser behavior aligned with `sources/parser.y`.
- Module grammar failures must be rejected without filesystem access.
- Do not implement module loading as part of the flat source-import interface.
