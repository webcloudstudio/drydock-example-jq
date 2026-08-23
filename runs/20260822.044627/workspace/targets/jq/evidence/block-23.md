# Evidence: Block 23 · Service (block-23)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 56964
- execution id: 20260823.032616.141Z-64a1b0fb

## Stories built
- Implement lexical variable bindings. (FUNC-001) [story]

## Acceptance tooling authorization
- FEATURE-FUNC-001.md#func-001-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-FUNC-001.md (SP 472)
- context: parser.y (SP 5596)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/parser.py
- tests/test_service_lexical_bindings.py

## Pre-build acceptance observation
- GREEN (prepassed): func-001-conformance (FEATURE-FUNC-001.md)
  intent: The executable passes the authoritative conformance cases exercising lexical bindings and variable lookup.
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 89,
        "fail": 0,
        "error": 0,
        "skip": 2
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
          "line": 1917,
          "program": "import \"data\" as $a; import \"data\" as $b; def f: {$a, $b}; f",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"this\":\"is a test\",\"that\":\"is too\"}],\"b\":[{\"this\":\"is a test\",\"that\":\"is too\"}]}"
          ],
          "actual": []
        }
      ]
    }

## Post-build programmatic acceptance
- PASS: func-001-conformance (FEATURE-FUNC-001.md)
  intent: The executable passes the authoritative conformance cases exercising lexical bindings and variable lookup.
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
        "pass": 89,
        "fail": 0,
        "error": 0,
        "skip": 2
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
          "line": 1917,
          "program": "import \"data\" as $a; import \"data\" as $b; def f: {$a, $b}; f",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "{\"a\":[{\"this\":\"is a test\",\"that\":\"is too\"}],\"b\":[{\"this\":\"is a test\",\"that\":\"is too\"}]}"
          ],
          "actual": []
        }
      ]
    }

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/parser.py
- tests/test_service_lexical_bindings.py

SUMMARY:
Implemented lexical variable scope validation and added binding tests for generators, shadowing, patterns, keyword names, and scope isolation.

Verification: 111 tests passed; conformance slice passed 89 cases with 0 failures and 0 errors.

BLOCKERS:
- None
