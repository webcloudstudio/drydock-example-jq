# FEATURE: Supplied Conformance Asset Staging

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Stage the supplied jq specifications and conformance harness assets without modification. |
| Depends On  | ARCHITECTURE.md |
| Provides    | sources/ conformance corpus and harness |
| Consumes    | none |

## Purpose

Copy every imported source asset into the application root under `sources/`, preserving its contents and required layout. The staged assets include the manual, corpus, grammar, lexer, reference builtin source, exclusions, conformance runner, and scoring script. The implementation must not rewrite, filter, or reinterpret these files.

## Programmatic Acceptance

=== AC verify-001-harness-list ===
Intent: The staged conformance runner can parse the staged corpus and exclusions without a harness error.

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", r"^\.$"],
    capture_output=True,
    text=True,
    env={**os.environ},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC verify-001-harness-list ===

=== AC verify-001-script-contract ===
Intent: The staged scoring script is executable by POSIX sh and reaches the candidate interface check.

import os
import subprocess
import sys

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    input="",
    capture_output=True,
    text=True,
    env={**os.environ},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode in (0, 1)
=== END AC verify-001-script-contract ===

## User Acceptance

- None.

## Guardrails

- Preserve all supplied source assets byte-for-byte.
- Do not modify the corpus, exclusions, runner, or scoring script.
- Keep all staged assets beneath `sources/`.
