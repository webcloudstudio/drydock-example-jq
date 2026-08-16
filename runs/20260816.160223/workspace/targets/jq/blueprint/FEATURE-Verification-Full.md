# FEATURE: Full Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Prove the completed interpreter against the complete supplied jq conformance corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-Entrypoint.md, FEATURE-CLI-Errors.md, FEATURE-Frontend-Validation.md, FEATURE-Eval-Cartesian.md, FEATURE-Values-Comparison.md, FEATURE-Control-Recursion.md, FEATURE-Language-Alternation.md, FEATURE-Paths-Assignment.md, FEATURE-Builtins-Utilities.md, FEATURE-Verification-Assets.md |
| Provides    | full conformance acceptance |
| Consumes    | executable jq and all interpreter capabilities |

## Scope

Run the supplied acceptance command from the completed application root:

`sh sources/full_test.sh`

This is the sole full-suite release gate. It must execute the unmodified corpus and exclusions, preserve diagnostics for investigation, and use the harness exit status as the verdict.

## Programmatic Acceptance

=== AC full-conformance ===
Intent: The completed executable passes the complete supplied jq 1.8.2 conformance suite.

Suite: full
Requires: executable=sh; scope=test
Requires: executable=python3; scope=test

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

## User Acceptance

- None.

## Guardrails

- This is the only story acceptance that runs the complete suite.
- Do not assert on summary text, case counts, stdout contents, or stderr wording.
- Do not modify the supplied corpus, exclusions, runner, or scoring script.
- The release verdict is the supplied harness exit status.
