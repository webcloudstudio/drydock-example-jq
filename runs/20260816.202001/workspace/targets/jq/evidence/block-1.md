# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 10729
- execution id: 20260816.203343.576Z-946ae603

## Stories built
- Define the standalone jq interpreter architecture and executable boundaries. (architecture) [story]

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- compass: COMPASS.md (SP 3836)
- implements: ARCHITECTURE.md (SP 1125)
- stack: python.md (SP 3892)
- stack: common.md (SP 1807)

## Build directory changes
- README.md
- jq
- jq_builtins.py
- jq_cli.py
- jq_lexer.py
- jq_parser.py
- jq_runtime.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: architecture-lexer-contract (ARCHITECTURE.md)
  intent: The lexer module exposes a callable tokenization boundary.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "architecture-lexer-contract.py", line 1, in <module>
        import jq_lexer
    ModuleNotFoundError: No module named 'jq_lexer'
- RED: architecture-parser-contract (ARCHITECTURE.md)
  intent: The parser module exposes a callable AST construction boundary.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "architecture-parser-contract.py", line 1, in <module>
        import jq_parser
    ModuleNotFoundError: No module named 'jq_parser'
- RED: architecture-runtime-contract (ARCHITECTURE.md)
  intent: The runtime module exposes generator evaluation.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "architecture-runtime-contract.py", line 1, in <module>
        import jq_runtime
    ModuleNotFoundError: No module named 'jq_runtime'
- RED: architecture-no-third-party-runtime (ARCHITECTURE.md)
  intent: The architecture remains executable with the Python standard library.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('jq_runtime.py')
      mode = 'r'
      buffering = -1
      encoding = 'utf-8'
      errors = None
      newline = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-no-third-party-runtime.py", line 4, in <module>
        source = Path("jq_runtime.py").read_text(encoding="utf-8")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1027, in read_text
        with self.open(mode='r', encoding=encoding, errors=errors) as f:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 1013, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'jq_runtime.py'

## Post-build programmatic acceptance
- PASS: architecture-lexer-contract (ARCHITECTURE.md)
  intent: The lexer module exposes a callable tokenization boundary.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-parser-contract (ARCHITECTURE.md)
  intent: The parser module exposes a callable AST construction boundary.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-runtime-contract (ARCHITECTURE.md)
  intent: The runtime module exposes generator evaluation.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-no-third-party-runtime (ARCHITECTURE.md)
  intent: The architecture remains executable with the Python standard library.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
- Python standard-library jq architecture with boundaries: `jq_lexer.tokenize`, `jq_parser.parse`, generator-based `jq_runtime.evaluate`, builtin registry, CLI, and executable `jq`.
- `./jq -c '<program>'` reads newline-delimited JSON and emits compact result streams.
- Exit codes: 0 success, 3 compile failure, 5 runtime failure; diagnostics stderr only.
- Preserve ordered generator semantics and partial output; prohibit third-party dependencies, network, subprocesses, and system jq.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- README.md
- jq
- jq_builtins.py
- jq_cli.py
- jq_lexer.py
- jq_parser.py
- jq_runtime.py
- tests/test_architecture.py

SUMMARY:
Implemented the standalone jq architecture and executable boundaries. All declared acceptance assertions pass, along with 4 focused architecture tests and CLI smoke checks.

BLOCKERS:
- None
