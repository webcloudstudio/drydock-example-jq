# Evidence: Block 33 · Service (block-33)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 53757
- execution id: 20260823.043810.706Z-eb6692b5

## Stories built
- Implement object-entry and containment builtins. (DATA-003) [story]

## Acceptance tooling authorization
- FEATURE-DATA-003.md#data-003-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-DATA-003.md (SP 447)
- context: builtin.jq (SP 2408)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_data_003_entries_containment.py

## Pre-build acceptance observation
- RED: data-003-conformance (FEATURE-DATA-003.md)
  intent: The object-entry, key, membership, and containment slice executes matching corpus cases and passes all selected cases.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 24,
        "fail": 2,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 1713,
          "program": "to_entries",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "[{\"key\":\"a\", \"value\":1}, {\"key\":\"b\", \"value\":2}]"
          ],
          "actual": []
        },
        {
          "line": 1717,
          "program": "from_entries",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "{\"a\": 1, \"b\": 2, \"c\": 3, \"d\": 4}"
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=24 fail=2 error=0 skip=0 total=26 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 24, 'fail': 2, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "data-003-conformance.py", line 18, in <module>
        assert summary["fail"] == 0
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: data-003-conformance (FEATURE-DATA-003.md)
  intent: The object-entry, key, membership, and containment slice executes matching corpus cases and passes all selected cases.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 26,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_data_003_entries_containment.py

SUMMARY:
Implemented `keys_unsorted`, `in`, `inside`, `to_entries`, and `from_entries`; corrected key handling and builtin registration. Added focused tests.

Verification: 149 tests passed; DATA-003 conformance passed 26/26 with zero failures/errors.

BLOCKERS:
- None
