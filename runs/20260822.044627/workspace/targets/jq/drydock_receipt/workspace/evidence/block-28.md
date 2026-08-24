# Evidence: Block 28 · Service (block-28)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 53792
- execution id: 20260823.035649.869Z-75289107

## Stories built
- Implement path access and mutation primitives. (PATH-002) [story]

## Acceptance tooling authorization
- FEATURE-PATH-002.md#path-002-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-PATH-002.md (SP 483)
- context: jq-manual.txt (SP 32696)
- context: builtin.jq (SP 2408)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- tests/test_path_002_access_mutation.py

## Pre-build acceptance observation
- GREEN (prepassed): path-002-conformance (FEATURE-PATH-002.md)
  intent: The authoritative corpus slice covering getpath, setpath, and delpaths executes and passes.
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 16,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Post-build programmatic acceptance
- PASS: path-002-conformance (FEATURE-PATH-002.md)
  intent: The authoritative corpus slice covering getpath, setpath, and delpaths executes and passes.
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
        "pass": 16,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Build summary
Implemented PATH-002.

RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/evaluator.py
- tests/test_path_002_access_mutation.py

SUMMARY:
Added validated immutable `getpath`, `setpath`, and `delpaths` behavior, including nested creation, deletion ordering, negative indices, depth/index limits, and invalid path handling.

Verification:
- Scoped conformance: 16 passed, 0 failed, 0 errors
- Pytest: 131 passed

BLOCKERS:
- None
