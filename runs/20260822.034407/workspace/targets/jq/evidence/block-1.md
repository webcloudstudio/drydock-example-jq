# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 10342
- execution id: 20260822.040932.089Z-ac3cfa8b

## Stories built
- Define the standalone jq interpreter architecture and module boundaries. (architecture) [story]

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: ARCHITECTURE.md (SP 956)
- context: TECHNOLOGY_STACK.md (SP 200)
- stack: common.md (SP 1807)
- stack: python.md (SP 3892)

## Build directory changes
- COMPASS.md
- jq
- jq_interpreter/__init__.py
- jq_interpreter/ast.py
- jq_interpreter/builtins.py
- jq_interpreter/cli.py
- jq_interpreter/errors.py
- jq_interpreter/evaluator.py
- jq_interpreter/lexer.py
- jq_interpreter/parser.py
- jq_interpreter/paths.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: architecture-contract (ARCHITECTURE.md)
  intent: The architecture contract exposes the required interpreter boundary and exit-code constants.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('COMPASS.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-contract.py", line 3, in <module>
        compass = Path("COMPASS.md").read_text(encoding="utf-8")
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'COMPASS.md'
- GREEN (prepassed): architecture-assets (ARCHITECTURE.md)
  intent: The architecture preserves the complete, mutually consistent, read-only language and conformance asset boundary.
  return code: 0

## Post-build programmatic acceptance
- PASS: architecture-contract (ARCHITECTURE.md)
  intent: The architecture contract exposes the required interpreter boundary and exit-code constants.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-assets (ARCHITECTURE.md)
  intent: The architecture preserves the complete, mutually consistent, read-only language and conformance asset boundary.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Repair attempts
- attempt 0 (initial build): failed; 1/2 checks model=gpt-5.6-luna; execution 20260822.040633.294Z-e7592f81; reason: programmatic acceptance failed: architecture-contract
- attempt 1 (repair 1): built; 2/2 checks model=gpt-5.6-luna; execution 20260822.040932.089Z-ac3cfa8b

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
Standalone Python 3.11+ jq interpreter using standard library only. Executable `jq` accepts `-c '<program>'`, reads JSON lines from stdin, evaluates ordered generator streams, and emits compact JSON lines.

Boundaries: lexer/source locations; parser/AST; evaluator/generator control flow; paths/updates; builtins; CLI and exit handling. Preserve ordering, multiplicity, cartesian pipelines, backtracking, and partial output before runtime errors.

Exit codes: 0 success, 3 compile failure, 5 runtime failure. No system jq, third-party runtime, network, or source-asset modifications. Required source assets remain read-only.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- COMPASS.md

SUMMARY:
Added the missing build-root architecture compass with the required standalone-interpreter and exit-code contract. Architecture contract, asset consistency checks, four project tests, and CLI smoke test pass.

BLOCKERS:
- None
