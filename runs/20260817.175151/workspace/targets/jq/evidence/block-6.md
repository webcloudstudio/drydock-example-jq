# Evidence: Block 6 · Service (block-6)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 23071
- execution id: 20260817.181827.485Z-16b9de24

## Stories built
- Reject invalid jq programs during compilation. (front-validation) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Front-Validation.md (SP 771)
- context: parser.y (SP 5596)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_conformance_staging.py
- tests/test_front_validation.py

## Pre-build acceptance observation
- GREEN (prepassed): validation-rejects-invalid-programs (FEATURE-Front-Validation.md)
  intent: Invalid jq programs are rejected with the declared compile exit status.
  return code: 0
- RED: validation-rejects-undefined-bindings (FEATURE-Front-Validation.md)
  intent: Undefined variable references fail during compilation rather than runtime evaluation.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '. as $known | $unknown'], returncode=0, stdout='null\n', stderr='')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "validation-rejects-undefined-bindings.py", line 13, in <module>
        assert result.returncode == 3
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): validation-rejects-invalid-object-keys (FEATURE-Front-Validation.md)
  intent: A constant non-string object key is rejected during compilation.
  return code: 0
- GREEN (prepassed): validation-accepts-valid-program (FEATURE-Front-Validation.md)
  intent: A valid program reaches evaluation and returns its supplied input.
  return code: 0

## Post-build programmatic acceptance
- PASS: validation-rejects-invalid-programs (FEATURE-Front-Validation.md)
  intent: Invalid jq programs are rejected with the declared compile exit status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: validation-rejects-undefined-bindings (FEATURE-Front-Validation.md)
  intent: Undefined variable references fail during compilation rather than runtime evaluation.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: validation-rejects-invalid-object-keys (FEATURE-Front-Validation.md)
  intent: A constant non-string object key is rejected during compilation.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: validation-accepts-valid-program (FEATURE-Front-Validation.md)
  intent: A valid program reaches evaluation and returns its supplied input.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_front_validation.py
- tests/test_conformance_staging.py

SUMMARY:
Implemented compile-time validation for undefined bindings and labels. Added front-validation tests and fixed test discovery compatibility. All 20 tests and acceptance checks pass.

BLOCKERS:
- None
