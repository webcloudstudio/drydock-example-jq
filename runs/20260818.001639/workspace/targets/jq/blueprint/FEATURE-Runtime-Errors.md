# FEATURE: Runtime Errors

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implements jq runtime errors, exception handling, halting, labels, and breaks. |
| Depends On  | FEATURE-Conditionals.md |
| Provides    | error, try/catch, halt, halt_error, label, break, runtime exit status 5 |
| Consumes    | ordered filter generators |

## Intent

Runtime failures propagate through generators with exit status 5 while preserving output already emitted. `try` and `catch` intercept errors, `halt` stops successfully, and labels provide lexical escape targets for `break`.

## Programmatic Acceptance

=== AC runtime-errors-corpus ===
Intent: The implementation passes conformance cases covering errors, try/catch, optional suppression, halting, labels, and breaks.
Suite: scoped

import os
import subprocess
import sys

selector = r"error|try |catch|halt|break|label"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC runtime-errors-corpus ===

=== AC runtime-partial-output ===
Intent: The selected runtime-error cases verify that valid output emitted before a runtime failure remains observable.
Suite: scoped

import os
import subprocess
import sys

selector = r"first\(1,error|1, try error|try limit"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC runtime-partial-output ===

## User Acceptance

- None.

## Guardrails

- Compile failures remain distinct from runtime failures.
- Runtime errors must not discard already-emitted output.
- Diagnostics go only to standard error.
