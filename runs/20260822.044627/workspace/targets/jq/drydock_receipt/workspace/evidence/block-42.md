# Evidence: Block 42 · Service (block-42)

- block type: block
- date: 2026-08-23
- resulting state: closed/verified
- story points (combined assembled cost): 10994
- execution id: 20260823.115639.033Z-7ca6d4e4

## Stories built
- Provide scoped conformance verification. (CONF-002) [story]

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-CONF-002.md (SP 315)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- tests/test_conf_002_acceptance.py

## Pre-build acceptance observation
- GREEN (prepassed): conf-002-scoped-run (FEATURE-CONF-002.md)
  intent: The scoped verification assets expose the candidate binding and machine-readable selector contracts.
  return code: 0

## Post-build programmatic acceptance
- PASS: conf-002-scoped-run (FEATURE-CONF-002.md)
  intent: The scoped verification assets expose the candidate binding and machine-readable selector contracts.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- tests/test_conf_002_acceptance.py

SUMMARY:
Added scoped conformance acceptance tests. Verified 22 selected `reduce` cases pass and all 19 project tests pass. Staged sources remain unchanged.

BLOCKERS:
- None
