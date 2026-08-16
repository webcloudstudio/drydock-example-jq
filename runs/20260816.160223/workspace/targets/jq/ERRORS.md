# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-08-16T16:53:25+00:00
- Execution ID: 20260816.165223.003Z-b06127a7
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: eval-cartesian-function, eval-cartesian-order
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.160223/workspace/targets/jq/evidence/block-9.md

## Diagnostic

Block "Block 9 · Service" [block-9] failed its acceptance criteria.
  Story "Implement cartesian evaluation of multi-output arguments." [eval-cartesian] does not meet its own acceptance criteria:
    - AC eval-cartesian-function — Function arguments retain all combinations when each argument is a generator.
        assertion: assert actual == expected → AssertionError
        raised at: eval-cartesian-function.py:14
        process exit code: 1
        values at failure:
          actual = [0, 1, 2, 0, 1, 2, 3, 1, 2, 1, 2, 3]
          expected = [0, 1, 2, 0, 1, 2, 3]
        check stderr:
          Traceback (most recent call last):
            File "eval-cartesian-function.py", line 14, in <module>
              assert actual == expected
                     ^^^^^^^^^^^^^^^^^^
… (13 more lines truncated)

## Recovery

Run: drydock build jq
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
