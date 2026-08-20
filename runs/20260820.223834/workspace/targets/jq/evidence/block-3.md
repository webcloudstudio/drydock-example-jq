# Evidence: Block 3 · Foundational (block-3)

- block type: block
- date: 2026-08-20
- resulting state: closed/verified
- story points (combined assembled cost): 66922
- execution id: 20260820.230338.946Z-42c5a9ce

## Stories built
- Stage and validate the authoritative conformance assets. (delivery-assets) [story]

## Reusable compacts
- run_conformance_compact.md
- jq_compact.md
- exclusions_compact.md
- full_test_compact.md

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-Delivery-Assets.md (SP 539)
- context: run_conformance.py (SP 4354)
- context: jq.test (SP 13058)
- context: exclusions.txt (SP 654)
- context: full_test.sh (SP 189)
- context: jq-manual.txt (SP 32696)
- context: lexer.l (SP 1137)
- context: parser.y (SP 5596)
- context: builtin.jq (SP 2408)
- context: ARCHITECTURE_compact.md (SP 100)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)

## Build directory changes
- tests/test_delivery_assets.py

## Pre-build acceptance observation
- GREEN (prepassed): assets-parse (FEATURE-Delivery-Assets.md)
  intent: The staged corpus and exclusions parse into the expected authoritative records.
  return code: 0
- GREEN (prepassed): assets-harness-import (FEATURE-Delivery-Assets.md)
  intent: The staged harness exposes its corpus and exclusion interfaces without launching a candidate.
  return code: 0

## Post-build programmatic acceptance
- PASS: assets-parse (FEATURE-Delivery-Assets.md)
  intent: The staged corpus and exclusions parse into the expected authoritative records.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: assets-harness-import (FEATURE-Delivery-Assets.md)
  intent: The staged harness exposes its corpus and exclusion interfaces without launching a candidate.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="run_conformance.py">
Parses jq.test cases and exclusions via parse_corpus, parse_exclusions, and apply_exclusions. Runs candidate from JQ, comparing structured JSON outputs. Candidate compile errors use exit 3; runtime errors use exit 5.
</reusable-compact>

<reusable-compact filename="jq.test">
Authoritative jq 1.8.2 corpus: cases contain program, input, and expected output lines; %%FAIL cases require compile rejection. Parsed corpus count is 550.
</reusable-compact>

<reusable-compact filename="exclusions.txt">
Contains 13 verbatim module-loader case programs excluded because fixture trees are unavailable. Every exclusion must match a corpus case; stale entries are hard errors.
</reusable-compact>

<reusable-compact filename="full_test.sh">
Requires executable ./jq, sets JQ to the application executable, and runs the complete conformance harness from the application root.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- tests/test_delivery_assets.py

SUMMARY:
Staged assets validated directly: 550 corpus cases and 13 exclusions. Harness interfaces passed import checks. Added and ran deterministic unittest coverage; all 4 tests passed.

BLOCKERS:
- None
