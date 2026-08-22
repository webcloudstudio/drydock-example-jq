# FEATURE: jq Composition and Cartesian Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Evaluate jq composition, collections, arguments, objects, and binary combinations. |
| Depends On  | ARCHITECTURE.md, FEATURE-CORE-001.md |
| Provides    | pipe, comma, argument, array, object, and binary composition |
| Consumes    | ordered generator evaluator |

## Scope

Implement composition over stream-valued filters: pipe outputs into downstream filters, concatenate comma streams, evaluate filter arguments against the correct input, collect arrays, construct objects, and produce Cartesian combinations for multi-output operands and arguments. Preserve jq's documented evaluation order.

## Programmatic Acceptance

=== AC core-002-conformance ===
Intent: The executable evaluates pipes, commas, arrays, objects, and composed operators.
Suite: scoped
Requires: executable=python3; scope=test

import subprocess

def run(program, input_text="null\n"):
    return subprocess.run(
        ["./jq", "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
    )

assert run("[1,2,3] | .[]").returncode == 0
assert run("[1,2,3] | .[]").stdout == "1\n2\n3\n"
assert run("[. + 1, . + 2]", "4\n").stdout == "[5,6]\n"
assert run("{a: 1, b: 2}").stdout == '{"a":1,"b":2}\n'
=== END AC core-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Pipe and comma ordering is observable and must remain stable.
- Multi-output operands must produce all required Cartesian combinations.
- Collection and object construction must not mutate their input values.
