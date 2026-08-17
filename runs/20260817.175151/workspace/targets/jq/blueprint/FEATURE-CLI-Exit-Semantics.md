# FEATURE: CLI Exit Semantics

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines jq compilation and runtime failure status behavior. |
| Depends On  | FEATURE-CLI-Entrypoint.md |
| Provides    | compile exit status 3, runtime exit status 5, partial runtime output |
| Consumes    | executable jq |

## Intent

Compilation failures exit with status `3`. Programs that compile and complete exit `0`. Programs that compile but raise during evaluation exit `5`. Values emitted before a runtime error remain on standard output, and diagnostics are written to standard error.

## Programmatic Acceptance

=== AC cli-exit-compile ===
Intent: A syntactically invalid jq program returns the documented compile-failure status.

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "["],
    input="null\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 3
=== END AC cli-exit-compile ===

=== AC cli-exit-runtime ===
Intent: A compiled program that raises at runtime returns the documented runtime-failure status.

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
assert result.returncode == 5
=== END AC cli-exit-runtime ===

=== AC cli-exit-partial-output ===
Intent: Values produced before a runtime error remain available to the caller.

import json
import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "1, error"],
    input="null\n",
    capture_output=True,
    text=True,
    env=os.environ.copy(),
)
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert result.returncode == 5
assert actual == [1]
=== END AC cli-exit-partial-output ===

## User Acceptance

- None.

## Guardrails

- Compile failures must remain distinguishable from runtime failures.
- Diagnostics go only to standard error and are not part of the output contract.
