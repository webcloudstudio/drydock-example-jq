# FEATURE: Frontend Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines lexical analysis for jq programs. |
| Depends On  | ARCHITECTURE.md |
| Provides    | jq tokenizer |
| Consumes    | interpreter architecture |

## Lexical Contract

The lexer recognizes:

- JSON-like literals, including numeric literals and escaped strings.
- Identifiers, field selectors, variable bindings, and qualified names.
- jq keywords such as `if`, `then`, `else`, `def`, `reduce`, `try`, and `label`.
- Operators including pipes, commas, arithmetic, comparisons, assignments, alternatives, and recursion.
- Format tokens beginning with `@`.
- String interpolation using `\( ... )`.
- Nested delimiters and comments beginning with `#`.
- Invalid characters and malformed escapes as lexer errors.

Whitespace is ignored outside strings. String escapes follow jq's JSON-compatible escape rules, and comments continue according to the supplied lexer specification.

## Programmatic Acceptance

=== AC lexer-literals ===
Intent: The lexer and parser accept literals, fields, bindings, and operators used by jq programs.

import json
import subprocess

program = "{value: .foo, copy: $x} | .value + .copy"
input_value = {"foo": 2}
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC lexer-literals ===

=== AC lexer-strings ===
Intent: The lexer accepts escaped strings and string interpolation.

import json
import subprocess

program = '"value=\\(.)"'
input_value = "x"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = "value=" + input_value
assert actual == [expected]
=== END AC lexer-strings ===

=== AC lexer-comments ===
Intent: Comments are ignored without changing the surrounding jq program.

import json
import subprocess

program = "1 # comment\n + 1"
input_value = None
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = 1 + 1
assert actual == [expected]
=== END AC lexer-comments ===

## User Acceptance

- None.

## Guardrails

- Lexical behavior follows `sources/lexer.l`.
- Invalid characters and malformed escapes must not be silently accepted.
- Comment markers inside strings are ordinary string content.
- Lexer output must preserve source ordering and provide the parser with stable token boundaries.
