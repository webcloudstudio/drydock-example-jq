# Evidence: Block 31 · Service (block-31)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 53741
- execution id: 20260823.042455.513Z-305e685e

## Stories built
- Implement collection transformation builtins. (DATA-001) [story]

## Acceptance tooling authorization
- FEATURE-DATA-001.md#data-001-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-DATA-001.md (SP 436)
- context: builtin.jq (SP 2408)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
- jq_interpreter/parser.py
- jq_interpreter/runtime.py

## Pre-build acceptance observation
- RED: data-001-conformance (FEATURE-DATA-001.md)
  intent: The collection transformation slice executes matching corpus cases and passes all selected cases.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 33,
        "fail": 7,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 455,
          "program": "flatten(3,2,1)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0,1,2,3]",
            "[0,1,2,[3]]",
            "[0,1,[2],[[3]]]"
          ],
          "actual": [
            "[3,2,1,0]"
          ]
        },
        {
          "line": 1795,
          "program": "flatten",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "[0, 1, 2, 3]"
          ],
          "actual": []
        },
        {
          "line": 1803,
          "program": "flatten(2)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0, 1, 2, [3]]"
          ],
          "actual": [
            "[[3],2,1,0]"
          ]
        },
        {
          "line": 1807,
          "program": "flatten(2)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[0, 1, 2, 1, [3], 2]"
          ],
          "actual": [
            "[[3],2,1,2,1,0]"
          ]
        },
        {
          "line": 1815,
          "program": "transpose",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "[[1,2],[null,3]]"
          ],
          "actual": []
        },
        {
          "line": 1819,
          "program": "transpose",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "[]"
          ],
          "actual": []
        },
        {
          "line": 2267,
          "program": "map(abs)",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[1e-1, 1000000000000000002]"
          ],
          "actual": [
            "[0.1,1000000000000000000]"
          ]
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=33 fail=7 error=0 skip=0 total=40 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 33, 'fail': 7, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "data-001-conformance.py", line 18, in <module>
        assert summary["fail"] == 0
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: data-001-conformance (FEATURE-DATA-001.md)
  intent: The collection transformation slice executes matching corpus cases and passes all selected cases.
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
        "pass": 40,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Repair attempts
- attempt 0 (initial build): failed; 1/1 checks model=gpt-5.6-luna; execution 20260823.041750.880Z-11477ccd; reason: acceptance regression: parse-003-conformance, parse-004-conformance, value-001-conformance, value-002-conformance, value-003-conformance, flow-001-conformance,…
- attempt 1 (repair 1): built; 1/1 checks model=gpt-5.6-luna; execution 20260823.042455.513Z-305e685e

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
- jq_interpreter/runtime.py

SUMMARY:
Implemented source-preserving numeric handling while retaining IEEE-754 behavior for transformed values. DATA-001 conformance passes 40/40; numeric regression slice passes 17/17; pytest passes 138 tests.

BLOCKERS:
- None
