# FEATURE: Reductions and Recursive Control Flow

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines jq reductions, generator limits, range helpers, and recursive control filters. |
| Depends On  | FEATURE-Functions-Bindings.md, FEATURE-Generator-Runtime.md |
| Provides    | reduce, foreach, range, limit, skip, first, last, nth, while, until, repeat, recurse |
| Consumes    | generator evaluator, functions and bindings, runtime labels |

## Intent

This feature provides jq's generator-oriented iteration and accumulation constructs. Each construct
must preserve stream order, evaluate generator expressions correctly, and support lexical labels and
backtracking where the jq language requires them.

## Behavior

- `reduce EXP as $x (INIT; UPDATE)` evaluates `UPDATE` once per generated value.
- `foreach` emits each intermediate accumulator through its extraction filter.
- `range` supports one-, two-, and three-argument forms, including descending ranges.
- `limit`, `skip`, `first`, `last`, and `nth` operate on generator outputs.
- `while`, `until`, and `repeat` recursively evaluate filters with generator semantics.
- `recurse` emits the current value before recursively generated descendants.
- Negative unsupported counts raise runtime errors; `label`/`break` can terminate iteration.

## Programmatic Acceptance

=== AC reductions-suite ===
Intent: The supplied conformance corpus passes the reduction and recursive-control cases owned by this feature.
Suite: scoped

import subprocess
import os

pattern = r"reduce|foreach|range\\(|limit\\(|skip\\(|first\\(|last\\(|nth\\(|while\\(|until\\(|repeat\\(|recurse|label \\$"
result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
=== END AC reductions-suite ===

=== AC reduce-and-foreach ===
Intent: Reduction and foreach preserve accumulator order and extraction behavior.
import subprocess
import json

program = "[reduce .[] as $x (0; . + $x), foreach .[] as $x (0; . + $x)]"
input_value = "[1,2,3]\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [[6, 1, 3, 6]]
assert actual == expected
=== END AC reduce-and-foreach ===

=== AC range-limit-skip ===
Intent: Range generation, limiting, and skipping preserve ordered stream values.
import subprocess
import json

program = "[range(0;10;3)], [limit(3; range(10))], [skip(3; range(6))]"
input_value = "null\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [[0, 3, 6, 9], [0, 1, 2], [3, 4, 5]]
assert actual == expected
=== END AC range-limit-skip ===

=== AC negative-count-runtime-error ===
Intent: Unsupported negative limit counts produce the documented runtime exit status.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "limit(-1; 1)"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC negative-count-runtime-error ===

## User Acceptance

- None.

## Guardrails

- Preserve generator order and do not collapse multi-output filters into one value.
- Do not evaluate an unneeded tail after `first`, `limit`, or `break`.
- Preserve partial output emitted before an uncaught runtime error.
