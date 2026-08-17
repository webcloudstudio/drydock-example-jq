# Evidence: Block 10 · Service (block-10)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 23324
- execution id: 20260817.182735.829Z-63874903

## Stories built
- Construct arrays and objects from generator expressions. (core-construction) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Core-Construction.md (SP 1031)
- context: parser.y (SP 5596)
- context: jq.test (SP 13058)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_construction.py

## Pre-build acceptance observation
- GREEN (prepassed): construction-array-collection (FEATURE-Core-Construction.md)
  intent: Array construction collects all outputs from a generator in order.
  return code: 0
- GREEN (prepassed): construction-empty-array (FEATURE-Core-Construction.md)
  intent: The empty array constructor returns an empty array.
  return code: 0
- GREEN (prepassed): construction-object-values (FEATURE-Core-Construction.md)
  intent: Object construction evaluates fields against the current input.
  return code: 0
- RED: construction-object-generator-expansion (FEATURE-Core-Construction.md)
  intent: A multi-output object value produces one object for each generated value.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      actual = [{'value': 4}]
      input_value = [4, 5]
    --- drydock: end values ---
    Traceback (most recent call last):
      File "construction-object-generator-expansion.py", line 17, in <module>
        assert actual == [{"value": value} for value in input_value]
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: construction-dynamic-key (FEATURE-Core-Construction.md)
  intent: A parenthesized key expression creates a string-keyed object field.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '{(.key): .value}'], returncode=3, stdout='', stderr='jq: invalid object key\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "construction-dynamic-key.py", line 15, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: construction-array-collection (FEATURE-Core-Construction.md)
  intent: Array construction collects all outputs from a generator in order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: construction-empty-array (FEATURE-Core-Construction.md)
  intent: The empty array constructor returns an empty array.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: construction-object-values (FEATURE-Core-Construction.md)
  intent: Object construction evaluates fields against the current input.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: construction-object-generator-expansion (FEATURE-Core-Construction.md)
  intent: A multi-output object value produces one object for each generated value.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: construction-dynamic-key (FEATURE-Core-Construction.md)
  intent: A parenthesized key expression creates a string-keyed object field.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_construction.py

SUMMARY:
Implemented array collection, object generator expansion, dynamic keys, shorthand keys, Cartesian products, and compile-time key validation. All 5 acceptance checks and 45 pytest tests pass.

BLOCKERS:
- None
