# FEATURE: Control Reductions

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provides jq reductions and bounded generator controls. |
| Depends On  | ARCHITECTURE.md, FEATURE-Eval-Stream.md, FEATURE-Control-Errors.md |
| Provides    | reduce, foreach, limit, skip, first, last, nth |
| Consumes    | ordered generator evaluator, runtime error handling |

## Purpose

Implement reduction and bounded-generator semantics while preserving jq stream ordering, backtracking, short-circuiting, and cartesian argument evaluation.

## Behavior

- `reduce EXP as $x (INIT; UPDATE)` evaluates each output of `EXP` in order and feeds the accumulator through `UPDATE`.
- `foreach` emits each extracted intermediate result.
- `limit`, `skip`, `first`, `last`, and `nth` consume generator output without evaluating unnecessary values.
- Multiple-output arguments produce jq-defined cartesian combinations.
- Negative bounds that jq rejects raise runtime errors.

## Programmatic Acceptance

=== AC reductions-basic ===
Intent: Reductions and foreach preserve ordered accumulation and extraction.

import json
import subprocess

source = [1, 2, 3]
payload = json.dumps(source) + "\n"
programs = [
    ("reduce .[] as $x (0; . + $x)", [sum(source)]),
    ("[foreach .[] as $x (0; . + $x)]", [1, 3, 6]),
]
for program, expected in programs:
    result = subprocess.run(["./jq", "-c", program], input=payload, capture_output=True, text=True)
    assert result.returncode == 0
    actual = [json.loads(line) for line in result.stdout.splitlines()]
    assert actual == expected
=== END AC reductions-basic ===

=== AC reductions-bounds ===
Intent: Bounded generator controls select the requested ordered outputs.

import json
import subprocess

source = list(range(10))
payload = json.dumps(source) + "\n"
cases = [
    ("[limit(3; .[])]", source[:3]),
    ("[skip(3; .[])]", source[3:]),
    ("[first(.[]), last(.[]), nth(5; .[])]", [source[0], source[-1], source[5]]),
]
for program, expected in cases:
    result = subprocess.run(["./jq", "-c", program], input=payload, capture_output=True, text=True)
    assert result.returncode == 0
    assert [json.loads(line) for line in result.stdout.splitlines()] == [expected]
=== END AC reductions-bounds ===

=== AC reductions-errors ===
Intent: Invalid negative bounds fail at runtime with jq's runtime exit class.

import subprocess

for program in ("limit(-1; error)", "skip(-1; error)", "nth(-1; range(3))"):
    result = subprocess.run(["./jq", "-c", f"try ({program}) catch ."], input="null\n", capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout.splitlines()
=== END AC reductions-errors ===

## User Acceptance

- None.

## Guardrails

- Preserve outputs already emitted before a later generator or update failure.
- Do not collapse streams into a single value during reduction control.
- Do not alter the supplied conformance corpus or harness.
