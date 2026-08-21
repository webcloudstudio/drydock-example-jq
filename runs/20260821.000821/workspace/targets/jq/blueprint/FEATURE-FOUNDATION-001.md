# FEATURE: Foundation Source Staging

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Stages the pinned jq specifications and conformance assets without modification. |
| Depends On  | — |
| Provides    | staged jq source and conformance assets |
| Consumes    | — |

## Scope

This capability stages the declared jq manual, grammar, lexer, builtin reference, conformance corpus, exclusions, and harness assets byte-for-byte under `sources/`. The staged assets remain read-only scoring inputs.

## Programmatic Acceptance

=== AC foundation-assets-parse ===
Intent: The staged corpus parses into the authoritative case set and every declared exclusion matches a case.

import sys

sys.path.insert(0, "sources")
import run_conformance as harness

EXPECTED_CASES = 550
EXPECTED_EXCLUSIONS = 13

cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
excluded = harness.apply_exclusions(cases, harness.parse_exclusions(harness.EXCLUSIONS))
assert len(cases) == EXPECTED_CASES
assert len(excluded) == EXPECTED_EXCLUSIONS
=== END AC foundation-assets-parse ===

=== AC foundation-assets-consistent ===
Intent: The staged harness assets retain their required parser and scoring interfaces.

from pathlib import Path
import sys

sources = Path("sources")
required = [
    "jq-manual.txt",
    "jq.test",
    "parser.y",
    "lexer.l",
    "builtin.jq",
    "run_conformance.py",
    "full_test.sh",
    "exclusions.txt",
]
assert all((sources / name).is_file() for name in required)

sys.path.insert(0, str(sources))
import run_conformance as harness

assert callable(harness.parse_corpus)
assert callable(harness.parse_exclusions)
assert callable(harness.apply_exclusions)
=== END AC foundation-assets-consistent ===

## User Acceptance

- The supplied source and scoring assets are available for implementation and verification.

## Guardrails

- Do not modify, regenerate, trim, substitute, or execute the conformance corpus from this staging story.
- Preserve the supplied assets byte-for-byte.
