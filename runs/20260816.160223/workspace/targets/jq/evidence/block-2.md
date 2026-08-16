# Evidence: Block 2 · Service (block-2)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 11883
- execution id: 20260816.162359.423Z-04f04678

## Stories built
- Implement the executable jq entry point and JSON stdin/stdout loop. (cli-entrypoint) [story]

## Reusable compacts
- full_test_compact.md
- run_conformance_compact.md

## Stacked context
- compass: COMPASS.md (SP 3787)
- implements: FEATURE-CLI-Entrypoint.md (SP 650)
- context: full_test.sh (SP 189)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 126)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- jq_cli.py
- jq_evaluator.py
- jq_lexer.py
- jq_parser.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: cli-input-output (FEATURE-CLI-Entrypoint.md)
  intent: The executable evaluates a jq program against stdin and emits compact JSON values.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '. + 1'], returncode=3, stdout='', stderr='expected EOF\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-input-output.py", line 12, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): cli-multiple-inputs (FEATURE-CLI-Entrypoint.md)
  intent: Each newline-delimited JSON input is processed and emitted in order.
  return code: 0
- GREEN (prepassed): cli-generator-output (FEATURE-CLI-Entrypoint.md)
  intent: Multiple values produced by one filter are emitted as separate compact JSON lines.
  return code: 0

## Post-build programmatic acceptance
- PASS: cli-input-output (FEATURE-CLI-Entrypoint.md)
  intent: The executable evaluates a jq program against stdin and emits compact JSON values.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-multiple-inputs (FEATURE-CLI-Entrypoint.md)
  intent: Each newline-delimited JSON input is processed and emitted in order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: cli-generator-output (FEATURE-CLI-Entrypoint.md)
  intent: Multiple values produced by one filter are emitted as separate compact JSON lines.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Full conformance suite timed out.
- detail:
    The CLI block is implemented and focused tests pass, but broader interpreter constructs cause the staged conformance run to exceed the timeout; complete the interpreter core before rerunning.

## Build summary
<reusable-compact filename="full_test.sh">
Requires executable `./jq`; runs `python3 sources/run_conformance.py` with `JQ="$PWD/jq"`. Exit status is the acceptance verdict.
</reusable-compact>

<reusable-compact filename="run_conformance.py">
Runs newline-delimited jq corpus cases, compares structured JSON outputs, requires compile errors to exit 3 and runtime errors to exit 5, and returns 0 only when all non-skipped cases pass.
</reusable-compact>

RESULT: FAILED

FILES CHANGED:
- jq_cli.py
- jq_lexer.py
- jq_parser.py
- jq_evaluator.py
- tests/test_architecture.py

SUMMARY:
CLI acceptance tests pass: arithmetic, multiple inputs, compact output, and generator ordering. Project tests: 6 passed. Full conformance timed out after 25 seconds because the existing interpreter remains incomplete beyond this CLI block.

BLOCKERS:
- Full `sources/full_test.sh` conformance does not complete successfully.

FAILURE_SUMMARY: Full conformance suite timed out.
FAILURE_DETAIL: The CLI block is implemented and focused tests pass, but broader interpreter constructs cause the staged conformance run to exceed the timeout; complete the interpreter core before rerunning.
