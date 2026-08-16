# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-08-16T20:58:21+00:00
- Execution ID: 20260816.205749.075Z-95efae9e
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: formats-suite
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq/evidence/block-6.md

## Diagnostic

Block "Block 6 · Service" [block-6] failed its acceptance criteria.
  Story "Implement jq interpolation and format filters." [formats] does not meet its own acceptance criteria:
    - AC formats-suite — The format implementation passes its authoritative conformance slice.
        assertion: assert result.returncode == 0 → AssertionError
        raised at: formats-suite.py:10
        process exit code: 1
        values at failure:
          result = CompletedProcess(args=['python3', 'sources/run_conformance.py', '--select', '@|interpolation'], returncode=2, stdout='', stderr='error: JQ is not set; give the command that runs your implementation, e.g.\n    JQ="$PWD/jq" python3 sources/run_conformance.py\n')
        observed output:
… (8 more lines truncated)

## Recovery

Run: drydock build jq
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
