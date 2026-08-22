# FEATURE: Complete Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Runs the complete jq conformance corpus as the terminal release verification. |
| Depends On  | FEATURE-IO-003.md, FEATURE-CONF-002.md |
| Provides    | complete jq conformance release verification |
| Consumes    | ./jq, sources/full_test.sh |

## Workflow

As the terminal verification, this story runs the supplied `sources/full_test.sh` without filtering or reinterpretation. The script validates the executable boundary and runs the complete non-excluded corpus.

## Programmatic Acceptance

=== AC conf-003-full-suite ===
Intent: The supplied complete conformance suite passes with a successful exit status.
Suite: full

import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
=== END AC conf-003-full-suite ===

## User Acceptance

- None.

## Guardrails

- This is the only story that runs the complete corpus.
- The scoring script and its exit status are authoritative; its output is diagnostic only.
