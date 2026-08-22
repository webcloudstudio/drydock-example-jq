# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-08-22T18:16:58+00:00
- Execution ID: 20260822.181613.175Z-5ac5befb
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: conformance-source-integrity
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/workspace/targets/jq/evidence/block-4.md

## Diagnostic

Block "Block 4 · Foundational" [block-4] failed its acceptance criteria.
  Story "Stage and validate immutable conformance assets." [conf-001] does not meet its own acceptance criteria:
    - AC conformance-source-integrity — The staged harness exposes the required corpus and exclusion paths and can be imported from the build directory.
        assertion: assert run_conformance.CORPUS == sources / "jq.test" → AssertionError
        raised at: conformance-source-integrity.py:10
        process exit code: 1
        values at failure:
          sources = PosixPath('sources')
        check stderr:
          Traceback (most recent call last):
            File "conformance-source-integrity.py", line 10, in <module>
              assert run_conformance.CORPUS == sources / "jq.test"
… (2 more lines truncated)

## Recovery

Run: drydock build jq
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
