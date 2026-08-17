# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-08-17T18:50:44+00:00
- Execution ID: 20260817.184955.880Z-e006efbf
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: path-exact-and-read
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq/evidence/block-15.md

## Diagnostic

Block "Block 15 · Service" [block-15] failed its acceptance criteria.
  Story "Discover, access, and materialize jq paths." [path-discovery] does not meet its own acceptance criteria:
    - AC path-exact-and-read — Exact paths can be materialized and read through the executable.
        assertion: assert actual[0][-1] == payload["a"][0]["b"] → AssertionError
        raised at: path-exact-and-read.py:16
        process exit code: 1
        values at failure:
          actual = [['a', 0, 'b'], 7]
          payload = {'a': [{'b': 7}]}
        check stderr:
          Traceback (most recent call last):
            File "path-exact-and-read.py", line 16, in <module>
              assert actual[0][-1] == payload["a"][0]["b"]
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
… (1 more line truncated)

## Recovery

Run: drydock build jq
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
