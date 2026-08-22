# FEATURE: Conformance Asset Staging

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Stage and validate the immutable jq conformance assets required by the build. |
| Depends On  | — |
| Provides    | staged sources/* assets, parsed corpus and exclusions |
| Consumes    | — |

## Purpose

Make the supplied manual, corpus, parser and lexer references, builtin reference, exclusions, runner, and full-test script available under `sources/` in the application root without modification.

## Behavior

- All imported source assets are copied byte-for-byte to their declared `sources/` paths.
- The supplied harness imports successfully.
- The corpus parses into its authoritative case set.
- Every exclusion matches at least one corpus case.
- This story validates staging only and does not execute candidate conformance cases.

## Programmatic Acceptance

=== AC staging-assets ===
Intent: The staged harness parses the corpus and applies every declared exclusion successfully.
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
=== END AC staging-assets ===

=== AC staging-harness-import ===
Intent: The staged harness exposes the required corpus and exclusion paths.
from pathlib import Path
import sys

sys.path.insert(0, "sources")
import run_conformance as harness

assert harness.CORPUS.is_file()
assert harness.EXCLUSIONS.is_file()
assert Path("sources/full_test.sh").is_file()
assert Path("sources/jq.test").is_file()
=== END AC staging-harness-import ===

=== AC staging-readonly-assets ===
Intent: The staged scoring assets retain their required executable and readable forms.
from pathlib import Path

assert Path("sources/full_test.sh").stat().st_mode & 0o111
assert Path("sources/run_conformance.py").read_text(encoding="utf-8")
assert Path("sources/jq-manual.txt").read_text(encoding="utf-8")
assert Path("sources/parser.y").read_text(encoding="utf-8")
assert Path("sources/lexer.l").read_text(encoding="utf-8")
=== END AC staging-readonly-assets ===

## User Acceptance

- None.

## Guardrails

- Never modify, trim, regenerate, or substitute any file under `sources/`.
- Do not launch the conformance harness from this staging story.
- Preserve the supplied corpus and exclusion data verbatim.
- The staged assets are read-only scoring inputs.
