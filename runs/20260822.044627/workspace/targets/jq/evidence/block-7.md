# Evidence: Block 7 · Service (block-7)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 58070
- execution id: 20260822.195833.572Z-be3705d7

## Stories built
- Implement literals, strings, escapes, and interpolation. (PARSE-002) [story]

## Acceptance tooling authorization
- FEATURE-PARSE-002.md#parse-002-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-PARSE-002.md (SP 441)
- context: lexer.l (SP 1137)
- context: parser.y (SP 5596)
- context: jq.test (SP 13058)
- context: jq-manual.txt (SP 32696)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/ast.py
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_parse_002.py

## Pre-build acceptance observation
- RED: parse-002-conformance (FEATURE-PARSE-002.md)
  intent: The executable passes every selected corpus case covering interpolation, URI formatting, and Base64 formatting.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 0,
        "fail": 6,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 72,
          "program": "@text,@json,([1,.]|@csv,@tsv),@html,(@uri|.,@urid),@sh,(@base64|.,@base64d)",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unsupported program in foundational parser",
          "expect_failure": false,
          "expected": [
            "\"!()<>&'\\\"\\t\"",
            "\"\\\"!()<>&'\\\\\\\"\\\\t\\\"\"",
            "\"1,\\\"!()<>&'\\\"\\\"\\t\\\"\"",
            "\"1\\t!()<>&'\\\"\\\\t\"",
            "\"!()&lt;&gt;&amp;&apos;&quot;\\t\"",
            "\"%21%28%29%3C%3E%26%27%22%09\"",
            "\"!()<>&'\\\"\\t\"",
            "\"'!()<>&'\\\\''\\\"\\t'\"",
            "\"ISgpPD4mJyIJ\"",
            "\"!()<>&'\\\"\\t\""
          ],
          "actual": []
        },
        {
          "line": 86,
          "program": "@base64",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unsupported program in foundational parser",
          "expect_failure": false,
          "expected": [
            "\"Zm/Ds2Jhcgo=\""
          ],
          "actual": []
        },
        {
          "line": 90,
          "program": "@base64d",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unsupported program in foundational parser",
          "expect_failure": false,
          "expected": [
            "\"fo\u00f3bar\\n\""
          ],
          "actual": []
        },
        {
          "line": 94,
          "program": "@uri",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unsupported program in foundational parser",
          "expect_failure": false,
          "expected": [
            "\"%CE%BC\""
          ],
          "actual": []
        },
        {
          "line": 98,
          "program": "@urid",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unsupported program in foundational parser",
          "expect_failure": false,
          "expected": [
            "\"\\u03bc\""
          ],
          "actual": []
        },
        {
          "line": 2548,
          "program": "strflocaltime(\"\" | ., @uri)",
          "status": "fail",
          "detail": "program did not compile: jq: compile error: unsupported program in foundational parser",
          "expect_failure": false,
          "expected": [
            "\"\"",
            "\"\""
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=0 fail=6 error=0 skip=0 total=6 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 0, 'fail': 6, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parse-002-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: parse-002-conformance (FEATURE-PARSE-002.md)
  intent: The executable passes every selected corpus case covering interpolation, URI formatting, and Base64 formatting.
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
        "pass": 6,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/ast.py
- jq_interpreter/parser.py
- jq_interpreter/evaluator.py
- tests/test_parse_002.py

SUMMARY:
Implemented literals, escaped strings, interpolation, pipes, and format filters. Added focused tests.

Verification: 32 tests passed; scoped conformance passed 6/6 with zero failures/errors.

BLOCKERS:
- None
