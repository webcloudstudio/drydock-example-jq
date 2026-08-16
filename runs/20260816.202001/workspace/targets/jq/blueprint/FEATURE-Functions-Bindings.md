# FEATURE: Functions, Variables, Closures, and Destructuring

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines jq functions, lexical bindings, closures, and destructuring alternatives. |
| Depends On  | FEATURE-Errors-Control.md, FEATURE-Parser.md, FEATURE-Generator-Runtime.md |
| Provides    | user functions, filter parameters, value parameters, lexical bindings, destructuring, ?// |
| Consumes    | jq parser and AST, generator evaluator, runtime control flow |

## Intent

This feature implements jq's lexical function and binding model. Function definitions are visible
only to subsequent expressions, recursive definitions are supported, and function parameters retain
jq's distinction between filter arguments and value arguments.

Bindings include scalar variables, nested object and array patterns, closures, recursive calls, and
the `?//` destructuring alternative. Alternative branches must expose all variables used by the
continuation, assigning `null` where a successful branch did not bind a name.

## Behavior

- `def name: filter;` and `def name(args): filter;` define callable filters.
- Identifier parameters are filter parameters; binding parameters are evaluated values.
- Function calls preserve generator ordering and backtracking.
- `as` binds each result of its left expression while the continuation receives the original input.
- Bindings are immutable and lexically scoped.
- Array and object patterns bind missing values as `null`.
- `?//` selects the first successful destructuring branch and retries a later branch when the
  continuation raises an error.
- Undefined variables, invalid patterns, and malformed definitions are compile errors.

## Programmatic Acceptance

=== AC functions-bindings-suite ===
Intent: The supplied conformance corpus passes the functions, closures, bindings, and destructuring cases owned by this feature.
Suite: scoped

import subprocess
import os

pattern = r"def | as \$|destructur|closure|\\?//|reduce .* as"
result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
=== END AC functions-bindings-suite ===

=== AC functions-generator-arguments ===
Intent: Filter and value parameters preserve jq's distinct evaluation behavior.
import subprocess
import json

program = "def f(x): x|x; 5|f(.*2)"
input_value = "null\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [20]
assert actual == expected
=== END AC functions-generator-arguments ===

=== AC bindings-and-patterns ===
Intent: Lexical bindings and nested destructuring produce the supplied bound values.
import subprocess
import json

program = ". as {a: $a, b: [$b, {c: $c}]} | [$a, $b, $c]"
input_value = '{"a":1,"b":[2,{"c":3}]}\n'
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [[1, 2, 3]]
assert actual == expected
=== END AC bindings-and-patterns ===

=== AC undefined-binding-compile-error ===
Intent: Referencing an undefined variable produces the documented compile exit status.
import subprocess

result = subprocess.run(
    ["./jq", "-c", ". as $x | $missing"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC undefined-binding-compile-error ===

## User Acceptance

- None.

## Guardrails

- Do not treat filter parameters as eagerly evaluated values.
- Do not leak bindings outside their lexical scope.
- Do not retry a destructuring alternative after a successful branch unless its continuation
  raises a runtime error.
