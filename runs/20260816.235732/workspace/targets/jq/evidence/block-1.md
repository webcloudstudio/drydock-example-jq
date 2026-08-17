# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 43668
- execution id: 20260817.000818.516Z-e40c4c16

## Stories built
- Define the standalone jq interpreter architecture and module boundaries. (architecture) [story]
- Declare jq Interpreter project identity and delivery metadata. (metadata) [story]

## Reusable compacts
- ARCHITECTURE_compact.md
- jq-manual_compact.md

## Stacked context
- compass: COMPASS.md (SP 3821)
- implements: ARCHITECTURE.md (SP 1031)
- context: TECHNOLOGY_STACK.md (SP 200)
- context: jq-manual.txt (SP 32696)
- stack: common.md (SP 1807)
- stack: python.md (SP 3892)
- implements: METADATA.md (SP 116)

## Build directory changes
- ARCHITECTURE.md
- METADATA.md
- tests/test_foundation.py

## Pre-build acceptance observation
- RED: architecture-contract (ARCHITECTURE.md)
  intent: The architecture contract declares the executable boundary and required exit statuses.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('ARCHITECTURE.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-contract.py", line 3, in <module>
        text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'ARCHITECTURE.md'
- RED: architecture-stack (ARCHITECTURE.md)
  intent: The architecture records the approved standard-library implementation boundary.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('ARCHITECTURE.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-stack.py", line 3, in <module>
        text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'ARCHITECTURE.md'
- RED: architecture-boundaries (ARCHITECTURE.md)
  intent: The architecture assigns ownership for the interpreter's required technical boundaries.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('ARCHITECTURE.md')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-boundaries.py", line 3, in <module>
        text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'ARCHITECTURE.md'

## Post-build programmatic acceptance
- PASS: architecture-contract (ARCHITECTURE.md)
  intent: The architecture contract declares the executable boundary and required exit statuses.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-stack (ARCHITECTURE.md)
  intent: The architecture records the approved standard-library implementation boundary.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-boundaries (ARCHITECTURE.md)
  intent: The architecture assigns ownership for the interpreter's required technical boundaries.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
Standalone Python 3.11+ standard-library jq CLI. Root `./jq` accepts `-c '<program>'`, reads JSON stdin, emits compact JSON lines stdout, diagnostics stderr, and uses exit codes 0 success, 3 compile/static failure, 5 runtime failure. Modules: executable boundary, Lexer, Parser/AST, generator-based Runtime, Values, Paths/assignments, and Builtins. Preserve generator order/multiplicity and never invoke external jq or modify `sources/`.
</reusable-compact>

<reusable-compact filename="jq-manual.txt">
jq filters transform one input into zero or more outputs. Core contracts include generator backtracking, left-to-right comma streams, pipe fan-out, JSON-native values, path-based access and assignment, lexical variables/functions, control flow, builtins, regex/string formatting, dates, streaming, and stdin-based input. Output is compact JSON per line; errors are diagnosable and catchable where specified.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- ARCHITECTURE.md
- METADATA.md
- tests/test_foundation.py

SUMMARY:
Created the foundational architecture and project metadata. Added three passing deterministic contract tests. Staged source assets remain unchanged.

BLOCKERS:
- None.
