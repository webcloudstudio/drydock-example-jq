# FEATURE: jq Process Exit and Diagnostics

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Separates compile failures, runtime failures, successful completion, and diagnostics. |
| Depends On  | FEATURE-EXEC-001.md |
| Provides    | compile exit 3, runtime exit 5, success exit 0, stderr diagnostics |
| Consumes    | ./jq -c '<program>' |

## Intent

Implement the process contract required by the conformance harness. Invalid jq syntax exits `3`; a compiled program that raises at runtime exits `5`; successful execution exits `0`. Diagnostics go to standard error, while values emitted before a runtime failure remain on standard output.

## Programmatic Acceptance

=== AC compile-exit-code ===
Intent: A syntactically invalid jq program returns the compile-failure status.

import os
import subprocess

result = subprocess.run(
    [f"{os.getcwd()}/jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC compile-exit-code ===

=== AC runtime-exit-code ===
Intent: A compiled jq program that raises returns the runtime-failure status.

import os
import subprocess

result = subprocess.run(
    [f"{os.getcwd()}/jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC runtime-exit-code ===

=== AC partial-runtime-output ===
Intent: Values emitted before a runtime error remain available on stdout.

import os
import subprocess

result = subprocess.run(
    [f"{os.getcwd()}/jq", "-c", "1, error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
assert result.stdout.splitlines()[:1] == ["1"]
=== END AC partial-runtime-output ===

## User Acceptance

- None.

## Guardrails

- Never collapse compile and runtime failures into one status.
- Diagnostics must not be written to standard output.
- Preserve output produced before a runtime failure.
