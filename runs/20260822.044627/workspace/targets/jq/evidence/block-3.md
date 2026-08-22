# Evidence: Block 3 · Service (block-3)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 11182
- execution id: 20260822.195011.791Z-7425cbae

## Stories built
- Implement jq process exit and diagnostic behavior. (EXEC-002) [story]

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-EXEC-002.md (SP 494)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- jq_interpreter/cli.py
- tests/test_architecture.py

## Pre-build acceptance observation
- GREEN (prepassed): compile-exit-code (FEATURE-EXEC-002.md)
  intent: A syntactically invalid jq program returns the compile-failure status.
  return code: 0
- GREEN (prepassed): runtime-exit-code (FEATURE-EXEC-002.md)
  intent: A compiled jq program that raises returns the runtime-failure status.
  return code: 0
- GREEN (prepassed): partial-runtime-output (FEATURE-EXEC-002.md)
  intent: Values emitted before a runtime error remain available on stdout.
  return code: 0

## Post-build programmatic acceptance
- PASS: compile-exit-code (FEATURE-EXEC-002.md)
  intent: A syntactically invalid jq program returns the compile-failure status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: runtime-exit-code (FEATURE-EXEC-002.md)
  intent: A compiled jq program that raises returns the runtime-failure status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: partial-runtime-output (FEATURE-EXEC-002.md)
  intent: Values emitted before a runtime error remain available on stdout.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
Implemented EXEC-002 process behavior.

- Compile failures exit `3`.
- Runtime failures exit `5`.
- Success exits `0`.
- Diagnostics remain on stderr.
- Partial output is flushed and preserved before runtime errors.

All 16 unit tests and three acceptance checks pass.

RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/cli.py
- tests/test_architecture.py

SUMMARY:
Added immediate output flushing and regression coverage for stderr-only runtime diagnostics.

BLOCKERS:
- None
