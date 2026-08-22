# FEATURE: Function Parameters

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq filter and value function parameter evaluation. |
| Depends On  | FEATURE-Variable-Bindings.md |
| Provides    | filter parameters, value parameters, multiple arities, Cartesian arguments |
| Consumes    | lexical variable bindings |

## Workflow

User-defined functions accept filter parameters and value parameters with jq arity rules. Filter arguments remain executable generators, value arguments are evaluated and bound, and multiple argument streams produce the required cartesian combinations.

## Programmatic Acceptance

=== AC function-parameters-scoped ===
Intent: Function-parameter behavior is implemented for filter arguments.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "def twice(f): f | f; twice(. + 1)"],
    input="1\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == 3

=== END AC function-parameters-scoped ===

=== AC cartesian-function-scoped ===
Intent: Multiple generator-valued arguments produce Cartesian combinations.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "def pair(a; b): [a, b]; pair(.[0, 1]; .[1, 2])"],
    input="[10, 20, 30]\n",
    capture_output=True,
    text=True,
)
values = [json.loads(line) for line in result.stdout.splitlines()]
assert result.returncode == 0
assert values == [[10, 20], [10, 30], [20, 20], [20, 30]]

=== END AC cartesian-function-scoped ===

## User Acceptance

- None.

## Guardrails

- Distinguish filter parameters from value parameters.
- Preserve argument stream ordering and cartesian multiplicity.
- Resolve parameters according to lexical scope and declared arity.
