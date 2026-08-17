# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 17537
- execution id: 20260817.025627.341Z-0902c853

## Stories built
- Define the standalone jq interpreter architecture and module boundaries. (architecture) [story]

## Reusable compacts
- ARCHITECTURE_compact.md
- parser_compact.md
- lexer_compact.md

## Stacked context
- compass: COMPASS.md (SP 3799)
- implements: ARCHITECTURE.md (SP 1219)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- stack: python.md (SP 3892)
- stack: common.md (SP 1807)

## Build directory changes
- README.md
- jq
- jq_interpreter/__init__.py
- jq_interpreter/builtins.py
- jq_interpreter/cli.py
- jq_interpreter/data_model.py
- jq_interpreter/diagnostics.py
- jq_interpreter/evaluator.py
- jq_interpreter/lexer.py
- jq_interpreter/parser.py
- jq_interpreter/paths.py
- tests/__init__.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: architecture-stream-contract (ARCHITECTURE.md)
  intent: The completed executable accepts the declared compact-filter interface and returns a valid JSON value derived from supplied input.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-stream-contract.py", line 6, in <module>
        result = subprocess.run(
                 ^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 548, in run
        with Popen(*popenargs, **kwargs) as process:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1026, in __init__
        self._execute_child(args, executable, preexec_fn, close_fds,
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1955, in _execute_child
        raise child_exception_type(errno_num, err_msg, err_filename)
    FileNotFoundError: [Errno 2] No such file or directory: './jq'
- RED: architecture-generator-order (ARCHITECTURE.md)
  intent: The evaluator preserves ordered generator multiplicity for comma expressions.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-generator-order.py", line 6, in <module>
        result = subprocess.run(
                 ^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 548, in run
        with Popen(*popenargs, **kwargs) as process:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1026, in __init__
        self._execute_child(args, executable, preexec_fn, close_fds,
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1955, in _execute_child
        raise child_exception_type(errno_num, err_msg, err_filename)
    FileNotFoundError: [Errno 2] No such file or directory: './jq'
- RED: architecture-runtime-status (ARCHITECTURE.md)
  intent: Runtime failures use the documented runtime exit status while keeping diagnostics off standard output.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      errno_num = 2
      err_msg = 'No such file or directory'
      err_filename = './jq'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-runtime-status.py", line 3, in <module>
        result = subprocess.run(
                 ^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 548, in run
        with Popen(*popenargs, **kwargs) as process:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1026, in __init__
        self._execute_child(args, executable, preexec_fn, close_fds,
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/subprocess.py", line 1955, in _execute_child
        raise child_exception_type(errno_num, err_msg, err_filename)
    FileNotFoundError: [Errno 2] No such file or directory: './jq'

## Post-build programmatic acceptance
- PASS: architecture-stream-contract (ARCHITECTURE.md)
  intent: The completed executable accepts the declared compact-filter interface and returns a valid JSON value derived from supplied input.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-generator-order (ARCHITECTURE.md)
  intent: The evaluator preserves ordered generator multiplicity for comma expressions.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-runtime-status (ARCHITECTURE.md)
  intent: Runtime failures use the documented runtime exit status while keeping diagnostics off standard output.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
Standalone Python jq interpreter contract: executable `./jq -c '<program>'`; JSON stdin to compact JSON lines on stdout. Exit `0` success, `3` compile/static failure, `5` runtime failure. Boundaries: CLI, lexer, parser/compiler, lazy evaluator, data model, paths/mutation, builtins, diagnostics, verification. Standard library only; no persistence, network, system jq, or third-party jq implementation. Evaluator preserves ordered generator multiplicity and partial output before runtime errors.
</reusable-compact>

<reusable-compact filename="parser.y">
Parser contract: jq supports identity `.`, literals, comma generators, field/index access, slices, arrays/objects, operators, conditionals, try/catch, reduce/foreach, bindings/patterns, functions, modules/imports, interpolation, formats, and assignments. Operator precedence is defined by the grammar; compile errors must be distinct from runtime errors. Module syntax must parse and reject invalid metadata without filesystem access.
</reusable-compact>

<reusable-compact filename="lexer.l">
Lexer contract: recognize jq keywords, identifiers, bindings, fields, literals, formats, comments, operators, delimiters, recursive descent, strings with JSON escapes, and string interpolation. Preserve source locations and reject invalid characters or malformed literals during compilation.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- README.md
- jq
- jq_interpreter/__init__.py
- jq_interpreter/builtins.py
- jq_interpreter/cli.py
- jq_interpreter/data_model.py
- jq_interpreter/diagnostics.py
- jq_interpreter/evaluator.py
- jq_interpreter/lexer.py
- jq_interpreter/parser.py
- jq_interpreter/paths.py
- tests/__init__.py
- tests/test_architecture.py

SUMMARY:
Implemented the standalone Python interpreter architecture with clear module boundaries, executable `jq` contract, lazy ordered generators, distinct exit statuses, README documentation, and focused tests. All 3 declared acceptance assertions and 4 project tests pass. Staged source assets remain unchanged.

BLOCKERS:
- None
