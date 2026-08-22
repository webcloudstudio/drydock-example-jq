# FEATURE: Recursive Generators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq recursive and repeated generator filters. |
| Depends On  | FEATURE-Reductions-and-Iteration-Control.md |
| Provides    | while, until, repeat, recurse, recursive descent |
| Consumes    | reductions and ordered generator evaluation |

## Workflow

The evaluator supports recursive descent and the `while`, `until`, `repeat`, and `recurse` generators. Recursive filters emit values in jq order, terminate according to their predicates or caught errors, and preserve branching when an update yields multiple values.

## Programmatic Acceptance

=== AC recursive-generators-scoped ===
Intent: Recursive generator behavior executes successfully for representative while, until, and recurse programs.
Suite: scoped

import subprocess

while_result = subprocess.run(
    ["./jq", "-c", "1 | while(. < 3; . + 1)",],
    input="null\n",
    capture_output=True,
    text=True,
)
until_result = subprocess.run(
    ["./jq", "-c", "1 | until(. >= 3; . + 1)",],
    input="null\n",
    capture_output=True,
    text=True,
)
recurse_result = subprocess.run(
    ["./jq", "-c", "1 | recurse(. < 3; . + 1)",],
    input="null\n",
    capture_output=True,
    text=True,
)
assert while_result.returncode == 0
assert until_result.returncode == 0
assert recurse_result.returncode == 0
assert while_result.stdout != ""
assert until_result.stdout != ""
assert recurse_result.stdout != ""
=== END AC recursive-generators-scoped ===

=== AC recursive-descent-scoped ===
Intent: Recursive-descent syntax executes successfully and emits descendants.
Suite: scoped

import subprocess

result = subprocess.run(
    ["./jq", "-c", "..",],
    input='{"a":1}\n',
    capture_output=True,
    text=True,
)
lines = result.stdout.splitlines()
assert result.returncode == 0
assert len(lines) >= 2
assert "1" in lines
=== END AC recursive-descent-scoped ===

## User Acceptance

- None.

## Guardrails

- Recursive generators must not emit duplicate or incorrectly ordered values.
- Termination must not depend on a fixed shallow recursion cutoff.
- Runtime errors from repeated expressions must remain catchable.
