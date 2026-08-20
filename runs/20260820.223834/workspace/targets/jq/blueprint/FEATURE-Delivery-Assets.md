# FEATURE: Delivery Assets

| Field       | Value |
|-------------|-------|
| Version     | 20260820 V1 |
| Description | Stages and validates the authoritative jq conformance assets. |
| Depends On  | METADATA.md, ARCHITECTURE.md |
| Provides    | staged sources and validated corpus |
| Consumes    | sources/run_conformance.py, sources/jq.test, sources/exclusions.txt |

## Scope

The application root contains the supplied assets under `sources/`, preserved verbatim:

- `INSTRUCTIONS.md`
- `run_conformance.py`
- `jq.test`
- `exclusions.txt`
- `full_test.sh`
- `jq-manual.txt`
- `lexer.l`
- `parser.y`
- `builtin.jq`

The harness is imported directly for staging validation. It is not launched by this story.

## Validation Contract

The corpus parser must produce the pinned corpus cases, and every exclusion must match a corpus program. The expected authoritative records are 550 parsed cases and 13 excluded cases. Source assets are read-only after staging.

## Programmatic Acceptance

=== AC assets-parse ===
Intent: The staged corpus and exclusions parse into the expected authoritative records.

import sys
from pathlib import Path

sys.path.insert(0, "sources")
import run_conformance as harness

cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
excluded = harness.apply_exclusions(
    cases, harness.parse_exclusions(harness.EXCLUSIONS)
)
assert len(cases) == 550
assert len(excluded) == 13
=== END AC assets-parse ===

=== AC assets-harness-import ===
Intent: The staged harness exposes its corpus and exclusion interfaces without launching a candidate.

import sys
from pathlib import Path

sys.path.insert(0, "sources")
import run_conformance as harness

assert harness.CORPUS.is_file()
assert harness.EXCLUSIONS.is_file()
assert callable(harness.parse_corpus)
assert callable(harness.apply_exclusions)
=== END AC assets-harness-import ===

## User Acceptance

- None.

## Guardrails

- Preserve every staged source asset byte-for-byte.
- Never modify, filter, reinterpret, or regenerate the supplied corpus, exclusions, harness, or scoring script.
- Do not invoke the conformance runner from this staging story.
