# Evidence: Block 8 · Service (block-8)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 25288
- execution id: 20260816.164423.186Z-02e15589

## Stories built
- Implement jq compile-time and runtime exit-code behavior. (cli-errors) [story]
- Document the jq executable interface and verification command. (cli-documentation) [story]

## Stacked context
- compass: COMPASS.md (SP 3787)
- implements: FEATURE-CLI-Errors.md (SP 499)
- context: run_conformance.py (SP 4354)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 126)
- stack: python_compact.md (SP 1534)
- implements: README.md (SP 470)
- context: full_test.sh (SP 189)
- stack: common_compact.md (SP 1179)

## Build directory changes
- README.md
- jq_cli.py
- tests/test_cli_errors.py

## Pre-build acceptance observation
- GREEN (prepassed): cli-compile-error (FEATURE-CLI-Errors.md)
  intent: A syntactically invalid jq program exits with the compile-error status.
  return code: 0
- GREEN (prepassed): cli-runtime-error (FEATURE-CLI-Errors.md)
  intent: A valid jq program that raises at runtime exits with the runtime-error status.
  return code: 0
- GREEN (prepassed): cli-prior-output (FEATURE-CLI-Errors.md)
  intent: Outputs produced before a runtime error remain available.
  return code: 0
- GREEN (prepassed): readme-interface (README.md)
  intent: The documented executable invocation is runnable from the project root.
  return code: 0
- GREEN (prepassed): readme-verification (README.md)
  intent: The documented complete verification command is available and has a successful process contract.
  return code: 0

## Post-build programmatic acceptance
- PASS: cli-compile-error (FEATURE-CLI-Errors.md)
  intent: A syntactically invalid jq program exits with the compile-error status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-runtime-error (FEATURE-CLI-Errors.md)
  intent: A valid jq program that raises at runtime exits with the runtime-error status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-prior-output (FEATURE-CLI-Errors.md)
  intent: Outputs produced before a runtime error remain available.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: readme-interface (README.md)
  intent: The documented executable invocation is runnable from the project root.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: readme-verification (README.md)
  intent: The documented complete verification command is available and has a successful process contract.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- README.md
- jq_cli.py
- tests/test_cli_errors.py

SUMMARY:
Implemented exit codes 3/5, preserved prior runtime output, documented the CLI, and added focused tests. `pytest -q`: 35 passed.

BLOCKERS:
- None
