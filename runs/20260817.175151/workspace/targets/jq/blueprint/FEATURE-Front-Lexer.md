# FEATURE: Front Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines lexical recognition of jq source text. |
| Depends On  | FEATURE-CLI-Entrypoint.md |
| Provides    | jq lexer |
| Consumes    | executable jq |

## Intent

The front end tokenizes jq literals, identifiers, field names, variable bindings, operators, delimiters, comments, format tokens, quoted strings, escapes, and string interpolation. It preserves sufficient source-location information for diagnostics and rejects invalid lexical forms at compilation.

## Programmatic Acceptance

=== AC front-lexer-basic-tokens ===
Intent: Lexically valid literals, fields, bindings, operators, and delimiters are accepted by the executable.

import os
import subprocess

program = '.foo + $value | [., "text", @json]'
result = subprocess.run(
    ["./jq", "-c", program],
    input='{"foo": 2}\n',
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 3 or result.returncode == 0
=== END AC front-lexer-basic-tokens ===

=== AC front-lexer-comments-interpolation ===
Intent: Comments and string interpolation are accepted as jq lexical forms.

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", '"value=\\(.) # trailing comment'],
    input="7\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 0
=== END AC front-lexer-comments-interpolation ===

=== AC front-lexer-invalid-escape ===
Intent: An invalid string escape is rejected during compilation.

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", '"u\\vw"'],
    input="null\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 3
=== END AC front-lexer-invalid-escape ===

## User Acceptance

- None.

## Guardrails

- Lexing must follow the supplied lexer specification and must not shell out to another jq implementation.
- Invalid escapes and invalid characters must not be silently accepted as valid source.
