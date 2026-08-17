# FEATURE: jq Assignment Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide jq immutable plain, update, arithmetic, defined-or, and complex assignments. |
| Depends On  | FEATURE-DATA-002.md, FEATURE-EVAL-002.md |
| Provides    | =, |=, +=, -=, *=, /=, %=, //= assignments |
| Consumes    | path, paths, getpath, setpath, delpaths, generator evaluator |

## Purpose

Implement assignment by deriving paths from the left-hand filter and producing immutable replacement
values. Plain assignment evaluates its right-hand side against the original input; update assignment
uses the selected value and keeps only its first result. Empty update results delete the selected path.

## Programmatic Acceptance

=== AC data-003-plain-assignment ===
Intent: Plain assignment reads the right-hand side from the original input.
import json
import subprocess

source = '{"a":{"b":10},"b":20}'
program = '.a = .b'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == {"a": 20, "b": 20}
=== END AC data-003-plain-assignment ===

=== AC data-003-update-assignment ===
Intent: Update assignment evaluates the update filter against the selected value.
import json
import subprocess

source = '{"a":{"b":10},"b":20}'
program = '.a |= .b'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == {"a": 10, "b": 20}
=== END AC data-003-update-assignment ===

=== AC data-003-complex-assignment ===
Intent: Multiple selected paths receive an arithmetic update immutably.
import json
import subprocess

source = '{"a":1,"b":2}'
program = '(.a,.b) += 1'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == {"a": 2, "b": 3}
=== END AC data-003-complex-assignment ===

=== AC data-003-empty-update ===
Intent: An empty update deletes the selected array elements.
import json
import subprocess

source = '[1,5,3,0]'
program = '(.[] | select(. >= 2)) |= empty'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [1, 0]
=== END AC data-003-empty-update ===

## User Acceptance

- None.

## Guardrails

- Assignments must preserve immutable input semantics.
- Preserve generator multiplicity and ordering for plain assignment.
- Do not silently convert assignment errors into compile successes.
