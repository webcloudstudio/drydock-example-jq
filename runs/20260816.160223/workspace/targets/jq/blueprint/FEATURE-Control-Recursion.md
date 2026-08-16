# FEATURE: Control Recursion

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provides jq recursive generators and lexical labelled control flow. |
| Depends On  | ARCHITECTURE.md, FEATURE-Control-Errors.md, FEATURE-Control-Reductions.md |
| Provides    | while, until, repeat, recurse, label, break |
| Consumes    | ordered generator evaluator, runtime error handling |

## Purpose

Implement recursive generator constructs and lexical labels without losing stream order or allowing invalid label access.

## Behavior

- `while` emits each value while its condition is true.
- `until` repeatedly applies its update until its condition becomes true.
- `recurse` emits the current value and recursively produced descendants.
- `repeat` continues until an error terminates it.
- `label` establishes a lexical break target; `break` exits the labelled computation.
- A break referring to no visible label is a compile-time failure.

## Programmatic Acceptance

=== AC recursion-generators ===
Intent: Recursive generators, while, and until produce the expected finite streams.

import json
import subprocess

cases = [
    ("[while(. < 100; . * 2)]", "1\n", [1, 2, 4, 8, 16, 32, 64]),
    ("[recurse(.[]?)]", json.dumps([1, [2]]) + "\n", [[1, [2]], 1, [2], 2]),
    ("[.,1] | until(.[0] < 1; [.[0] - 1, .[1] * .[0]]) | .[1]", "4\n", [24]),
]
for program, payload, expected in cases:
    result = subprocess.run(["./jq", "-c", program], input=payload, capture_output=True, text=True)
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == expected
=== END AC recursion-generators ===

=== AC recursion-labels ===
Intent: Lexical labels and break preserve values emitted before the break.

import json
import subprocess

source = [0, 1, 2]
program = '[(label $out | .[] | if . > 1 then break $out else . end), "done"]'
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == [[0, 1, "done"]]
=== END AC recursion-labels ===

=== AC recursion-invalid-label ===
Intent: A break without a visible lexical label is rejected during compilation.

import subprocess

result = subprocess.run(["./jq", "-c", "break $missing"], input="null\n", capture_output=True, text=True)
assert result.returncode == 3
=== END AC recursion-invalid-label ===

## User Acceptance

- None.

## Guardrails

- Recursion must preserve generator ordering and avoid unbounded eager materialization where tail evaluation is possible.
- Labels are lexical; a binding with the same name must not create an implicit break target.
