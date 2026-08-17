# FEATURE: Complete jq Conformance Gate

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Assemble the completed interpreter and verify it against the entire supplied jq conformance corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-001.md, FEATURE-CLI-002.md, FEATURE-FRONTEND-001.md, FEATURE-FRONTEND-002.md, FEATURE-FRONTEND-003.md, FEATURE-EVAL-001.md, FEATURE-EVAL-002.md, FEATURE-EVAL-003.md, FEATURE-DATA-001.md, FEATURE-DATA-002.md, FEATURE-DATA-003.md, FEATURE-BUILTIN-001.md, FEATURE-BUILTIN-002.md, FEATURE-BUILTIN-003.md, FEATURE-BUILTIN-004.md, FEATURE-BUILTIN-005.md, FEATURE-VERIFY-001.md, FEATURE-VERIFY-002.md |
| Provides    | complete jq conformance verdict |
| Consumes    | ./jq -c, staged conformance assets |

## Purpose

Run the supplied scoring entry point against the finished executable. The complete corpus is authoritative for project correctness; exclusions remain exactly those declared by the supplied exclusions file. Repair implementation defects until the scoring command exits successfully.

## Programmatic Acceptance

=== AC verify-003-full-conformance ===
Intent: The finished interpreter passes the complete supplied jq conformance gate.
Suite: full

import os
import subprocess
import sys

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
    env={**os.environ},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC verify-003-full-conformance ===

## User Acceptance

- None.

## Guardrails

- `sh sources/full_test.sh` is the sole complete-suite acceptance command.
- Do not edit or bypass the supplied corpus, exclusions, runner, or scoring script.
- Do not assert on summary text or case counts.
