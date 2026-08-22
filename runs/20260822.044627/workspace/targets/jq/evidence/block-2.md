# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 11170
- execution id: 20260822.194909.871Z-c0f03947

## Stories built
- Implement the executable jq entry point. (EXEC-001) [story]

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-EXEC-001.md (SP 483)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- jq

## Pre-build acceptance observation
- GREEN (prepassed): exec-entry-conformance (FEATURE-EXEC-001.md)
  intent: The executable entry point passes the corpus slice containing the primitive interface programs.
  return code: 0
  stdout:
    {
      "candidate": [
        "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
      ],
      "corpus": "jq.test",
      "summary": {
        "pass": 5,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
- GREEN (prepassed): exec-is-runnable (FEATURE-EXEC-001.md)
  intent: The deliverable is directly executable at the application root.
  return code: 0

## Post-build programmatic acceptance
- PASS: exec-entry-conformance (FEATURE-EXEC-001.md)
  intent: The executable entry point passes the corpus slice containing the primitive interface programs.
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
        "pass": 5,
        "fail": 0,
        "error": 0,
        "skip": 0
      },
      "cases": []
    }
- PASS: exec-is-runnable (FEATURE-EXEC-001.md)
  intent: The deliverable is directly executable at the application root.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
Implemented EXEC-001 entry point hardening.

RESULT: SUCCESS

FILES CHANGED:
- [jq](/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq)

SUMMARY:
- Directly executable `jq` launcher confirmed.
- Project tests: 15 passed.
- Primitive conformance slice: 5 passed, 0 failed, 0 errored.
- Staged source assets unchanged.

BLOCKERS:
- None
