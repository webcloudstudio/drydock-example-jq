# Evidence: Block 38 · Service (block-38)

- block type: block
- date: 2026-08-23
- resulting state: closed/verified
- story points (combined assembled cost): 51519
- execution id: 20260823.113822.128Z-2a70a44a

## Stories built
- Implement date and time filters. (TEXT-004) [story]

## Acceptance tooling authorization
- FEATURE-TEXT-004.md#text-004-date-conformance: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-TEXT-004.md#text-004-utc: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-TEXT-004.md (SP 621)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_service_date_time.py

## Pre-build acceptance observation
- RED: text-004-date-conformance (FEATURE-TEXT-004.md)
  intent: The authoritative corpus cases covering date and time filters execute and pass.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 12,
        "fail": 2,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 1855,
          "program": "mktime",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "1726876800"
          ],
          "actual": []
        },
        {
          "line": 1859,
          "program": "gmtime",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[2015,2,5,23,51,47,4,63]"
          ],
          "actual": [
            "[2015,2,5,23,51,47,3,63]"
          ]
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=12 fail=2 error=0 skip=0 total=14 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 12, 'fail': 2, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "text-004-date-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: text-004-utc (FEATURE-TEXT-004.md)
  intent: The selected corpus exercises both ISO convenience filters and low-level UTC conversions.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 9,
        "fail": 2,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 1855,
          "program": "mktime",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "1726876800"
          ],
          "actual": []
        },
        {
          "line": 1859,
          "program": "gmtime",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[2015,2,5,23,51,47,4,63]"
          ],
          "actual": [
            "[2015,2,5,23,51,47,3,63]"
          ]
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=9 fail=2 error=0 skip=0 total=11 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 9, 'fail': 2, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "text-004-utc.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: text-004-date-conformance (FEATURE-TEXT-004.md)
  intent: The authoritative corpus cases covering date and time filters execute and pass.
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
        "pass": 14,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
- PASS: text-004-utc (FEATURE-TEXT-004.md)
  intent: The selected corpus exercises both ISO convenience filters and low-level UTC conversions.
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
        "pass": 11,
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
- tests/test_service_date_time.py

SUMMARY:
Implemented UTC date parsing, formatting, local/UTC time conversion, `mktime`, and ISO aliases. All 170 tests pass; acceptance slices pass 14/14 and 11/11.

BLOCKERS:
- None
