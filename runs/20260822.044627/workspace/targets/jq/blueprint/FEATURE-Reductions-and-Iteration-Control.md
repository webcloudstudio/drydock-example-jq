# FEATURE: Reductions and Iteration Control

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq reductions and generator control primitives. |
| Depends On  | FEATURE-Labels-and-Breaks.md, FEATURE-Generator-Core.md |
| Provides    | reduce, foreach, limit, skip, first, last, nth, range |
| Consumes    | label and break evaluation, ordered generator evaluation |

## Workflow

The evaluator implements stateful `reduce` and `foreach` operations, bounded and skipped generator consumption, first/last/nth selection, and range generation. All operations preserve jq stream ordering, multiplicity, cartesian argument behavior, and lexical break handling.

## Programmatic Acceptance

=== AC reductions-scoped ===
Intent: Reduction and iteration-control behavior executes successfully for representative reduce, foreach, limit, first, and nth programs.
Suite: scoped

import subprocess

reduce_result = subprocess.run(
    ["./jq", "-c", "reduce range(1; 4) as $x (0; . + $x)",],
    input="null\n",
    capture_output=True,
    text=True,
)
foreach_result = subprocess.run(
    ["./jq", "-c", "foreach range(1; 4) as $x (0; . + $x)",],
    input="null\n",
    capture_output=True,
    text=True,
)
limit_result = subprocess.run(
    ["./jq", "-c", "limit(2; range(5))",],
    input="null\n",
    capture_output=True,
    text=True,
)
assert reduce_result.returncode == 0
assert foreach_result.returncode == 0
assert limit_result.returncode == 0
assert reduce_result.stdout != ""
assert foreach_result.stdout != ""
assert limit_result.stdout.splitlines() == ["0", "1"]
=== END AC reductions-scoped ===

=== AC range-scoped ===
Intent: Range generation executes successfully and preserves generated values.
Suite: scoped

import subprocess

result = subprocess.run(
    ["./jq", "-c", "range(2; 5)",],
    input="null\n",
    capture_output=True,
    text=True,
)
lines = result.stdout.splitlines()
assert result.returncode == 0
assert lines == ["2", "3", "4"]
assert len(lines) > 0
=== END AC range-scoped ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering, multiplicity, backtracking, and partial runtime output.
- Do not implement reductions as scalar-only operations.
- Negative limits, skips, and nth indices must retain jq runtime-error behavior.
