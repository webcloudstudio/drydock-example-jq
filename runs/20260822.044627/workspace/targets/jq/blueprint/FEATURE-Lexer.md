# FEATURE: jq Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Tokenizes jq source text into the lexical forms required by the parser and evaluator. |
| Depends On  | ARCHITECTURE.md, FEATURE-Json-IO.md |
| Provides    | jq tokenization |
| Consumes    | interpreter executable boundary |

## Lexical Scope

Implement lexical recognition for:

- JSON literals and numeric forms, including exponent notation.
- Identifiers, field names, variable bindings, and qualified names.
- jq keywords such as `def`, `if`, `reduce`, `try`, `label`, `module`, and `include`.
- Operators including arithmetic, comparison, pipe, comma, alternative, assignment, and optional forms.
- Parentheses, brackets, braces, separators, and delimiters.
- Line comments beginning with `#`, including the source-defined continuation behavior.
- Format tokens beginning with `@`.
- Quoted strings, JSON escapes, and interpolation markers.

The lexer must reject invalid characters and malformed escapes so the parser can report a compile failure with exit code `3`.

## Source Contract

`sources/lexer.l` is the lexical authority. `sources/parser.y` consumes the corresponding token categories. The lexer must not load module files or introduce command-line behavior beyond the fixed `-c` interface.

## Programmatic Acceptance

=== AC parse-001-conformance ===
Intent: Core lexical literals and punctuation compile and execute successfully.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "{true: true, false: false, null: null, number: 1, identity: .}"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual["true"] is True
assert actual["false"] is False
assert actual["null"] is None
assert actual["number"] == 1
assert actual["identity"] is None
=== END AC parse-001-conformance ===

=== AC parse-001-comments-and-keywords ===
Intent: Lexical comments and keyword identifiers remain distinguishable in valid jq source.

import json
import subprocess

program = "{if:0,and:1,or:2,then:3,else:4,elif:5,end:6,as:7,def:8}"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == {
    "if": 0,
    "and": 1,
    "or": 2,
    "then": 3,
    "else": 4,
    "elif": 5,
    "end": 6,
    "as": 7,
    "def": 8,
}
=== END AC parse-001-comments-and-keywords ===

=== AC parse-001-invalid-lexeme ===
Intent: An invalid escape is rejected during compilation with the declared compile-failure status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", '"u\\vw"'],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 3
=== END AC parse-001-invalid-lexeme ===

## User Acceptance

- None.

## Guardrails

- Follow the token categories and delimiter-state behavior defined by `sources/lexer.l`.
- Preserve string escape and interpolation markers for parser consumption.
- Reject malformed escapes and invalid characters at compile time.
- Keep comments out of the token stream.
- Do not modify staged lexical or parser sources.
