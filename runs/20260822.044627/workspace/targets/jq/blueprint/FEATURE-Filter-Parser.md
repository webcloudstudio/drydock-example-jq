# FEATURE: Filter Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse jq filter expressions, precedence, accessors, collections, and operators. |
| Depends On  | FEATURE-Strings-and-Interpolation-Parser.md |
| Provides    | AST for pipes, commas, precedence, indexing, slices, arrays, objects, operators |
| Consumes    | jq tokenization |

## Programmatic Acceptance

=== AC parse-003-expression-grammar ===
Intent: Expression grammar and precedence execute successfully.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["./jq", "-c", ". + 2 * 3"],
    input="4\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout.splitlines() == ["10"]

literal = subprocess.run(
    ["./jq", "-c", "[.foo, .bar]"],
    input='{"foo":1,"bar":2}\n',
    capture_output=True,
    text=True,
)
assert literal.returncode == 0
assert literal.stdout.splitlines() == ["[1,2]"]
=== END AC parse-003-expression-grammar ===

=== AC parse-003-composition-syntax ===
Intent: Collection, object, indexing, and composition syntax execute successfully.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["./jq", "-c", ".items | .[0]"],
    input='{"items":["a","b"]}\n',
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout.splitlines() == ['"a"']

composed = subprocess.run(
    ["./jq", "-c", "[.a, .b]"],
    input='{"a":1,"b":2}\n',
    capture_output=True,
    text=True,
)
assert composed.returncode == 0
assert composed.stdout.splitlines() == ["[1,2]"]
=== END AC parse-003-composition-syntax ===

## User Acceptance

- None.

## Guardrails

- Follow the precedence and associativity specified by `sources/parser.y`.
- Preserve generator-valued expressions in the AST.
- Do not modify files under `sources/`.
