# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-08-23T05:14:37+00:00
- Execution ID: 20260823.051322.004Z-76747529
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: text-003-regex-conformance, text-003-captures
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/workspace/targets/jq/evidence/block-37.md

## Diagnostic

Block "Block 37 · Service" [block-37] failed its acceptance criteria.
  Story "Implement regular-expression filters." [TEXT-003] does not meet its own acceptance criteria:
    - AC text-003-regex-conformance — The authoritative corpus cases covering regular-expression filters execute and pass.
        assertion: assert sum(summary.values()) > 0 → AssertionError
        cases: pass=0 fail=0 error=0 skip=0 total=0 from=summary
        raised at: text-003-regex-conformance.py:17
        process exit code: 1
        values at failure:
          summary = {'pass': 0, 'fail': 0, 'error': 0, 'skip': 0}
        observed output:
            "candidate": [
              "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260822.044627/build/jq/jq"
            ],
            "corpus": "jq.test",
… (42 more lines truncated)

## Recovery

Run: drydock build jq
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
