# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-08-20T23:44:07+00:00
- Execution ID: 20260820.233735.815Z-80d32779
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: lexer-corpus
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260820.223834/workspace/targets/jq/evidence/block-4.md

## Diagnostic

Block "Block 4 · Service" [block-4] failed its acceptance criteria.
  Story "Tokenize jq programs including literals, strings, comments, and operators." [frontend-lexer] does not meet its own acceptance criteria:
    - AC lexer-corpus — The lexer and its dependent frontend pass the executable corpus slice covering literal, field, format, definition, module, and invalid-character syntax.
        assertion: assert summary["fail"] == 0 → AssertionError
        cases: pass=121 fail=19 error=0 skip=6 total=146 from=summary
        raised at: lexer-corpus.py:18
        process exit code: 1
        values at failure:
          summary = {'pass': 121, 'fail': 19, 'error': 0, 'skip': 6}
        observed output:
                "status": "fail",
                "detail": "output mismatch",
… (16 more lines truncated)

## Recovery

Run: drydock build jq
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
