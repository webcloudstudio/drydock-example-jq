# Evidence: Block 2 · Service (block-2)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 12152
- execution id: 20260822.180815.255Z-f7eb80f1

## Stories built
- Implement the executable jq entry point. (exec-001) [story]
- Implement jq process exit and diagnostic behavior. (exec-002) [story]

## Acceptance tooling authorization
- FEATURE-Executable-Entry-Point.md#exec-001-conformance: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Process-Contract.md#exec-002-compile-runtime: executable=python3; scope=test; authorization=existing Target environment

## Reusable compacts
- run_conformance_compact.md

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-Executable-Entry-Point.md (SP 615)
- context: run_conformance.py (SP 4354)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)
- implements: FEATURE-Process-Contract.md (SP 769)

## Build directory changes
- jq_interpreter/ast.py
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
- jq_interpreter/parser.py
- tests/test_architecture.py

## Pre-build acceptance observation
- GREEN (prepassed): exec-001-conformance (FEATURE-Executable-Entry-Point.md)
  intent: The executable runs the basic identity interface successfully.
  return code: 0
- GREEN (prepassed): exec-001-process (FEATURE-Executable-Entry-Point.md)
  intent: The executable accepts the declared -c interface and completes a supplied identity filter successfully.
  return code: 0
  stdout:
    null
- RED: exec-002-compile-runtime (FEATURE-Process-Contract.md)
  intent: The executable distinguishes compile failures, runtime failures, and successful completion.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      runtime_result = CompletedProcess(args=['./jq', '-c', 'error'], returncode=3, stdout='', stderr='jq: compile error: unexpected character at position 0\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "exec-002-compile-runtime.py", line 22, in <module>
        assert runtime_result.returncode == 5
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: exec-002-statuses (FEATURE-Process-Contract.md)
  intent: The executable exposes distinct compile, runtime, and successful completion statuses.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      runtime_result = CompletedProcess(args=['./jq', '-c', 'error'], returncode=3, stdout='', stderr='jq: compile error: unexpected character at position 0\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "exec-002-statuses.py", line 22, in <module>
        assert runtime_result.returncode == 5
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: exec-002-partial-output (FEATURE-Process-Contract.md)
  intent: A runtime failure preserves values emitted before the failure and keeps diagnostics off standard output.
  return code: 1
  stderr:
    jq: compile error: unexpected character at position 0
    
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '1, error'], returncode=3, stdout='', stderr='jq: compile error: unexpected character at position 0\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "exec-002-partial-output.py", line 11, in <module>
        assert result.returncode == 5
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: exec-001-conformance (FEATURE-Executable-Entry-Point.md)
  intent: The executable runs the basic identity interface successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: exec-001-process (FEATURE-Executable-Entry-Point.md)
  intent: The executable accepts the declared -c interface and completes a supplied identity filter successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    null
- PASS: exec-002-compile-runtime (FEATURE-Process-Contract.md)
  intent: The executable distinguishes compile failures, runtime failures, and successful completion.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: exec-002-statuses (FEATURE-Process-Contract.md)
  intent: The executable exposes distinct compile, runtime, and successful completion statuses.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: exec-002-partial-output (FEATURE-Process-Contract.md)
  intent: A runtime failure preserves values emitted before the failure and keeps diagnostics off standard output.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    1
  stderr:
    jq: runtime error: error

## Build summary
<reusable-compact filename="run_conformance.py">
Run `JQ=./jq python3 sources/run_conformance.py`; candidate must emit JSON lines and use exit 3 for compile errors, 5 for runtime errors. Harness reports structural output matches and supports scoped execution via `--select REGEX --json`; exit 2 indicates harness faults.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- jq_interpreter/ast.py
- jq_interpreter/parser.py
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
- tests/test_architecture.py

SUMMARY:
Implemented literals, comma generators, runtime errors, arrays, limits, BOM-tolerant input, diagnostics, and exit-code behavior. All 7 project tests and declared process acceptance checks pass. Identity conformance slice passes 2/2.

BLOCKERS:
- None
