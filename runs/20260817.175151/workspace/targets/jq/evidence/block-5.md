# Evidence: Block 5 · Service (block-5)

- block type: block
- date: 2026-08-17
- resulting state: closed/verified
- story points (combined assembled cost): 43647
- execution id: 20260817.181512.872Z-4f65c40f

## Stories built
- Parse jq source into an executable representation. (front-parser) [story]

## Stacked context
- compass: COMPASS.md (SP 2068)
- implements: FEATURE-Front-Parser.md (SP 574)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: jq-manual.txt (SP 32696)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- tests/test_front_parser.py

## Pre-build acceptance observation
- RED: front-parser-precedence (FEATURE-Front-Parser.md)
  intent: The parser accepts grouped arithmetic with jq precedence and executes the resulting representation.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '(1 + 2) * 3'], returncode=3, stdout='', stderr='jq: unsupported jq program\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "front-parser-precedence.py", line 14, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: front-parser-construction (FEATURE-Front-Parser.md)
  intent: The parser accepts array and object construction expressions.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '{value: ., items: [., 2]}'], returncode=3, stdout='', stderr='jq: unsupported jq program\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "front-parser-construction.py", line 15, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): front-parser-invalid-structure (FEATURE-Front-Parser.md)
  intent: An unterminated parser construct returns the compile-failure status.
  return code: 0

## Post-build programmatic acceptance
- PASS: front-parser-precedence (FEATURE-Front-Parser.md)
  intent: The parser accepts grouped arithmetic with jq precedence and executes the resulting representation.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: front-parser-construction (FEATURE-Front-Parser.md)
  intent: The parser accepts array and object construction expressions.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: front-parser-invalid-structure (FEATURE-Front-Parser.md)
  intent: An unterminated parser construct returns the compile-failure status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- jq
- tests/test_front_parser.py

SUMMARY:
Implemented jq AST parsing/evaluation for arithmetic, construction, indexing, slicing, conditionals, bindings, and core functions. All acceptance checks and unit tests pass.

BLOCKERS:
- None
