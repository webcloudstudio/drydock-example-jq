# Evidence: Block 40 · Service (block-40)

- block type: block
- date: 2026-08-23
- resulting state: closed/verified
- story points (combined assembled cost): 52679
- execution id: 20260823.114910.696Z-b8005d40

## Stories built
- Implement diagnostics and stderr output. (IO-002) [story]

## Acceptance tooling authorization
- FEATURE-IO-002.md#io-002-diagnostics-conformance: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-IO-002.md#io-002-channels: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-IO-002.md (SP 609)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- jq_interpreter/__init__.py
- jq_interpreter/cli.py
- jq_interpreter/errors.py
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_io_002_diagnostics.py

## Pre-build acceptance observation
- RED: io-002-diagnostics-conformance (FEATURE-IO-002.md)
  intent: The authoritative corpus cases covering debug, stderr, and halt_error execute and pass.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 0,
        "fail": 1,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 2341,
          "program": "debug",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=0 fail=1 error=0 skip=0 total=1 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 0, 'fail': 1, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "io-002-diagnostics-conformance.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: io-002-channels (FEATURE-IO-002.md)
  intent: The selected corpus exercises diagnostic filters while the conformance runner observes the declared process contract.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 0,
        "fail": 1,
        "error": 0,
        "skip": 0
      },
      "cases": [
        {
          "line": 2341,
          "program": "debug",
          "status": "fail",
          "detail": "output mismatch",
          "expect_failure": false,
          "expected": [
            "1"
          ],
          "actual": []
        }
      ]
    }
  stderr:
    --- drydock: progress ---
    cases: pass=0 fail=1 error=0 skip=0 total=1 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 0, 'fail': 1, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "io-002-channels.py", line 18, in <module>
        assert summary["fail"] == 0 and summary["error"] == 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: io-002-diagnostics-conformance (FEATURE-IO-002.md)
  intent: The authoritative corpus cases covering debug, stderr, and halt_error execute and pass.
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
        "pass": 1,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
- PASS: io-002-channels (FEATURE-IO-002.md)
  intent: The selected corpus exercises diagnostic filters while the conformance runner observes the declared process contract.
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
        "pass": 1,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/__init__.py
- jq_interpreter/cli.py
- jq_interpreter/errors.py
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_io_002_diagnostics.py

SUMMARY:
Implemented `debug`, `stderr`, and `halt_error` with channel separation and exit semantics. All 177 tests pass; diagnostics conformance passes with 1 pass, 0 failures, 0 errors.

BLOCKERS:
- None
