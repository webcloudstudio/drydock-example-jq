# FEATURE: Filter Grammar

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse jq filter expressions with the specified composition, precedence, indexing, collection, and operator grammar. |
| Depends On  | FEATURE-Lexer.md, FEATURE-Literals-And-Interpolation.md |
| Provides    | AST grammar for pipes, commas, indexing, slices, arrays, objects, operators, and optionals |
| Consumes    | jq lexer, literal parser, interpreter architecture |

## Scope

The parser shall implement jq expression precedence and associativity for pipes, commas, arithmetic and comparison operators, indexing, slicing, iteration, arrays, objects, unary negation, parentheses, and optional expressions. It shall produce an executable intermediate representation for the evaluator.

## Programmatic Acceptance

=== AC filter-grammar-conformance ===
Intent: The authoritative corpus slice exercising expression punctuation, indexing, collection, and operators executes and passes with no failures or errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\.|\[|\{|\+|\-|\*|/|%"
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
=== END AC filter-grammar-conformance ===

=== AC filter-grammar-runtime-boundary ===
Intent: The selected grammar cases preserve the harness distinction between successful execution and compile rejection.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\.|\[|\{|\+|\-|\*|/|%"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
report = json.loads(result.stdout)
summary = report["summary"]
assert summary["pass"] + summary["fail"] + summary["error"] + summary["skip"] > 0
assert result.returncode == 0
=== END AC filter-grammar-runtime-boundary ===

## User Acceptance

- None.

## Guardrails

- Preserve parser precedence and associativity from `sources/parser.y`.
- Do not reinterpret generator syntax as scalar-only expressions.
- Reject malformed expressions with compile exit status 3.
