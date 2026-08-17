# FEATURE: Bounded Implementation Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide focused deterministic verification for the interpreter's core behavior and CLI contract. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-002.md, FEATURE-FRONTEND-003.md, FEATURE-EVAL-003.md, FEATURE-DATA-003.md, FEATURE-BUILTIN-005.md |
| Provides    | focused implementation verification |
| Consumes    | ./jq -c, interpreter modules |

## Purpose

Add bounded diagnostic verification for representative lexer, parser, generator, structural, assignment, builtin, compile-error, and runtime-error behavior. These checks are independent of the complete acceptance gate and must remain deterministic, local, and standard-library-only.

## Programmatic Acceptance

=== AC verify-002-cli-success ===
Intent: The executable accepts a compact jq program and returns success with one result per produced value.

import json
import subprocess

payload = json.dumps([1, 2, 3])
result = subprocess.run(
    ["./jq", "-c", ".[]"],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert len([line for line in result.stdout.splitlines() if line]) == len(json.loads(payload))
=== END AC verify-002-cli-success ===

=== AC verify-002-compile-error ===
Intent: A syntactically invalid jq program returns the compile-error exit status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "{"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC verify-002-compile-error ===

=== AC verify-002-runtime-error ===
Intent: A compiled jq program that raises at runtime returns the runtime-error exit status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC verify-002-runtime-error ===

## User Acceptance

- None.

## Guardrails

- Keep verification bounded and deterministic.
- Assert exit status or parsed state, never diagnostic message text.
- Do not invoke the complete conformance suite from this story.
