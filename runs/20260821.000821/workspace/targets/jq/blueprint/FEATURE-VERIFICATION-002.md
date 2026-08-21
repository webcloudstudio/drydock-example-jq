# FEATURE: Complete Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provides terminal verification against the complete supplied jq conformance corpus. |
| Depends On  | FEATURE-VERIFICATION-001.md |
| Provides    | complete jq conformance release verification |
| Consumes    | executable jq, staged conformance assets, all implemented capabilities |

## Purpose

Run the supplied scoring entry point as the terminal release gate after all implementation stories have completed.

## Behavior

The terminal verification executes `sh sources/full_test.sh` from the application root. The supplied script performs the executable check and invokes the complete conformance corpus with the candidate bound through `JQ`. Captured output is printed for diagnosis; the script's exit status is the sole verdict.

## Programmatic Acceptance

=== AC verification-002-full ===
Intent: The completed interpreter passes the supplied complete conformance corpus and release script.
Suite: full
Requires: executable=sh; scope=test
Requires: executable=python3; scope=test

import os
import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
    env={**os.environ},
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
=== END AC verification-002-full ===

## User Acceptance

- None.

## Guardrails

- This is the only story that runs the unfiltered corpus.
- Do not alter, filter, skip, or reinterpret the supplied scoring script.
- Treat the script exit status as the release verdict; diagnostics are informational only.
