# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-20
- resulting state: closed/verified
- story points (combined assembled cost): 69782
- execution id: 20260821.002520.731Z-944141c5

## Stories built
- Stage the pinned jq source and scoring assets. (FOUNDATION-001) [story]

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-FOUNDATION-001.md (SP 515)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: builtin.jq (SP 2408)
- context: run_conformance.py (SP 4354)
- context: full_test.sh (SP 189)
- context: exclusions.txt (SP 654)
- stack: common.md (SP 1807)
- stack: python.md (SP 3892)

## Build directory changes
- tests/test_foundation_assets.py

## Pre-build acceptance observation
- GREEN (prepassed): foundation-assets-parse (FEATURE-FOUNDATION-001.md)
  intent: The staged corpus parses into the authoritative case set and every declared exclusion matches a case.
  return code: 0
- GREEN (prepassed): foundation-assets-consistent (FEATURE-FOUNDATION-001.md)
  intent: The staged harness assets retain their required parser and scoring interfaces.
  return code: 0

## Post-build programmatic acceptance
- PASS: foundation-assets-parse (FEATURE-FOUNDATION-001.md)
  intent: The staged corpus parses into the authoritative case set and every declared exclusion matches a case.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: foundation-assets-consistent (FEATURE-FOUNDATION-001.md)
  intent: The staged harness assets retain their required parser and scoring interfaces.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- tests/test_foundation_assets.py

SUMMARY:
Staged assets verified: 550 cases, 13 exclusions, required interfaces present. Added and passed two regression tests. Conformance corpus was not executed per staging-story rules.

BLOCKERS:
- None
