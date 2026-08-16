# FEATURE: Frontend Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Parse jq programs into an executable abstract syntax tree. |
| Depends On  | ARCHITECTURE.md, FEATURE-Frontend-Lexer.md |
| Provides    | jq parser and AST |
| Consumes    | jq tokenizer |

## Intent

The parser consumes lexer tokens and constructs AST nodes for jq filters, operators, constructors, control flow, functions, bindings, assignments, and module syntax. It must preserve jq precedence, associativity, generator structure, and source locations needed by diagnostics.

## Scope

Supported grammar includes:

- identity, literals, fields, indexing, iteration, slicing, pipes, commas, and parentheses;
- arrays, objects, string interpolation, formats, and unary operators;
- arithmetic, comparison, boolean, alternative, and assignment operators;
- conditionals, `try`, `reduce`, `foreach`, labels, bindings, and function definitions;
- module/import syntax sufficient to validate supported and rejected forms.

The parser must not evaluate programs or perform filesystem module loading.

## Programmatic Acceptance

=== AC frontend-parser-basic ===
Intent: The parser accepts representative jq expressions and the executable evaluates them successfully.

import json
import subprocess

source = '[.[] | . + 1]'
input_value = [1, 2, 3]
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = [value + 1 for value in input_value]
assert actual == expected
=== END AC frontend-parser-basic ===

=== AC frontend-parser-constructors ===
Intent: The parser accepts object construction, interpolation, and precedence-bearing expressions.

import json
import subprocess

source = '{value: (.x + 1), text: "item \\(.x)"}'
input_value = {"x": 4}
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual["value"] == input_value["x"] + 1
assert actual["text"] == "item " + str(input_value["x"])
=== END AC frontend-parser-constructors ===

=== AC frontend-parser-definitions ===
Intent: The parser accepts function definitions, bindings, reductions, and assignments.

import json
import subprocess

source = 'def inc: . + 1; reduce .[] as $x (0; . + $x) | inc'
input_value = [1, 2, 3]
result = subprocess.run(
    ["./jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == sum(input_value) + 1
=== END AC frontend-parser-definitions ===

## User Acceptance

- None.

## Guardrails

- Preserve generator-producing AST structure and operator precedence.
- Do not shell out to jq or use a third-party parser.
- Do not load module files while parsing.
