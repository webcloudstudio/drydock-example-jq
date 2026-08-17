# FEATURE: Conformance Staging

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Preserve and validate the supplied jq conformance assets and harness. |
| Depends On  | — |
| Provides    | Staged conformance corpus and harness |
| Consumes    | — |

## Purpose

The supplied conformance assets are staged unchanged under `sources/` in the application root. The staging boundary preserves the corpus, exclusions, runner, scoring script, and normative reference files for implementation and final verification.

## Asset Contract

The following files remain byte-for-byte supplied assets:

- `sources/jq.test`
- `sources/exclusions.txt`
- `sources/run_conformance.py`
- `sources/full_test.sh`
- `sources/jq-manual.txt`
- `sources/parser.y`
- `sources/lexer.l`
- `sources/builtin.jq`

The harness is invoked with `JQ` set to the application executable. List mode must enumerate the corpus without executing candidate cases.

## Programmatic Acceptance

=== AC conformance-staging-list ===
Intent: The staged conformance harness parses and enumerates its corpus successfully without executing cases.

import os
import subprocess
import sys
from pathlib import Path

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": str(Path.cwd() / "jq")},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0

source = Path("sources/run_conformance.py").read_text(encoding="utf-8")
assert "def parse_corpus" in source
=== END AC conformance-staging-list ===

## User Acceptance

- None.

## Guardrails

- Do not modify, regenerate, trim, or substitute any file under `sources/`.
- Do not invoke the candidate through a system jq executable or third-party implementation.
