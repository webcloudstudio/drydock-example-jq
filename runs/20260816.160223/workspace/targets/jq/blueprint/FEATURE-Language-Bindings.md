# FEATURE: Language Bindings

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provides jq lexical variable bindings and destructuring patterns. |
| Depends On  | ARCHITECTURE.md, FEATURE-Language-Functions.md, FEATURE-Eval-Cartesian.md |
| Provides    | as bindings and array/object patterns |
| Consumes    | evaluator, function scope, generator semantics |

## Purpose

Implement `as` bindings and array/object destructuring with lexical scope, generator-aware evaluation, keyword-compatible names, and null values for absent pattern members.

## Behavior

- `EXP as $name | BODY` evaluates `BODY` with the original input and each bound output.
- Array patterns bind positional elements and use null for missing positions.
- Object patterns bind named fields and nested patterns.
- Bindings are immutable and lexically scoped.
- Pattern bindings preserve upstream generator ordering.

## Programmatic Acceptance

=== AC bindings-basic ===
Intent: Scalar bindings retain their value across a pipeline and repeated references.

import json
import subprocess

payload = "null\n"
program = "1 as $x | 2 as $y | [$x, $y, $x]"
result = subprocess.run(["./jq", "-c", program], input=payload, capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [[1, 2, 1]]
=== END AC bindings-basic ===

=== AC bindings-patterns ===
Intent: Array and object destructuring bind present fields and null-fill absent array members.

import json
import subprocess

source = [[1], {"c": 3}]
program = ". as [$a, $b] | [$a, $b]"
result = subprocess.run(["./jq", "-c", program), input=json.dumps(source) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [[[1], None], [{"c": 3}, None]]
=== END AC bindings-patterns ===

=== AC bindings-nested ===
Intent: Nested object and array patterns expose their declared values in lexical scope.

import json
import subprocess

source = {"a": 1, "b": [2, {"d": 3}]}
program = ". as {$a, b: [$c, {$d}]} | [$a, $c, $d]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [[1, 2, 3]]
=== END AC bindings-nested ===

## User Acceptance

- None.

## Guardrails

- Bindings must not be mutable assignments.
- Bindings must not remain visible outside their lexical scope.
- Missing pattern members must bind null rather than raising an incidental host-language error.
