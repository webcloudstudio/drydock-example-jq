# Evidence: Block 27 · Service (block-27)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 53766
- execution id: 20260823.035101.009Z-f278c23c

## Stories built
- Implement path discovery and projection. (PATH-001) [story]

## Acceptance tooling authorization
- FEATURE-PATH-001.md#path-001-conformance: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-PATH-001.md (SP 464)
- context: jq-manual.txt (SP 32696)
- context: builtin.jq (SP 2408)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_interpreter/evaluator.py
- tests/test_path_001_discovery_projection.py

## Pre-build acceptance observation
- GREEN (prepassed): path-001-conformance (FEATURE-PATH-001.md)
  intent: The authoritative corpus slice covering path discovery and projection executes and passes.
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 29,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Post-build programmatic acceptance
- PASS: path-001-conformance (FEATURE-PATH-001.md)
  intent: The authoritative corpus slice covering path discovery and projection executes and passes.
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
        "pass": 29,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }

## Build summary
Implemented PATH-001 path discovery and projection improvements.

RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/evaluator.py
- tests/test_path_001_discovery_projection.py

SUMMARY:
Fixed filtered `paths(...)` traversal and added regression coverage for path ordering, recursive discovery, and `pick` projections.

Verification: 125 tests passed; conformance slice passed 29 cases with zero failures/errors.

BLOCKERS:
- None
