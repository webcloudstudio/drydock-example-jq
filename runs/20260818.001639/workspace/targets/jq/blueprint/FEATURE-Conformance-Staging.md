# FEATURE: Conformance Staging

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Stages the supplied jq conformance assets and proves the harness can enumerate them. |
| Depends On  | ARCHITECTURE.md |
| Provides    | `sources/jq.test`, `sources/run_conformance.py`, `sources/full_test.sh`, `sources/exclusions.txt` |
| Consumes    | — |

## Workflow

The build copies the supplied conformance assets into the application root under `sources/` without modification. The staging story verifies that the corpus parses, exclusions are valid, and the harness starts in list mode with the required `JQ` environment variable.

## Programmatic Acceptance

=== AC conformance-assets ===
Intent: The supplied conformance harness enumerates the complete corpus and applies declared exclusions.

import os
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": str(root / "jq")},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0

import runpy
runner = runpy.run_path("sources/run_conformance.py")
corpus = runner["parse_corpus"]((root / "sources/jq.test").read_text(encoding="utf-8"))
excluded = runner["apply_exclusions"](
    corpus,
    runner["parse_exclusions"](root / "sources/exclusions.txt"),
)
listed = [line for line in result.stdout.splitlines() if line.startswith(("run ", "skip "))]
assert len(listed) == len(corpus)
assert sum(line.startswith("skip ") for line in listed) == len(excluded)
=== END AC conformance-assets ===

## User Acceptance

- None.

## Guardrails

- Copy every staged asset verbatim.
- Never edit, filter, regenerate, or trim files under `sources/`.
- List mode is used only for staging verification and must execute no corpus case.
