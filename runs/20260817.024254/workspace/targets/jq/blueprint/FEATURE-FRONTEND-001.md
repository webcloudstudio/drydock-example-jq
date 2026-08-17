# FEATURE: jq Lexical Analysis

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines lexical analysis for jq programs, including literals, bindings, strings, and operators. |
| Depends On  | ARCHITECTURE.md |
| Provides    | jq tokenization |
| Consumes    | interpreter module boundaries |

## Lexical Scope

The lexer recognizes:

- JSON-like literals, identifiers, field names, and variable bindings.
- Keywords including `def`, `if`, `then`, `else`, `end`, `as`, `reduce`, `foreach`, `try`, `catch`, `label`, and `break`.
- Operators including arithmetic, comparison, Boolean, alternative, assignment, and recursive-descent operators.
- Delimiters for parentheses, arrays, objects, and interpolated strings.
- `@format` tokens.
- Double-quoted strings with JSON escapes and `\(filter)` interpolation.
- `#` comments, including escaped line continuations.
- Invalid escapes, characters, and mismatched delimiters as lexical errors.

Source locations must be retained sufficiently for diagnostics such as line and column reporting.

## Programmatic Acceptance

=== AC frontend-001-literals-and-fields ===
Intent: Lexically valid literals, fields, and bindings compile and evaluate through the public executable.
import json
import subprocess

input_value = {"field": 7}
result = subprocess.run(
    ["./jq", "-c", ".field, 42, $value"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC frontend-001-literals-and-fields ===

=== AC frontend-001-strings-and-interpolation ===
Intent: Valid escaped strings and interpolation are accepted and produce the value derived from supplied input.
import json
import subprocess

input_value = "jq"
program = '"prefix-\\(.)"'
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = ["prefix-" + input_value]
assert actual == expected
=== END AC frontend-001-strings-and-interpolation ===

=== AC frontend-001-invalid-escape ===
Intent: An invalid string escape is rejected during compilation.
import subprocess

result = subprocess.run(
    ["./jq", "-c", '"u\\vw"'],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC frontend-001-invalid-escape ===

## User Acceptance

- None.

## Guardrails

- Follow the supplied lexer token and state behavior.
- Reject malformed escapes and mismatched delimiters at compile time.
- Ignore comments without altering tokens in strings.
- Do not depend on a generated lexer or external parser tool at runtime.
