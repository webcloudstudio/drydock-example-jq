# Evidence: Block 21 · Service (block-21)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 53812
- execution id: 20260823.031407.736Z-316a0d1a

## Stories built
- Implement reductions and iteration controls. (FLOW-005) [story]

## Acceptance tooling authorization
- FEATURE-FLOW-005.md#flow-005-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-FLOW-005.md (SP 503)
- context: builtin.jq (SP 2408)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- tests/test_flow_005_reductions_iteration.py

## Pre-build acceptance observation
- RED: flow-005-conformance (FEATURE-FLOW-005.md)
  intent: The executable passes the authoritative conformance cases exercising reductions and iteration controls.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 50,
        "fail": 2,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 1205,
          "program": "pick(first)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1]"
          ],
          "actual": []
        },
        {
          "line": 1209,
          "program": "pick(first|first)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[[10]]"
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=50 fail=2 error=0 skip=0 total=52 from=tally
    --- drydock: end progress ---
    --- drydock: values at failure ---
      tally = {'pass': 50, 'fail': 2, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "flow-005-conformance.py", line 18, in <module>
        assert tally["fail"] == 0 and tally["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: flow-005-conformance (FEATURE-FLOW-005.md)
  intent: The executable passes the authoritative conformance cases exercising reductions and iteration controls.
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
        "pass": 52,
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
- tests/test_flow_005_reductions_iteration.py

SUMMARY:
Implemented projection-aware `first` path handling for `pick`, with reduction/iteration regression coverage.

Verification:
- FLOW-005 conformance: 52 passed, 0 failed, 0 errored
- Pytest: 101 passed

BLOCKERS:
- None
