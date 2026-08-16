# FEATURE: Language Functions

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provides jq user-defined functions, parameters, closures, and recursion. |
| Depends On  | ARCHITECTURE.md, FEATURE-Frontend-Parser.md, FEATURE-Eval-Cartesian.md, FEATURE-Control-Recursion.md |
| Provides    | def declarations and function calls |
| Consumes    | parser and AST, generator evaluator, lexical scope |

## Purpose

Implement jq function definitions and calls with filter parameters, value parameters, arity, lexical scoping, redefinition, closures, and recursion.

## Behavior

- `def name: FILTER;` defines a zero-argument filter.
- Named arguments are filters; `$`-prefixed arguments are value expressions.
- Calls preserve generator backtracking and cartesian argument order.
- Functions may recurse and capture lexically visible definitions and values.
- Redefinition is scoped to subsequent references and keyed by function arity.

## Programmatic Acceptance

=== AC functions-filter-arguments ===
Intent: Filter arguments are evaluated against the current pipeline value and may be reused.

import json
import subprocess

payload = json.dumps([[1, 2], [10, 20]]) + "\n"
program = "def addvalue(f): f as $x | map(. + $x); addvalue(.[0])"
result = subprocess.run(["./jq", "-c", program], input=payload, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [[[1, 2, 1, 2], [10, 20, 1, 2]]]
=== END AC functions-filter-arguments ===

=== AC functions-recursion ===
Intent: User-defined recursive functions calculate each requested factorial.

import json
import subprocess

source = [1, 2, 3, 4]
program = "def fac: if . == 1 then 1 else . * (. - 1 | fac) end; [.[] | fac]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [[1, 2, 6, 24]]
=== END AC functions-recursion ===

=== AC functions-closures ===
Intent: Lexical closures retain captured values independently of later pipeline inputs.

import json
import subprocess

program = "2000 as $x | def f(x): 1 as $x | [$x, x]; f($x)"
result = subprocess.run(["./jq", "-c", program], input='"input"\n', capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [[1, 2000]]
=== END AC functions-closures ===

## User Acceptance

- None.

## Guardrails

- Function arguments must remain filters unless explicitly declared as value parameters.
- Function scope must be lexical and must not leak bindings into callers.
- Do not use a third-party jq implementation or invoke a system jq binary.
