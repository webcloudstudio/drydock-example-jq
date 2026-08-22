# FEATURE: Function Definitions

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq function definitions, lexical scope, redefinition, and recursion. |
| Depends On  | FEATURE-Function-Parameters.md |
| Provides    | def, function redefinition, recursion, forward and self references |
| Consumes    | function parameter evaluation |

## Workflow

The interpreter compiles `def` declarations into lexically scoped callable definitions. Definitions support recursive self-reference, arity-specific redefinition, forward references permitted by jq semantics, and closure behavior across nested definitions.

## Programmatic Acceptance

=== AC function-definitions-scoped ===
Intent: Function-definition behavior is implemented and callable.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "def inc: . + 1; inc"],
    input="2\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == 3

=== END AC function-definitions-scoped ===

=== AC function-recursion-scoped ===
Intent: Recursive user-function behavior is implemented and terminates correctly.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "def fact: if . <= 1 then 1 else . * ((. - 1) | fact) end; fact"],
    input="5\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == 120

=== END AC function-recursion-scoped ===

## User Acceptance

- None.

## Guardrails

- Function identity includes name and arity.
- Redefinition must affect only references permitted by jq lexical scope.
- Recursive calls must terminate or propagate runtime errors according to the filter semantics.
