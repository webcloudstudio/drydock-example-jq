# Evidence: Block 3 · Service (block-3)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 11678
- execution id: 20260817.030420.278Z-6b166c8c

## Stories built
- Implement jq compile and runtime diagnostics with documented exit codes. (cli-002) [story]

## Stacked context
- compass: COMPASS.md (SP 3799)
- implements: FEATURE-CLI-002.md (SP 593)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 162)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- jq_interpreter/cli.py
- tests/test_cli_interface.py

## Pre-build acceptance observation
- GREEN (prepassed): cli-002-compile-error (FEATURE-CLI-002.md)
  intent: Invalid jq syntax is rejected with compile exit status 3 and a stderr diagnostic.
  return code: 0
- GREEN (prepassed): cli-002-runtime-error (FEATURE-CLI-002.md)
  intent: A compiled filter that raises at runtime returns exit status 5 and keeps diagnostics off stdout.
  return code: 0
- GREEN (prepassed): cli-002-partial-output (FEATURE-CLI-002.md)
  intent: Results emitted before a runtime error remain on stdout while the process returns runtime exit status 5.
  return code: 0

## Post-build programmatic acceptance
- PASS: cli-002-compile-error (FEATURE-CLI-002.md)
  intent: Invalid jq syntax is rejected with compile exit status 3 and a stderr diagnostic.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-002-runtime-error (FEATURE-CLI-002.md)
  intent: A compiled filter that raises at runtime returns exit status 5 and keeps diagnostics off stdout.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-002-partial-output (FEATURE-CLI-002.md)
  intent: Results emitted before a runtime error remain on stdout while the process returns runtime exit status 5.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/cli.py
- tests/test_cli_interface.py

SUMMARY:
Implemented stderr diagnostics with distinct compile exit `3` and runtime exit `5`, preserving partial stdout output. Added tests for all three acceptance behaviors. `pytest`: 10 passed; CLI acceptance: 3 passed.

BLOCKERS:
- Full conformance run was interrupted by an unrelated runaway existing case.
