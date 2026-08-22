# FEATURE: Process Contract

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq compilation, runtime failure, success, and diagnostic process behavior. |
| Depends On  | FEATURE-Executable-Entry-Point.md, FEATURE-Declarations-And-Control-Syntax.md, FEATURE-Errors-And-Optional-Evaluation.md |
| Provides    | compile exit 3, runtime exit 5, success exit 0, stderr diagnostics |
| Consumes    | executable jq, parser, evaluator |

## Intent

The process distinguishes compilation failures from runtime failures:

- Exit `0` means compilation and execution completed.
- Exit `3` means the filter was rejected before execution.
- Exit `5` means execution raised a runtime error.
- Diagnostics are written to standard error.
- Values produced before a runtime error remain on standard output.

## Programmatic Acceptance

=== AC compile-exit-status ===
Intent: Invalid jq syntax is rejected with compile exit status 3.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 3
=== END AC compile-exit-status ===

=== AC runtime-exit-status ===
Intent: A compiled filter that raises at runtime exits 5 and keeps diagnostics off stdout.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 5
assert result.stderr != ""
assert result.stdout == ""
=== END AC runtime-exit-status ===

=== AC partial-runtime-output ===
Intent: Values emitted before a runtime error remain available on stdout.

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
=== END AC partial-runtime-output ===

## User Acceptance

- None.

## Guardrails

- Compile failures must remain distinct from runtime failures.
- Runtime diagnostics must never be emitted as JSON output.
- Partial output before a runtime failure must not be discarded.
