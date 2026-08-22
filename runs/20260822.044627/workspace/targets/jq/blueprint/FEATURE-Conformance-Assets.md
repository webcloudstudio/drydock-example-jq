# FEATURE: Conformance Assets

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Stage and validate the immutable jq conformance assets. |
| Depends On  | ARCHITECTURE.md |
| Provides    | staged conformance corpus, exclusions, runner, scoring script |
| Consumes    | none |

## Workflow

Place the supplied conformance sources under `sources/` without modification. Validate the
harness in process by importing its corpus and exclusion parsers, confirming the pinned corpus
parses completely and every declared exclusion matches a corpus case. This story verifies staging
only and does not claim interpreter behavior.

## Programmatic Acceptance

=== AC conformance-assets ===
Intent: The staged corpus and exclusions parse successfully and remain mutually consistent with the pinned authoritative assets.
Requires: executable=python3; scope=test

import sys

sys.path.insert(0, "sources")
import run_conformance as harness

cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
excluded = harness.apply_exclusions(
    cases,
    harness.parse_exclusions(harness.EXCLUSIONS),
)
assert len(cases) == 550
assert len(excluded) == 13
=== END AC conformance-assets ===

=== AC conformance-source-integrity ===
Intent: The staged harness exposes the required corpus and exclusion paths and can be imported from the build directory.
Requires: executable=python3; scope=test

from pathlib import Path
import sys

sources = Path("sources")
assert (sources / "jq.test").is_file()
assert (sources / "exclusions.txt").is_file()
assert (sources / "run_conformance.py").is_file()
sys.path.insert(0, str(sources))
import run_conformance
assert run_conformance.CORPUS == sources / "jq.test"
assert run_conformance.EXCLUSIONS == sources / "exclusions.txt"
=== END AC conformance-source-integrity ===

## User Acceptance

- None.

## Guardrails

- Do not modify, regenerate, trim, or substitute any file under `sources/`.
- Module-loader cases remain excluded only through the supplied exclusions file.
