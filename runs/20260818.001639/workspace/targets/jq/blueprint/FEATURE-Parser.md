# FEATURE: Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Parse jq programs into executable abstract syntax trees with jq-compatible precedence and grammar. |
| Depends On  | FEATURE-Lexer.md |
| Provides    | jq parser and AST |
| Consumes    | jq lexer |

## Purpose

The parser converts the token stream produced by the jq lexer into executable AST structures. It must preserve jq's precedence, associativity, generator composition, and lexical scoping rules.

## Supported grammar

The parser covers:

- Queries, pipelines, comma generators, parenthesized expressions, and comments.
- Literals, strings, interpolation, formats, identity, field access, indexing, iteration, and slices.
- Arrays, objects, computed keys, shorthand keys, optional expressions, and recursive descent.
- Arithmetic, comparison, boolean, defined-or, and assignment operators.
- `if`/`elif`/`else`, `try`/`catch`, `label`/`break`, `reduce`, and `foreach`.
- Function definitions, function arguments, variable bindings, destructuring patterns, and `?//`.
- Module, import, and include syntax sufficiently for later validation.

The AST must retain enough source and operator information for compile-time validation and generator-based evaluation.

## Programmatic Acceptance

=== AC parser-corpus-slice ===
Intent: The parser and AST execute the parser-oriented corpus slice covering literals, constructors, field access, indexing, arrays, objects, and function syntax.
Suite: scoped

import os
import subprocess
import sys

selector = r"^(true|false|null|-?[0-9]|\.|\[|\{|def )"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC parser-corpus-slice ===

=== AC parser-rejects-malformed ===
Intent: A syntactically malformed jq program is rejected with the declared compile exit status.
import subprocess

program = "{"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC parser-rejects-malformed ===

## User Acceptance

- None.

## Guardrails

- Do not evaluate filters during parsing.
- Preserve generator ordering and operator associativity in the AST.
- Do not shell out to a system jq implementation.
- Use only the Python standard library.
