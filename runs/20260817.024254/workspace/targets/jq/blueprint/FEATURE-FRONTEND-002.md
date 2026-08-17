# FEATURE: jq Parser and AST

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines parsing and executable AST construction for jq expressions and declarations. |
| Depends On  | ARCHITECTURE.md, FEATURE-FRONTEND-001.md |
| Provides    | jq parser, AST, precedence and syntax validation |
| Consumes    | jq tokenization |

## Parser Contract

The parser must construct an executable representation for jq queries, including:

- Identity, literals, field access, indexing, slicing, iteration, arrays, and objects.
- Parentheses, pipes, comma generators, operators, conditionals, optional filters, and errors.
- Function definitions and calls, bindings, destructuring, reductions, foreach, labels, and breaks.
- String interpolation and format expressions.
- Assignment operators and module grammar.
- The precedence and associativity declared by the supplied parser grammar.

Invalid syntax and statically invalid constructs must fail compilation with exit status `3`.

## Programmatic Acceptance

=== AC frontend-002-precedence ===
Intent: The parser applies jq arithmetic precedence and evaluates the resulting AST.
import json
import subprocess

input_value = None
result = subprocess.run(
    ["./jq", "-c", "1 + 2 * 2"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [1 + 2 * 2]
assert actual == expected
=== END AC frontend-002-precedence ===

=== AC frontend-002-collections-and-pipeline ===
Intent: The parser accepts collection and pipeline syntax and preserves the collected values.
import json
import subprocess

input_value = [1, 2, 3]
result = subprocess.run(
    ["./jq", "-c", "[.[] | . + 1]"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [[value + 1 for value in input_value]]
assert actual == expected
=== END AC frontend-002-collections-and-pipeline ===

=== AC frontend-002-invalid-syntax ===
Intent: The parser rejects an unterminated object expression with compile exit status 3.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC frontend-002-invalid-syntax ===

=== AC frontend-002-assignment-syntax ===
Intent: The parser accepts assignment syntax and the evaluator applies the parsed update.
import json
import subprocess

input_value = {"count": 1}
result = subprocess.run(
    ["./jq", "-c", ".count += 1"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [{"count": input_value["count"] + 1}]
assert actual == expected
=== END AC frontend-002-assignment-syntax ===

## User Acceptance

- None.

## Guardrails

- Preserve the precedence, associativity, and syntax boundaries in the supplied parser grammar.
- Produce an AST or equivalent executable representation; do not translate programs by invoking jq.
- Keep compile-time rejection distinct from runtime evaluation.
- Support module grammar validation without requiring module-loader filesystem fixtures.
