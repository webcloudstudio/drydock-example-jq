# Evidence: Block 8 · Service (block-8)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 23240
- execution id: 20260817.182245.537Z-fa765ab9

## Stories built
- Implement jq indexing, iteration, optional access, and slicing. (core-indexing) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Core-Indexing.md (SP 944)
- context: parser.y (SP 5596)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_generators.py

## Pre-build acceptance observation
- GREEN (prepassed): indexing-object-field (FEATURE-Core-Indexing.md)
  intent: Object field access returns the value associated with the requested key.
  return code: 0
- GREEN (prepassed): indexing-iteration (FEATURE-Core-Indexing.md)
  intent: Array iteration emits each element in order.
  return code: 0
- GREEN (prepassed): indexing-negative-index (FEATURE-Core-Indexing.md)
  intent: Negative indexing selects from the end of an array.
  return code: 0
- GREEN (prepassed): indexing-slice (FEATURE-Core-Indexing.md)
  intent: Array slicing returns the requested half-open range.
  return code: 0
- GREEN (prepassed): indexing-optional-access (FEATURE-Core-Indexing.md)
  intent: Optional access suppresses an invalid indexing operation.
  return code: 0

## Post-build programmatic acceptance
- PASS: indexing-object-field (FEATURE-Core-Indexing.md)
  intent: Object field access returns the value associated with the requested key.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: indexing-iteration (FEATURE-Core-Indexing.md)
  intent: Array iteration emits each element in order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: indexing-negative-index (FEATURE-Core-Indexing.md)
  intent: Negative indexing selects from the end of an array.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: indexing-slice (FEATURE-Core-Indexing.md)
  intent: Array slicing returns the requested half-open range.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: indexing-optional-access (FEATURE-Core-Indexing.md)
  intent: Optional access suppresses an invalid indexing operation.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_generators.py

SUMMARY:
Implemented jq indexing, iteration, optional access, negative indices, and slicing. All 32 tests and 5 declared acceptance checks pass.

BLOCKERS:
- None
