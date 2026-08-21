# FEATURE: jq Expression Parser and AST

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Parses jq expressions into an evaluable AST with jq-compatible precedence and syntax. |
| Depends On  | FEATURE-FRONTEND-001.md |
| Provides    | jq parser and AST |
| Consumes    | jq lexer |

## Scope

The parser builds the internal representation for jq expressions, including precedence and associativity, pipelines and generators, suffix access and slices, arrays and objects, conditionals, errors, assignments, reductions, function definitions, bindings, destructuring forms, and module grammar. It preserves the distinction between compile-time syntax errors and runtime evaluation.

## Programmatic Acceptance

=== AC parser-conformance-slice ===
Intent: The executable passes the non-empty conformance slice exercising parser constructs covered by the frontend gate.

import json
import os
import subprocess
import sys

SELECT = r'^(\\.|\\[|\\{|def|if|try|reduce|foreach|module|include|%::|"|@)'

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
=== END AC parser-conformance-slice ===

=== AC parser-precedence ===
Intent: The parser preserves jq arithmetic precedence and grouping in a runnable expression.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "1+2*2+10/2"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = 10
assert actual == [expected]
=== END AC parser-precedence ===

=== AC parser-compile-rejection ===
Intent: The parser rejects an unterminated collection at compile time.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC parser-compile-rejection ===

## User Acceptance

- Parser behavior follows the supplied `sources/parser.y` grammar and the jq manual.

## Guardrails

- Preserve generator-producing syntax and downstream evaluation structure in the AST.
- Keep compile-time rejection distinct from runtime failure.
