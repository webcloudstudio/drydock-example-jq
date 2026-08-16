# FEATURE: Full Conformance

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Gate the completed jq interpreter against the complete supplied jq 1.8.2 conformance corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-Executable.md, FEATURE-Focused-Verification.md |
| Provides    | complete jq conformance verdict |
| Consumes    | ./jq executable and supplied scoring script |

## Purpose

This feature performs the terminal verification of the completed standalone jq interpreter. It invokes the supplied scoring entry point exactly as authored, preserving the corpus, exclusions, harness, and diagnostics.

The full suite is the project-level definition of done for the interpreter. Its exit status is the sole verdict; the suite’s printed summary is diagnostic output only.

## Workflow

1. Confirm all implementation and verification stories are complete.
2. Run `sh sources/full_test.sh` from the application root.
3. Preserve the command’s stdout and stderr for diagnosis.
4. Accept the feature only when the command exits successfully.

## Operational Requirements

- Do not modify `sources/full_test.sh`, `sources/run_conformance.py`, `sources/jq.test`, or `sources/exclusions.txt`.
- Do not filter, reinterpret, or selectively rerun corpus cases during the full gate.
- The executable must remain `./jq` and must be executable.
- The full gate must run without network access, package installation, or third-party jq implementations.

## Programmatic Acceptance

=== AC full-conformance ===
Intent: The completed interpreter passes the supplied full jq conformance suite.
Suite: full
Requires: executable=python3; scope=test
Requires: executable=sh; scope=test

import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=subprocess.sys.stderr)
assert result.returncode == 0
=== END AC full-conformance ===

## User Acceptance

- None.

## Guardrails

- The supplied scoring script and corpus remain unmodified.
- The complete suite runs only after all implementation stories and focused verification close.
- The suite exit status is the only acceptance oracle; summary text is never asserted.
