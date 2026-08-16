# Evidence: Block 4 · Service (block-4)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 45691
- execution id: 20260816.204408.297Z-baca52fd

## Stories built
- Parse jq programs into an executable abstract syntax tree. (parser) [story]

## Stacked context
- compass: COMPASS.md (SP 3836)
- implements: FEATURE-Parser.md (SP 675)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: jq-manual.txt (SP 32696)
- context: ARCHITECTURE_compact.md (SP 160)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq_parser.py
- tests/test_parser.py

## Pre-build acceptance observation
- RED: parser-builds-ast (FEATURE-Parser.md)
  intent: A valid jq program is parsed into a non-null AST.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      token = Token(kind='field', value='foo', position=0, line=1, column=1)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parser-builds-ast.py", line 3, in <module>
        ast = jq_parser.parse(".foo | .bar")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq/jq_parser.py", line 72, in parse
        tree = parser.expression()
               ^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq/jq_parser.py", line 36, in expression
        left = self.term()
               ^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq/jq_parser.py", line 66, in term
        raise ParseError(f"unexpected token at position {token.position}")
    jq_parser.ParseError: unexpected token at position 0
- RED: parser-preserves-precedence (FEATURE-Parser.md)
  intent: Arithmetic precedence is represented distinctly from addition.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      parser = <jq_parser.Parser object at 0x7e5c8c92c1d0>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parser-preserves-precedence.py", line 3, in <module>
        ast = jq_parser.parse("1 + 2 * 2")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq/jq_parser.py", line 74, in parse
        raise ParseError(f"unexpected token at position {parser.current().position}")
    jq_parser.ParseError: unexpected token at position 2
- RED: parser-supports-constructors (FEATURE-Parser.md)
  intent: Array and object construction parse successfully.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      token = Token(kind='delimiter', value='[', position=0, line=1, column=1)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "parser-supports-constructors.py", line 4, in <module>
        assert jq_parser.parse(program) is not None
               ^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq/jq_parser.py", line 72, in parse
        tree = parser.expression()
               ^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq/jq_parser.py", line 36, in expression
        left = self.term()
               ^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq/jq_parser.py", line 66, in term
        raise ParseError(f"unexpected token at position {token.position}")
    jq_parser.ParseError: unexpected token at position 0
- GREEN (prepassed): parser-rejects-malformed-program (FEATURE-Parser.md)
  intent: Unterminated syntax is rejected as a compile error by the parser boundary.
  return code: 0

## Post-build programmatic acceptance
- PASS: parser-builds-ast (FEATURE-Parser.md)
  intent: A valid jq program is parsed into a non-null AST.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: parser-preserves-precedence (FEATURE-Parser.md)
  intent: Arithmetic precedence is represented distinctly from addition.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: parser-supports-constructors (FEATURE-Parser.md)
  intent: Array and object construction parse successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: parser-rejects-malformed-program (FEATURE-Parser.md)
  intent: Unterminated syntax is rejected as a compile error by the parser boundary.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq_parser.py
- tests/test_parser.py

SUMMARY:
Implemented immutable, precedence-aware jq AST parsing with constructors, bindings, functions, control flow, reducers, indexing, interpolation, modules, and compile-time validation. All 17 tests pass.

BLOCKERS:
- None
