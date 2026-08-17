# FEATURE: Front End Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Parses jq programs into executable abstract syntax trees with jq-compatible precedence and syntax. |
| Depends On  | ARCHITECTURE.md, FEATURE-FRONTEND-LEXER.md |
| Provides    | jq parser, executable AST |
| Consumes    | jq tokenizer |

## Purpose

The parser converts the token stream into an executable AST. It must preserve jq's grammar, operator precedence, associativity, generator composition, lexical definitions, and source-aware compile failures.

## Scope

Support literals, strings and interpolation, field and array access, slices, arrays, objects, pipes, commas, arithmetic and comparison operators, conditionals, alternatives, try/catch, definitions, bindings, reductions, assignments, labels, modules, and formats. Reject malformed syntax with exit code 3.

The parser must expose a stable AST contract to the evaluator. AST nodes represent filters rather than single values, and argument expressions remain generator-valued until evaluation.

## Programmatic Acceptance

=== AC parser-valid-programs ===
Intent: The parser accepts representative valid jq programs and the conformance runner reports success for the parser-owned corpus slice.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^(\.foo|\.|\[\.|def |if |reduce |foreach |try |@)"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC parser-valid-programs ===

=== AC parser-invalid-programs ===
Intent: Invalid jq syntax is rejected with the documented compile-error status.

import json
import subprocess

program = "{"
payload = "null\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC parser-invalid-programs ===

=== AC parser-precedence ===
Intent: Parsed arithmetic precedence and grouping are accepted by the authoritative corpus.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"1\+1|1 \+ 2 \* 2|16 / 4"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC parser-precedence ===

## User Acceptance

- None.

## Guardrails

- Do not shell out to a jq implementation.
- Preserve compile exit code 3 and send diagnostics to stderr.
- Do not modify supplied lexer, parser, corpus, or harness assets.
