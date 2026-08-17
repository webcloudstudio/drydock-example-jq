# FEATURE: Front Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines parsing jq source into an executable abstract syntax representation. |
| Depends On  | FEATURE-Front-Lexer.md |
| Provides    | jq parser and AST |
| Consumes    | jq lexer |

## Intent

The parser builds an executable representation for jq precedence and associativity, indexing, slicing, arrays, objects, conditionals, function definitions, bindings, modules, and reductions. It preserves generator structure so later evaluation can retain jq ordering and multiplicity.

## Programmatic Acceptance

=== AC front-parser-precedence ===
Intent: The parser accepts grouped arithmetic with jq precedence and executes the resulting representation.

import json
import os
import subprocess

program = "(1 + 2) * 3"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert result.returncode == 0
assert actual == [9]
=== END AC front-parser-precedence ===

=== AC front-parser-construction ===
Intent: The parser accepts array and object construction expressions.

import json
import os
import subprocess

program = "{value: ., items: [., 2]}"
payload = {"x": 1}
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(payload) + "\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert result.returncode == 0
assert actual == [{"value": payload, "items": [payload, 2]}]
=== END AC front-parser-construction ===

=== AC front-parser-invalid-structure ===
Intent: An unterminated parser construct returns the compile-failure status.

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "{a: 1"],
    input="null\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 3
=== END AC front-parser-invalid-structure ===

## User Acceptance

- None.

## Guardrails

- Parser precedence and associativity must follow `sources/parser.y`.
- Module syntax is parsed far enough to reject invalid forms without attempting unsupported module loading.
