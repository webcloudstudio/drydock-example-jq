# FEATURE: Errors and Control Flow

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implements jq runtime errors, try/catch, optional evaluation, labels, and breaks. |
| Depends On  | FEATURE-Operators.md |
| Provides    | runtime error status 5, try/catch, optional access, labels, break |
| Consumes    | generator evaluator, operators |

## Intent

Implement structured runtime failure and control-flow semantics while preserving ordered outputs emitted before uncaught failures.

## Scope

- Runtime error propagation with exit status 5.
- `error`, `try`, `catch`, and postfix `?`.
- Lexically scoped `label` and `break`.
- Error suppression and partial stream output.
- Distinction between compile errors and runtime errors.

## Programmatic Acceptance

=== AC errors-control-suite ===
Intent: Error and control behavior passes its authoritative conformance slice.
Suite: scoped

import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"(try|catch|break|label|\?)"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC errors-control-suite ===

=== AC errors-runtime-status ===
Intent: An uncaught runtime failure exits with the documented runtime status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC errors-runtime-status ===

=== AC errors-try-catch ===
Intent: try/catch converts a supplied runtime failure into a value.

import json
import subprocess

fallback = "handled"
program = f'try error catch {json.dumps(fallback)}'
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == fallback
=== END AC errors-try-catch ===

=== AC errors-partial-output ===
Intent: Values emitted before an uncaught runtime failure remain observable.

import json
import subprocess

program = "1, error"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [1]
=== END AC errors-partial-output ===

## User Acceptance

- None.

## Guardrails

- Runtime failures use exit status 5; compile failures use exit status 3.
- Diagnostics go to stderr only.
- `try`, `catch`, `?`, labels, and breaks must not reorder already-produced values.
- Break labels are lexical and unavailable outside their defining scope.
