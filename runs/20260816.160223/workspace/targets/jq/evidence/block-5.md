# Evidence: Block 5 · Service (block-5)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 24894
- execution id: 20260816.163408.702Z-b0fa6334

## Stories built
- Implement jq compile-time validation and rejection. (frontend-validation) [story]

## Reusable compacts
- jq_compact.md

## Stacked context
- compass: COMPASS.md (SP 3787)
- implements: FEATURE-Frontend-Validation.md (SP 755)
- context: parser.y (SP 5596)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 126)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_evaluator.py
- jq_parser.py
- tests/test_frontend_validation.py

## Pre-build acceptance observation
- GREEN (prepassed): frontend-validation-syntax (FEATURE-Frontend-Validation.md)
  intent: Malformed jq syntax is rejected with the compile-error status.
  return code: 0
- GREEN (prepassed): frontend-validation-bindings (FEATURE-Frontend-Validation.md)
  intent: Undefined variables and invisible labels are rejected before runtime.
  return code: 0
- GREEN (prepassed): frontend-validation-object-keys (FEATURE-Frontend-Validation.md)
  intent: Invalid constant object keys are rejected at compile time.
  return code: 0
- GREEN (prepassed): frontend-validation-valid-program (FEATURE-Frontend-Validation.md)
  intent: Valid programs pass static validation and reach normal execution.
  return code: 0

## Post-build programmatic acceptance
- PASS: frontend-validation-syntax (FEATURE-Frontend-Validation.md)
  intent: Malformed jq syntax is rejected with the compile-error status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: frontend-validation-bindings (FEATURE-Frontend-Validation.md)
  intent: Undefined variables and invisible labels are rejected before runtime.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: frontend-validation-object-keys (FEATURE-Frontend-Validation.md)
  intent: Invalid constant object keys are rejected at compile time.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: frontend-validation-valid-program (FEATURE-Frontend-Validation.md)
  intent: Valid programs pass static validation and reach normal execution.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Full conformance suite did not complete.
- detail:
    `sh sources/full_test.sh` stalled in the supplied evaluator during a `-. | ...` corpus case; focused frontend-validation checks and project tests pass, but the required full-suite verdict could not be obtained.

## Build summary
<reusable-compact filename="jq.test">
The corpus defines jq’s compile/runtime contract: `%%FAIL` cases must exit 3; valid programs must execute with ordered generator outputs; runtime failures exit 5 while preserving prior output. Values are structurally compared, and module-loader cases are skipped only per `sources/exclusions.txt`. Frontend validation must reject malformed syntax, undefined variables/labels, invalid constant object keys, and invalid module metadata before evaluation.
</reusable-compact>

RESULT: FAILED

FILES CHANGED:
- jq_parser.py
- jq_evaluator.py
- tests/test_frontend_validation.py

SUMMARY:
Implemented compile-time validation for syntax, bindings, labels, object keys, and module metadata. Added label/break AST support and five focused tests. All 20 project tests pass; declared focused checks pass.

BLOCKERS:
- The full conformance harness hung during execution and produced no exit status.

FAILURE_SUMMARY: Full conformance suite did not complete.
FAILURE_DETAIL: `sh sources/full_test.sh` stalled in the supplied evaluator during a `-. | ...` corpus case; focused frontend-validation checks and project tests pass, but the required full-suite verdict could not be obtained.
