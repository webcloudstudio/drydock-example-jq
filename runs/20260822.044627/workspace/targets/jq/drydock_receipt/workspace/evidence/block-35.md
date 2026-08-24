# Evidence: Block 35 · Service (block-35)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 53782
- execution id: 20260823.045149.005Z-117c6dab

## Stories built
- Implement string manipulation builtins. (TEXT-001) [story]

## Acceptance tooling authorization
- FEATURE-TEXT-001.md#text-001-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-TEXT-001.md (SP 474)
- context: builtin.jq (SP 2408)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_text_001_string_builtins.py

## Pre-build acceptance observation
- RED: text-001-conformance (FEATURE-TEXT-001.md)
  intent: The string manipulation slice executes matching corpus cases and passes all selected cases.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 28,
        "fail": 2,
        "error": 0,
        "skip": 1
      },
      "cases": [
        {
          "line": 1516,
          "program": "split(\"\")",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "[\"a\",\"b\",\"c\"]"
          ],
          "actual": []
        },
        {
          "line": 1823,
          "program": "ascii_upcase",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unknown filter",
          "expect_failure": false,
          "expected": [
            "\"USEFUL BUT NOT FOR \u00e9\""
          ],
          "actual": []
        },
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
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=28 fail=2 error=0 skip=1 total=31 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 28, 'fail': 2, 'error': 0, 'skip': 1}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "text-001-conformance.py", line 18, in <module>
        assert summary["fail"] == 0
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: text-001-conformance (FEATURE-TEXT-001.md)
  intent: The string manipulation slice executes matching corpus cases and passes all selected cases.
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
        "pass": 30,
        "fail": 0,
        "error": 0,
        "skip": 1
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
        }
      ]
    }

## Build summary
Implemented TEXT-001 string builtins.

- Added ASCII case conversion and parser registration.
- Fixed empty-string splitting and strict string validation.
- Added focused regression tests.
- `pytest -q`: 156 passed.
- Scoped conformance: 30 passed, 0 failed, 0 errored, 1 skipped.

RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/parser.py
- jq_interpreter/evaluator.py
- tests/test_text_001_string_builtins.py

SUMMARY:
String manipulation builtins now satisfy the declared scoped conformance suite.

BLOCKERS:
- None
