# Evidence: Block 9 · Service (block-9)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 50316
- execution id: 20260817.182444.614Z-8ae14f5e

## Stories built
- Implement jq values and fundamental operators. (core-values-operators) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Core-Values-Operators.md (SP 919)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_core_values_operators.py

## Pre-build acceptance observation
- GREEN (prepassed): operators-addition (FEATURE-Core-Values-Operators.md)
  intent: Numeric addition produces the arithmetic sum.
  return code: 0
- RED: operators-type-distinction (FEATURE-Core-Values-Operators.md)
  intent: Equality does not equate booleans with numbers.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', 'true == 1'], returncode=0, stdout='true\n', stderr='')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "operators-type-distinction.py", line 15, in <module>
        assert json.loads(result.stdout) is False
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): operators-truthiness (FEATURE-Core-Values-Operators.md)
  intent: Conditional truthiness treats only false and null as false.
  return code: 0
- GREEN (prepassed): operators-defined-or (FEATURE-Core-Values-Operators.md)
  intent: Defined-or returns the fallback for a false or null value.
  return code: 0
- GREEN (prepassed): operators-runtime-error (FEATURE-Core-Values-Operators.md)
  intent: Division by zero is reported as a runtime failure.
  return code: 0

## Post-build programmatic acceptance
- PASS: operators-addition (FEATURE-Core-Values-Operators.md)
  intent: Numeric addition produces the arithmetic sum.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: operators-type-distinction (FEATURE-Core-Values-Operators.md)
  intent: Equality does not equate booleans with numbers.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: operators-truthiness (FEATURE-Core-Values-Operators.md)
  intent: Conditional truthiness treats only false and null as false.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: operators-defined-or (FEATURE-Core-Values-Operators.md)
  intent: Defined-or returns the fallback for a false or null value.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: operators-runtime-error (FEATURE-Core-Values-Operators.md)
  intent: Division by zero is reported as a runtime failure.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_core_values_operators.py

SUMMARY:
Implemented jq value/operator semantics, including arithmetic, type-aware equality, truthiness, logical operators, defined-or, and runtime errors. All 38 tests pass.

BLOCKERS:
- None
