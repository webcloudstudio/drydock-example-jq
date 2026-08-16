# FEATURE: CLI Errors

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines jq compile-time and runtime failure behavior. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-Entrypoint.md, FEATURE-Frontend-Validation.md, FEATURE-Eval-Core.md |
| Provides    | compile exit 3, runtime exit 5, stderr diagnostics |
| Consumes    | executable entrypoint, parser, evaluator |

## Behavior

Invalid syntax or static errors are rejected before evaluation with exit code `3`. A valid program that raises during evaluation exits `5`. Diagnostics are written to stderr. Values emitted before a runtime failure remain available on stdout.

## Programmatic Acceptance

=== AC cli-compile-error ===
Intent: A syntactically invalid jq program exits with the compile-error status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC cli-compile-error ===

=== AC cli-runtime-error ===
Intent: A valid jq program that raises at runtime exits with the runtime-error status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC cli-runtime-error ===

=== AC cli-prior-output ===
Intent: Outputs produced before a runtime error remain available.

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
expected = [1]
assert actual == expected
=== END AC cli-prior-output ===

## User Acceptance

- None.

## Guardrails

- Compile failures must not be reported as runtime failures.
- Runtime failures must not erase values already emitted.
- Diagnostics go to stderr and are not used as a behavioral output channel.
