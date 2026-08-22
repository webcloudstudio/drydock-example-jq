# FEATURE: Diagnostics

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq diagnostic, stderr, and halt-error filters. |
| Depends On  | FEATURE-Input-Streams.md, FEATURE-Process-Contract.md |
| Provides    | debug, stderr, halt_error |
| Consumes    | process exit and diagnostic behavior |

## Intent

Implement diagnostic filters that write to stderr, preserve stdout values, and terminate with the required status behavior. `debug` must retain the input stream, `stderr` must emit raw diagnostic data, and `halt_error` must stop processing with its requested exit code.

## Programmatic Acceptance

=== AC io-002-conformance ===
Intent: Diagnostic filters preserve stdout values and write diagnostics to stderr.
Requires: executable=python3; scope=test

import subprocess

debug = subprocess.run(
    ["./jq", "-c", "debug"],
    input='"value"\n',
    capture_output=True,
    text=True,
)
assert debug.returncode == 0
assert debug.stdout.splitlines() == ['"value"']
assert debug.stderr

stderr = subprocess.run(
    ["./jq", "-c", "stderr"],
    input='"value"\n',
    capture_output=True,
    text=True,
)
assert stderr.returncode == 0
assert stderr.stdout == ""
assert stderr.stderr
=== END AC io-002-conformance ===

=== AC io-002-execution ===
Intent: halt_error terminates execution with a runtime failure status.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "halt_error(5)"],
    input='"value"\n',
    capture_output=True,
    text=True,
)
assert result.returncode == 5
assert result.stdout == ""
=== END AC io-002-execution ===

## User Acceptance

- None.

## Guardrails

- Diagnostics must not be used as the output oracle.
- Preserve stdout values emitted before runtime termination.
- Keep diagnostic output on stderr and use only standard-library facilities.
