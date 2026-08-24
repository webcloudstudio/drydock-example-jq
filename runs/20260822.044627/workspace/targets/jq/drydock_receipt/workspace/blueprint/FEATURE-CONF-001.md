# FEATURE: Conformance Asset Staging

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Stages and validates the immutable jq conformance assets. |
| Depends On  | ARCHITECTURE.md |
| Provides    | sources/ conformance corpus, manual, grammar, harness, exclusions, full-test script |
| Consumes    | target application root |

## Workflow

The supplied source assets are staged byte-for-byte beneath `sources/`. The harness parser is imported directly to validate corpus structure and exclusion consistency without launching the candidate interpreter.

## Programmatic Acceptance

=== AC conf-001-assets ===
Intent: The staged corpus parses into the authoritative case set and all declared exclusions match cases.
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
assert harness.CORPUS.is_file()
assert harness.EXCLUSIONS.is_file()
=== END AC conf-001-assets ===

## User Acceptance

- None.

## Guardrails

- The supplied scoring assets remain read-only and are never modified, rewritten, filtered, or substituted.
