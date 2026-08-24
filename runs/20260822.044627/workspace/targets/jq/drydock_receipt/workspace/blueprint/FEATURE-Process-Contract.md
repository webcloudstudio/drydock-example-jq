# FEATURE: jq Process Contract

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq compilation, runtime failure, success, partial-output, and diagnostic process behavior. |
| Depends On  | FEATURE-Executable-Entry-Point.md |
| Provides    | compile exit 3, runtime exit 5, success exit 0, stderr diagnostics |
| Consumes    | ./jq -c program execution |

## Compile and Runtime Outcomes

| Condition | Exit |
|---|---:|
| Program compiles and finishes | `0` |
| Program is rejected during compilation | `3` |
| Program compiles and raises during evaluation | `5` |

A compile failure must not be reported as a runtime failure. A runtime failure may occur after values have already been emitted; those values remain observable on stdout. Diagnostics go to stderr and are not part of the value stream.

## Programmatic Acceptance

=== AC exec-002-compile-runtime ===
Intent: The executable distinguishes compile failures, runtime failures, and successful completion.
Suite: scoped
Requires: executable=python3; scope=test

import subprocess

compile_result = subprocess.run(
    ["./jq", "-c", "{",],
    input="null\n",
    capture_output=True,
    text=True,
)
runtime_result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
success_result = subprocess.run(
    ["./jq", "-c", "."],
    input="null\n",
    capture_output=True,
    text=True,
)
assert compile_result.returncode == 3
assert runtime_result.returncode == 5
assert success_result.returncode == 0
assert compile_result.stderr != ""
assert runtime_result.stderr != ""
=== END AC exec-002-compile-runtime ===

=== AC exec-002-statuses ===
Intent: The executable exposes distinct compile, runtime, and successful completion statuses.

import subprocess

compile_result = subprocess.run(
    ["./jq", "-c", "{",],
    input="null\n",
    capture_output=True,
    text=True,
)
runtime_result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
success_result = subprocess.run(
    ["./jq", "-c", "."],
    input="null\n",
    capture_output=True,
    text=True,
)
assert compile_result.returncode == 3
assert runtime_result.returncode == 5
assert success_result.returncode == 0
=== END AC exec-002-statuses ===

=== AC exec-002-partial-output ===
Intent: A runtime failure preserves values emitted before the failure and keeps diagnostics off standard output.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "1, error"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 5
assert result.stdout.splitlines() == ["1"]
assert result.stderr != ""
=== END AC exec-002-partial-output ===

## User Acceptance

- None.

## Guardrails

- Compile failures exit `3`.
- Runtime failures exit `5`.
- Successful completion exits `0`.
- Runtime output produced before failure is preserved.
- Diagnostics are written to stderr only.
