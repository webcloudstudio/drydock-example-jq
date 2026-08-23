# Evidence: Block 37 · Service (block-37)

- block type: block
- date: 2026-08-23
- resulting state: closed/implemented
- story points (combined assembled cost): 56291
- execution id: -

## Stories built
- Implement regular-expression filters. (TEXT-003) [story]

## Acceptance tooling authorization
- FEATURE-TEXT-003.md#text-003-regex-conformance: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-TEXT-003.md#text-003-captures: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-TEXT-003.md (SP 622)
- context: builtin.jq (SP 2408)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python.md (SP 3892)

## Pre-build acceptance observation
- RED: text-003-regex-conformance (FEATURE-TEXT-003.md)
  intent: The authoritative corpus cases covering regular-expression filters execute and pass.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 0,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
  stderr:
    --- drydock: progress ---
    cases: pass=0 fail=0 error=0 skip=0 total=0 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 0, 'fail': 0, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "text-003-regex-conformance.py", line 17, in <module>
        assert sum(summary.values()) > 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: text-003-captures (FEATURE-TEXT-003.md)
  intent: The selected corpus includes matching, named capture, and replacement behavior.
  return code: 1
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 0,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
  stderr:
    --- drydock: progress ---
    cases: pass=0 fail=0 error=0 skip=0 total=0 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 0, 'fail': 0, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "text-003-captures.py", line 17, in <module>
        assert sum(summary.values()) > 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- UNVERIFIED: text-003-regex-conformance (FEATURE-TEXT-003.md)
  intent: The authoritative corpus cases covering regular-expression filters execute and pass.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not requested
  return code: 1
  error: unverified acceptance: selector matched zero cases
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 0,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
  stderr:
    --- drydock: progress ---
    cases: pass=0 fail=0 error=0 skip=0 total=0 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 0, 'fail': 0, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "text-003-regex-conformance.py", line 17, in <module>
        assert sum(summary.values()) > 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- UNVERIFIED: text-003-captures (FEATURE-TEXT-003.md)
  intent: The selected corpus includes matching, named capture, and replacement behavior.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not requested
  return code: 1
  error: unverified acceptance: selector matched zero cases
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 0,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
  stderr:
    --- drydock: progress ---
    cases: pass=0 fail=0 error=0 skip=0 total=0 from=summary
    --- drydock: end progress ---
    --- drydock: values at failure ---
      summary = {'pass': 0, 'fail': 0, 'error': 0, 'skip': 0}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "text-003-captures.py", line 17, in <module>
        assert sum(summary.values()) > 0
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Build summary
(no summary returned)
