# Evidence: Block 5 · Service (block-5)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 23572
- execution id: 20260816.204819.647Z-2cbc3678

## Stories built
- Enforce jq compile diagnostics and exit-status behavior. (compile-contract) [story]

## Stacked context
- compass: COMPASS.md (SP 3836)
- implements: FEATURE-Compile-Contract.md (SP 585)
- context: run_conformance.py (SP 4354)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 160)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_parser.py
- tests/test_compile_contract.py

## Pre-build acceptance observation
- RED: compile-api-separates-errors (FEATURE-Compile-Contract.md)
  intent: The compiler exposes a compile boundary that distinguishes invalid source.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      rejected = False
    --- drydock: end values ---
    Traceback (most recent call last):
      File "compile-api-separates-errors.py", line 10, in <module>
        assert rejected is True
               ^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): compile-valid-source-reaches-ast (FEATURE-Compile-Contract.md)
  intent: Valid source crosses compilation and produces an AST.
  return code: 0
- GREEN (prepassed): compile-cli-status-contract (FEATURE-Compile-Contract.md)
  intent: The executable reports a malformed program with the declared compile status.
  return code: 0
- GREEN (prepassed): compile-diagnostics-use-stderr (FEATURE-Compile-Contract.md)
  intent: Compile diagnostics are separated from result output.
  return code: 0

## Post-build programmatic acceptance
- PASS: compile-api-separates-errors (FEATURE-Compile-Contract.md)
  intent: The compiler exposes a compile boundary that distinguishes invalid source.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: compile-valid-source-reaches-ast (FEATURE-Compile-Contract.md)
  intent: Valid source crosses compilation and produces an AST.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: compile-cli-status-contract (FEATURE-Compile-Contract.md)
  intent: The executable reports a malformed program with the declared compile status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: compile-diagnostics-use-stderr (FEATURE-Compile-Contract.md)
  intent: Compile diagnostics are separated from result output.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_parser.py
- tests/test_compile_contract.py

SUMMARY:
Implemented static compile rejection for invalid patterns and undefined labels. Added compile/runtime contract tests. All 23 project tests and 10 targeted compile checks pass. Staged asset hashes remain unchanged.

BLOCKERS:
- Full conformance still has unrelated pre-existing runtime failures outside this block.
