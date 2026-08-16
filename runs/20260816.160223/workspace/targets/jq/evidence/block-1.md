# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 11180
- execution id: 20260816.161950.832Z-39e754cd

## Stories built
- Define the self-contained jq interpreter architecture and module boundaries. (architecture) [story]
- Stage the supplied jq conformance assets and harness. (verify-assets) [story]

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- compass: COMPASS.md (SP 3787)
- implements: ARCHITECTURE.md (SP 1080)
- context: TECHNOLOGY_STACK.md (SP 200)
- stack: python.md (SP 3892)
- stack: common.md (SP 1807)
- implements: FEATURE-Verification-Assets.md (SP 302)
- context: ARCHITECTURE.md (SP 1080)

## Build directory changes
- README.md
- jq
- jq_cli.py
- jq_evaluator.py
- jq_lexer.py
- jq_parser.py
- jq_values.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: architecture-runtime (ARCHITECTURE.md)
  intent: The implementation architecture exposes a runnable root-level jq executable using the declared Python standard-library boundary.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      executable = PosixPath('jq')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-runtime.py", line 6, in <module>
        assert executable.is_file()
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: architecture-stream (ARCHITECTURE.md)
  intent: The architecture preserves the ordered multi-output generator contract.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3', 'jq', '-c', '[.[]]'], returncode=2, stdout='', stderr="/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3: can't open file '/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.160223/build/jq/jq': [Errno 2] No such file or directory\n")
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-stream.py", line 13, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: architecture-dependencies (ARCHITECTURE.md)
  intent: The executable runs without requiring third-party runtime packages or network access.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3', 'jq', '-c', '.'], returncode=2, stdout='', stderr="/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3: can't open file '/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.160223/build/jq/jq': [Errno 2] No such file or directory\n")
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-dependencies.py", line 10, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: architecture-runtime (ARCHITECTURE.md)
  intent: The implementation architecture exposes a runnable root-level jq executable using the declared Python standard-library boundary.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-stream (ARCHITECTURE.md)
  intent: The architecture preserves the ordered multi-output generator contract.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-dependencies (ARCHITECTURE.md)
  intent: The executable runs without requiring third-party runtime packages or network access.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Full conformance suite failed
- detail:
    The foundational interpreter supports only a small expression subset; 501 corpus cases fail and require downstream parser, evaluator, builtin, control-flow, and path implementation blocks.

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
Root executable `jq` delegates to Python standard-library CLI, lexer, parser, values, evaluator, control, paths, and builtins boundaries. Evaluation is generator-based and preserves ordered streams/backtracking. Compile errors exit 3; runtime errors exit 5; prior outputs remain emitted. No third-party dependencies, jq subprocesses, or network access.
</reusable-compact>

RESULT: FAILED

FILES CHANGED:
- jq
- jq_cli.py
- jq_evaluator.py
- jq_lexer.py
- jq_parser.py
- jq_values.py
- README.md
- tests/test_architecture.py

SUMMARY:
Implemented the foundational executable architecture. All three declared architecture assertions and three local tests pass. Supplied assets remained unchanged. Full conformance currently reports 36 passed, 501 failed, 0 errored, 13 skipped.

BLOCKERS:
- Full jq conformance is not yet implemented.

FAILURE_SUMMARY: Full conformance suite failed

FAILURE_DETAIL: The foundational interpreter supports only a small expression subset; 501 corpus cases fail and require downstream parser, evaluator, builtin, control-flow, and path implementation blocks.
