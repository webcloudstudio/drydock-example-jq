# FEATURE: Generator Runtime

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Evaluates jq filters as ordered zero-, one-, or many-value streams. |
| Depends On  | FEATURE-Compile-Contract.md, FEATURE-Formats.md |
| Provides    | generator evaluator, pipeline semantics, comma semantics |
| Consumes    | jq parser and AST |

## Intent

Implement jq's generator evaluation model. Every filter consumes one input and yields an ordered stream; pipelines apply downstream filters to every upstream result.

## Scope

- Identity, literals, comma, pipe, and empty stream evaluation.
- Cartesian products for multi-result operands.
- Ordered backtracking and partial output preservation.
- Stream propagation through constructors and function calls.
- Runtime evaluation state sufficient for later bindings, control flow, and builtins.

## Programmatic Acceptance

=== AC generator-suite ===
Intent: The generator runtime passes its authoritative conformance slice.
Suite: scoped

import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"(^empty$|,|\|)"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC generator-suite ===

=== AC generator-order ===
Intent: Comma and pipeline preserve ordered stream results.

import json
import subprocess

input_value = [1, 2, 3]
program = ".[] | ., (.+10)"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = []
for item in input_value:
    expected.extend([item, item + 10])
assert actual == expected
=== END AC generator-order ===

=== AC generator-empty ===
Intent: The empty filter produces no output and succeeds.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "empty"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout == ""
=== END AC generator-empty ===

## User Acceptance

- None.

## Guardrails

- Preserve zero, one, and multiple outputs as distinct stream events.
- Never collapse a generator to a single value.
- Preserve values emitted before a later runtime error.
