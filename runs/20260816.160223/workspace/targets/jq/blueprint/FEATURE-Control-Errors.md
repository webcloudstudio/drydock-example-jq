# FEATURE: Runtime Errors and Recovery

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implement jq runtime errors, recovery handlers, halt behavior, and output preservation. |
| Depends On  | FEATURE-Control-Conditionals.md, FEATURE-CLI-Errors.md |
| Provides    | try/catch, error, halt, halt_error |
| Consumes    | ordered generator evaluator, executable exit mapping |

## Intent

Runtime failures are structured control transfers carrying jq values or messages. `try EXP catch HANDLER` evaluates the handler with the error value; `try EXP` suppresses the error. `error`, `halt`, and `halt_error` have distinct output and process-termination semantics.

The evaluator must preserve values emitted before a failure. The executable maps ordinary uncaught runtime failures to exit 5 while allowing `halt` to terminate successfully and `halt_error` to select its requested code.

## Behaviors

- `error` raises the current input and `error(message)` raises the supplied value.
- `try/catch` recovers errors and continues generator evaluation where applicable.
- `halt` stops without an error status.
- `halt_error` writes the raw input to stderr and exits with its requested status.
- Uncaught runtime errors produce exit 5 and diagnostics on stderr.
- Previously emitted stdout values remain available after a runtime failure.

## Programmatic Acceptance

=== AC errors-try-catch ===
Intent: The implementation passes the authoritative try/catch and error-value corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "try|catch|error\\(|try error|caught"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC errors-try-catch ===

=== AC errors-halting ===
Intent: The implementation passes the authoritative halt and halt_error corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "halt(_error)?|halt_error"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC errors-halting ===

=== AC errors-output-preservation ===
Intent: The implementation passes the authoritative corpus cases that emit values before runtime failure.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "outputs before|prior outputs|first\\(1,error|OK.*error|error.*catch"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC errors-output-preservation ===

## User Acceptance

- None.

## Guardrails

- Never discard values emitted before an uncaught runtime error.
- Keep diagnostics on stderr; stdout contains only JSON result values.
- Do not convert compile-time failures into runtime failures.
- Do not invoke an external jq binary or third-party implementation.
