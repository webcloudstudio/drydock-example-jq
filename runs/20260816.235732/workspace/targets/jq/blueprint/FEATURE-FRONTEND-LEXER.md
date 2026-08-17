# FEATURE: Front End Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | jq lexical analyzer for literals, identifiers, strings, operators, comments, formats, and delimiters. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-FOUNDATION.md |
| Provides    | jq tokenizer |
| Consumes    | interpreter module boundaries |

## Scope

The lexer converts jq source text into parser tokens while preserving source locations. It recognizes JSON-compatible literals, identifiers, field selectors, variable bindings, quoted strings, interpolation boundaries, formats, comments, operators, delimiters, and module-related keywords.

Invalid escapes, invalid characters, mismatched delimiters, and malformed lexical forms must be reported as compile errors through the CLI contract.

## Token Categories

- Literals: integers, decimals, exponents, strings, booleans, and null.
- Names: identifiers, field names, qualified names, and `$` bindings.
- Operators: arithmetic, comparison, assignment, alternatives, pipes, commas, and suffix markers.
- Structures: parentheses, brackets, braces, and interpolation delimiters.
- Formats: `@text`, `@json`, `@csv`, `@tsv`, `@uri`, `@html`, `@sh`, `@base64`, and related format names.
- Comments: `#` through the line ending, including documented continuation behavior.

## Programmatic Acceptance

=== AC lexer-literals ===
Intent: Lexically valid literal and format tokens are accepted through the executable boundary and preserve their supplied values.

import json
import subprocess

literal = "alpha"
program = f'"{literal}"'
expected = json.dumps(literal, separators=(",", ":")) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert result.stdout == expected
=== END AC lexer-literals ===

=== AC lexer-interpolation ===
Intent: String interpolation lexical boundaries are accepted and produce a value derived from supplied input.

import json
import subprocess

value = 7
program = '"value=\\(.)"'
expected_value = f"value={value}"
expected = json.dumps(expected_value, separators=(",", ":")) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert result.stdout == expected
=== END AC lexer-interpolation ===

=== AC lexer-comments-and-operators ===
Intent: Comments and operator tokens are ignored or recognized without changing the evaluated result.

import json
import subprocess

value = 2
program = "1 + . # trailing comment"
expected_value = value + 1
expected = json.dumps(expected_value, separators=(",", ":")) + "\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert result.stdout == expected
=== END AC lexer-comments-and-operators ===

=== AC lexer-invalid-escape ===
Intent: An invalid string escape is rejected as a compile error.

import subprocess

result = subprocess.run(
    ["./jq", "-c", '"u\\vw"'],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 3
=== END AC lexer-invalid-escape ===

## User Acceptance

- None.

## Guardrails

- Do not reinterpret invalid lexical forms as runtime errors.
- Preserve source locations sufficiently for compile diagnostics.
- Do not modify the supplied lexer or parser reference assets.
