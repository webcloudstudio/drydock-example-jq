# Evidence: Block 25 · Service (block-25)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 56981
- execution id: 20260823.033926.906Z-4e4c50bc

## Stories built
- Implement function definitions, scope, and recursion. (FUNC-003) [story]

## Acceptance tooling authorization
- FEATURE-FUNC-003.md#func-003-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-FUNC-003.md (SP 486)
- context: parser.y (SP 5596)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- tests/test_func_002_parameters.py

## Pre-build acceptance observation
- GREEN (prepassed): func-003-conformance (FEATURE-FUNC-003.md)
  intent: The executable passes the authoritative conformance cases exercising function definitions, scope, redefinition, and recursion.
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 15,
        "fail": 0,
        "error": 0,
        "skip": 2
      },
      "cases": [
        {
          "line": 1900,
          "program": "import \"a\" as foo; import \"b\" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"c\",\"a\"]"
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
- PASS: func-003-conformance (FEATURE-FUNC-003.md)
  intent: The executable passes the authoritative conformance cases exercising function definitions, scope, redefinition, and recursion.
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
        "pass": 15,
        "fail": 0,
        "error": 0,
        "skip": 2
      },
      "cases": [
        {
          "line": 1900,
          "program": "import \"a\" as foo; import \"b\" as bar; def fooa: foo::a; [fooa, bar::a, bar::b, foo::a]",
          "status": "skip",
          "detail": "declared in exclusions.txt",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"c\",\"a\"]"
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
- jq_interpreter/evaluator.py
- tests/test_func_002_parameters.py

SUMMARY:
Implemented definition-time lexical closures while preserving recursion, redefinition, arity, and generator behavior.

Verification:
- 120 pytest tests passed.
- Conformance `def ` slice: 15 passed, 0 failed, 0 errored, 2 skipped.

BLOCKERS:
- None
