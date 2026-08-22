# FEATURE: Complete Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Verify the completed interpreter against the full supplied jq conformance corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-Scoped-Conformance.md |
| Provides    | complete conformance release verification |
| Consumes    | ./jq -c program execution, supplied scoring script |

## Workflow

After every implementation and staging story has completed, run the supplied
`sources/full_test.sh` from the application root. This is the sole whole-corpus verification.
The story succeeds only when the script exits zero; captured output is printed for diagnosis and
is not itself used as an oracle.

## Programmatic Acceptance

=== AC complete-conformance ===
Intent: The completed executable passes the supplied full jq conformance suite.
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
=== END AC complete-conformance ===

## User Acceptance

- None.

## Guardrails

- This is the only story that runs the whole corpus.
- Do not modify the supplied scoring script, runner, corpus, or exclusions.
- Release acceptance is determined by the scoring command's exit status.
