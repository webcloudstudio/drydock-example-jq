# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-08-20
- resulting state: closed/verified
- story points (combined assembled cost): 49244
- execution id: 20260820.230238.842Z-1df9cad8

## Stories built
- Define interpreter modules and execution boundaries. (architecture) [story]

## Reusable compacts
- ARCHITECTURE_compact.md
- jq-manual_compact.md
- lexer_compact.md
- parser_compact.md
- builtin_compact.md

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: ARCHITECTURE.md (SP 1219)
- context: jq-manual.txt (SP 32696)
- context: lexer.l (SP 1137)
- context: parser.y (SP 5596)
- context: builtin.jq (SP 2408)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)

## Build directory changes
- ARCHITECTURE.md

## Pre-build acceptance observation
- RED: architecture-boundaries (ARCHITECTURE.md)
  intent: The architecture records every required interpreter boundary and the generator evaluation model.
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
- RED: architecture-stack (ARCHITECTURE.md)
  intent: The architecture records the approved standard-library-only implementation constraint.
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

## Post-build programmatic acceptance
- PASS: architecture-boundaries (ARCHITECTURE.md)
  intent: The architecture records every required interpreter boundary and the generator evaluation model.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: architecture-stack (ARCHITECTURE.md)
  intent: The architecture records the approved standard-library-only implementation constraint.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
Defines lexer, parser, evaluator, path/assignment, control/binding, builtin, and executable boundaries. Requires lazy generator streams, immutable values, standard-library-only Python 3.11+, POSIX sh, and exit codes 3/5 for compile/runtime failures.
</reusable-compact>

<reusable-compact filename="jq-manual.txt">
Normative jq language contract: filters are ordered generators over JSON values, with composition, operators, builtins, variables, functions, recursion, assignments, regex, I/O, streaming, and modules.
</reusable-compact>

<reusable-compact filename="lexer.l">
Lexer contract covering comments, identifiers, fields, bindings, literals, strings/interpolation, formats, operators, delimiters, and lexical state for parentheses, brackets, braces, interpolation, and comments.
</reusable-compact>

<reusable-compact filename="parser.y">
Parser contract covering jq precedence/associativity, AST construction, functions, modules/imports, patterns, bindings, assignments, conditionals, try/catch, reductions, foreach, interpolation, indexing, slicing, objects, and arrays.
</reusable-compact>

<reusable-compact filename="builtin.jq">
Builtin surface includes collection, traversal, assignment, recursion, string/regex, numeric/date, generator, streaming, environment/I/O, and SQL-style filters; builtins preserve jq generator semantics.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- ARCHITECTURE.md

SUMMARY:
Added the foundational jq interpreter architecture specification and verified both declared acceptance checks. No conformance suite was run because this architecture step declares no harness criterion.

BLOCKERS:
- None
