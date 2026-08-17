# Evidence: Block 2 · Service (block-2)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 11857
- execution id: 20260817.025852.137Z-e533a99b

## Stories built
- Implement the executable jq command interface. (cli-001) [story]

## Reusable compacts
- run_conformance_compact.md

## Stacked context
- compass: COMPASS.md (SP 3799)
- implements: FEATURE-CLI-001.md (SP 762)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 162)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- jq_interpreter/cli.py
- jq_interpreter/evaluator.py
- jq_interpreter/parser.py
- tests/test_cli_interface.py

## Pre-build acceptance observation
- RED: cli-001-single-input (FEATURE-CLI-001.md)
  intent: The executable evaluates a compact filter against one JSON input and emits the parsed result.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '.name'], returncode=3, stdout='', stderr='unexpected token at position 1\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-001-single-input.py", line 11, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: cli-001-multiple-inputs (FEATURE-CLI-001.md)
  intent: The executable processes multiple JSON texts from standard input independently and in order.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '.value'], returncode=3, stdout='', stderr='unexpected token at position 1\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-001-multiple-inputs.py", line 11, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: cli-001-generator-output (FEATURE-CLI-001.md)
  intent: The executable emits each generator result as a separate compact JSON line in generator order.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', 'range(3)'], returncode=3, stdout='', stderr='unexpected character at position 5\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-001-generator-output.py", line 11, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: cli-001-single-input (FEATURE-CLI-001.md)
  intent: The executable evaluates a compact filter against one JSON input and emits the parsed result.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-001-multiple-inputs (FEATURE-CLI-001.md)
  intent: The executable processes multiple JSON texts from standard input independently and in order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-001-generator-output (FEATURE-CLI-001.md)
  intent: The executable emits each generator result as a separate compact JSON line in generator order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Full jq conformance suite timed out.
- detail:
    The CLI acceptance behavior passes, but the required full corpus includes unsupported jq features and did not finish under the execution timeout. Extend parser/evaluator coverage and rerun `sh sources/full_test.sh`.

## Build summary
<reusable-compact filename="run_conformance.py">
Conformance runner for `sources/jq.test`; invokes `$JQ -c <program>` per case, compares JSON outputs structurally, requires compile errors as exit 3 and runtime errors as exit 5, skips declared exclusions, and returns 0 only when no cases fail or error.
</reusable-compact>

RESULT: FAILED

FILES CHANGED:
- jq
- jq_interpreter/parser.py
- jq_interpreter/evaluator.py
- jq_interpreter/cli.py
- tests/test_cli_interface.py

SUMMARY:
Implemented the executable `jq -c` interface. CLI tests pass: 7 tests green, including multiple inputs, generator output, and exit-code distinctions. Staged assets were preserved.

BLOCKERS:
- Full conformance did not complete within 30 seconds and timed out; broader jq language support remains incomplete.

FAILURE_SUMMARY: Full jq conformance suite timed out.
FAILURE_DETAIL: The CLI acceptance behavior passes, but the required full corpus includes unsupported jq features and did not finish under the execution timeout. Extend parser/evaluator coverage and rerun `sh sources/full_test.sh`.
