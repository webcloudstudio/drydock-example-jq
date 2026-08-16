# Evidence: Block 7 · Service (block-7)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 25014
- execution id: 20260816.164045.261Z-9332c9d6

## Stories built
- Implement jq core composition and indexing operators. (eval-core) [story]

## Stacked context
- compass: COMPASS.md (SP 3787)
- implements: FEATURE-Eval-Core.md (SP 873)
- context: parser.y (SP 5596)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 126)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_evaluator.py
- jq_parser.py
- tests/test_eval_core.py

## Pre-build acceptance observation
- GREEN (prepassed): eval-core-identity (FEATURE-Eval-Core.md)
  intent: Identity and literal filters return their input-derived and constant values.
  return code: 0
- GREEN (prepassed): eval-core-collection (FEATURE-Eval-Core.md)
  intent: Collection gathers all outputs of a generator into one array.
  return code: 0
- RED: eval-core-indexing (FEATURE-Eval-Core.md)
  intent: Field, computed index, and iteration access the corresponding input values.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      actual = ['jq', None, [[4, 5], 'jq']]
      input_value = {'items': [4, 5], 'name': 'jq'}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "eval-core-indexing.py", line 15, in <module>
        assert actual[1] == input_value["items"][1]
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): eval-core-slices (FEATURE-Eval-Core.md)
  intent: Array and string slicing follows jq's bounds and ordering semantics.
  return code: 0

## Post-build programmatic acceptance
- PASS: eval-core-identity (FEATURE-Eval-Core.md)
  intent: Identity and literal filters return their input-derived and constant values.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: eval-core-collection (FEATURE-Eval-Core.md)
  intent: Collection gathers all outputs of a generator into one array.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: eval-core-indexing (FEATURE-Eval-Core.md)
  intent: Field, computed index, and iteration access the corresponding input values.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: eval-core-slices (FEATURE-Eval-Core.md)
  intent: Array and string slicing follows jq's bounds and ordering semantics.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_evaluator.py
- jq_parser.py
- tests/test_eval_core.py

SUMMARY:
Implemented base-aware field/index/iteration/slice evaluation, optional access behavior, and empty array literals. Added core tests. Project suite: 30 passed.

BLOCKERS:
- Full conformance remains incomplete due to later build blocks’ missing builtins, assignments, and control-flow features.
