# FEATURE: Error and Optional Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq runtime errors, optional evaluation, suppression, and try/catch behavior. |
| Depends On  | FEATURE-Composition.md |
| Provides    | empty, error, runtime failure, optional operator, try/catch |
| Consumes    | ordered generator evaluation |

## Workflow

Runtime errors propagate with exit status 5 after preserving values already emitted. `empty` emits no values. The optional suffix suppresses errors, while `try ... catch ...` evaluates a handler with the error value.

## Programmatic Acceptance

=== AC core-003-conformance ===
Intent: Runtime errors, optional evaluation, and try/catch behave as declared.
Requires: executable=python3; scope=test

import subprocess

optional = subprocess.run(
    ["./jq", "-c", ".foo?"],
    input="1\n",
    capture_output=True,
    text=True,
)
assert optional.returncode == 0
assert optional.stdout.splitlines() == ["null"]

caught = subprocess.run(
    ["./jq", '-c', 'try error("x") catch .'],
    input="null\n",
    capture_output=True,
    text=True,
)
assert caught.returncode == 0
assert caught.stdout.splitlines() == ['"x"']
=== END AC core-003-conformance ===

=== AC core-003-runtime-contract ===
Intent: Compile errors, runtime errors, and successful execution retain their distinct exit statuses.
Requires: executable=python3; scope=test

import subprocess

valid = subprocess.run(
    ["./jq", "-c", "."],
    input="1\n",
    capture_output=True,
    text=True,
)
compile_error = subprocess.run(
    ["./jq", "-c", "["],
    input="1\n",
    capture_output=True,
    text=True,
)
runtime_error = subprocess.run(
    ["./jq", "-c", "error"],
    input="1\n",
    capture_output=True,
    text=True,
)
assert valid.returncode == 0
assert compile_error.returncode == 3
assert runtime_error.returncode == 5
=== END AC core-003-runtime-contract ===

## User Acceptance

- None.

## Guardrails

- Diagnostics are written to stderr and are not used as the behavioral oracle.
- Partial stdout emitted before a runtime error is preserved.
- Optional evaluation must not suppress compile-time errors.
