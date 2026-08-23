# Evidence: Block 14 · Service (block-14)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 51245
- execution id: 20260823.023629.826Z-b996dd45

## Stories built
- Implement field and index access. (VALUE-002) [story]

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-VALUE-002.md (SP 347)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- tests/test_value_002_access.py

## Pre-build acceptance observation
- GREEN (prepassed): value-002-conformance (FEATURE-VALUE-002.md)
  intent: The authoritative corpus cases exercising field and index access execute successfully.
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 135,
        "fail": 0,
        "error": 0,
        "skip": 3
      },
      "cases": [
        {
          "line": 1912,
          "program": "import \"data\" as $e; import \"data\" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(\";\")",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "\"is a test;is too;is a test;is too\""
          ],
          "actual": []
        },
        {
          "line": 1973,
          "program": "modulemeta | .deps | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "6"
          ],
          "actual": []
        },
        {
          "line": 1977,
          "program": "modulemeta | .defs | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        }
      ]
    }

## Post-build programmatic acceptance
- PASS: value-002-conformance (FEATURE-VALUE-002.md)
  intent: The authoritative corpus cases exercising field and index access execute successfully.
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
        "pass": 135,
        "fail": 0,
        "error": 0,
        "skip": 3
      },
      "cases": [
        {
          "line": 1912,
          "program": "import \"data\" as $e; import \"data\" as $d; [$d[].this,$e[].that,$d::d[].this,$e::e[].that]|join(\";\")",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "\"is a test;is too;is a test;is too\""
          ],
          "actual": []
        },
        {
          "line": 1973,
          "program": "modulemeta | .deps | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "6"
          ],
          "actual": []
        },
        {
          "line": 1977,
          "program": "modulemeta | .defs | length",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "2"
          ],
          "actual": []
        }
      ]
    }

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/evaluator.py
- tests/test_value_002_access.py

SUMMARY:
Implemented strict object key access and added VALUE-002 coverage for fields, indexes, negatives, optional access, missing values, and errors.

Tests: 68 passed. Conformance: 135 passed, 0 failed, 0 errored, 3 skipped.

BLOCKERS:
- None
