# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-08-22T21:17:01+00:00
- Execution ID: 20260822.210533.139Z-e0792409
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: parse-003-conformance, parse-004-conformance
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/workspace/targets/jq/evidence/block-8.md

## Diagnostic

Block "Block 8 · Service" [block-8] failed its acceptance criteria.
  Story "Implement jq filter expression grammar." [PARSE-003] does not meet its own acceptance criteria:
    - AC parse-003-conformance — The executable passes every selected corpus case exercising expression punctuation, accessors, collections, and operators.
        assertion: assert summary["fail"] == 0 and summary["error"] == 0 → AssertionError
        cases: pass=210 fail=245 error=0 skip=9 total=464 from=summary
        raised at: parse-003-conformance.py:18
        process exit code: 1
        values at failure:
          summary = {'pass': 210, 'fail': 245, 'error': 0, 'skip': 9}
        observed output:
                "line": 2633,
… (46 more lines truncated)

## Recovery

Run: drydock build jq
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
