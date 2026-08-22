# FEATURE: Full Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Verify the completed jq interpreter against the complete supplied conformance suite. |
| Depends On  | FEATURE-Scoped-Conformance.md |
| Provides    | complete jq conformance verification |
| Consumes    | scoped conformance verification |

## Intent

This terminal verification assembles the completed interpreter and invokes the supplied scoring entry point from the application root. The full suite is the release acceptance verdict after all implementation and staging stories have completed.

## Behavior

- `sources/full_test.sh` is invoked unchanged.
- The completed executable is checked and exercised by the supplied runner.
- The full corpus is executed exactly once by this terminal story.
- The story passes only when the scoring command exits successfully.

## Programmatic Acceptance

=== AC full-conformance ===
Intent: The completed interpreter passes the supplied full conformance scoring entry point.
Suite: full
Requires: executable=sh; scope=test

import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC full-conformance ===

=== AC full-conformance-exit ===
Intent: The terminal scoring command returns the successful process status required by the project contract.

import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC full-conformance-exit ===

## User Acceptance

- None.

## Guardrails

- This is the sole story permitted to run the unscoped corpus.
- Do not alter `sources/full_test.sh`, `sources/run_conformance.py`, `sources/jq.test`, or `sources/exclusions.txt`.
- Treat the command exit status as the acceptance verdict.
