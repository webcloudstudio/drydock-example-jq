# FEATURE: jq Filter Expression Grammar

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse jq expressions with precedence, composition, accessors, collections, and operators. |
| Depends On  | ARCHITECTURE.md, FEATURE-PARSE-002.md |
| Provides    | expression AST, precedence, pipes, commas, indexing, slicing, arrays, objects, operators |
| Consumes    | jq lexer and token stream |

## Scope

Implement the expression grammar and AST for pipes, commas, parentheses, unary operators, binary operators, field and index access, iteration, slices, arrays, objects, optional expressions, and assignment syntax. Operator precedence and associativity must follow `sources/parser.y`.

## Programmatic Acceptance

=== AC parse-003-conformance ===
Intent: The executable passes every selected corpus case exercising expression punctuation, accessors, collections, and operators.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"\.|\[|\{|\+|\-|\*|/|%"
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
=== END AC parse-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve parser precedence and generator-producing expression structure.
- Reject malformed delimiters and invalid object-key expressions at compile time.
- Do not modify the supplied grammar or corpus.
