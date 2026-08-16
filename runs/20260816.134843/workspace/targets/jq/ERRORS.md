# BIG ERRORS — action required

- Command: `plan`
- Phase: post-output validation
- State: Error
- Timestamp: 2026-08-16T13:58:55+00:00
- Execution ID: 20260816.135016.742Z-fdc3b8b3
- Challenge Execution ID: -
- Classification: plan output validation failed
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/workspace/logs

## Diagnostic

FEATURE-Command-Line-Errors.md [errors-compile-status] acceptance block is never closed: found '=== AC errors-runtime-status ===' before '=== END AC errors-compile-status ==='
  No files were changed.

## Recovery

Correct the plan input or model artifact, then run: drydock plan jq
