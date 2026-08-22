# FEATURE: CLI Harness

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Stages and validates the supplied jq conformance assets without modifying or executing the candidate. |
| Depends On  | ARCHITECTURE.md |
| Provides    | staged conformance corpus, exclusions, runner, scoring entry point |
| Consumes    | interpreter architecture |

## Intent

Stage every supplied source asset byte-for-byte under `sources/`, preserving the authoritative corpus, exclusions, runner, scoring script, manual, grammar, lexer, and builtin reference. Validate corpus parsing and exclusion consistency by importing the harness directly; this story does not execute the candidate interpreter.

## Programmatic Acceptance

=== AC cli-harness-assets ===
Intent: The staged conformance corpus parses completely and all declared exclusions match corpus cases.
Requires: executable=python3; scope=test

import sys

sys.path.insert(0, "sources")
import run_conformance as harness

expected_cases = 550
expected_exclusions = 13
cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
excluded = harness.apply_exclusions(
    cases,
    harness.parse_exclusions(harness.EXCLUSIONS),
)
assert len(cases) == expected_cases
assert len(excluded) == expected_exclusions

=== END AC cli-harness-assets ===

=== AC cli-harness-parser ===
Intent: The staged runner exposes the required corpus and exclusion parser interfaces.
Requires: executable=python3; scope=test

import sys

sys.path.insert(0, "sources")
import run_conformance as harness

cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
exclusions = harness.parse_exclusions(harness.EXCLUSIONS)
excluded = harness.apply_exclusions(cases, exclusions)
assert cases
assert exclusions
assert excluded
assert all(case.program for case in cases)

=== END AC cli-harness-parser ===

## User Acceptance

- None.

## Guardrails

- Preserve all supplied files byte-for-byte under `sources/`.
- Do not invoke the candidate interpreter in this staging story.
- Do not invoke list, dry-run, or whole-suite harness modes from any other non-terminal story.
