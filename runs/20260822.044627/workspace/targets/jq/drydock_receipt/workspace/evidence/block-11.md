# Evidence: Block 11 · Service (block-11)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 51215
- execution id: 20260823.022510.696Z-432b7141

## Stories built
- Implement empty, runtime errors, optional evaluation, and try. (CORE-003) [story]

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-CORE-003.md (SP 319)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- tests/test_core_003_errors.py

## Pre-build acceptance observation
- GREEN (prepassed): core-003-conformance (FEATURE-CORE-003.md)
  intent: The executable evaluates optional errors and try/catch while preserving runtime failure distinction.
  return code: 0

## Post-build programmatic acceptance
- PASS: core-003-conformance (FEATURE-CORE-003.md)
  intent: The executable evaluates optional errors and try/catch while preserving runtime failure distinction.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- `jq_interpreter/evaluator.py`
- `tests/test_core_003_errors.py`

SUMMARY:
Implemented CORE-003 runtime error handling and lazy `nth` evaluation. Added tests for empty, optional suppression, try/catch, runtime exit status, partial output, and generator errors.

Verification: 51 tests passed; focused conformance: 134 passed, 0 failed, 0 errored, 1 skipped.

BLOCKERS:
- None
