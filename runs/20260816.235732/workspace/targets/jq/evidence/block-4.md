# Evidence: Block 4 · Service (block-4)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 60150
- execution id: 20260817.001406.115Z-748d6118

## Stories built
- Implement jq lexical analysis for the supported language surface. (frontend-lexer) [story]

## Reusable compacts
- lexer_compact.md
- parser_compact.md
- jq_compact.md

## Stacked context
- compass: COMPASS.md (SP 3821)
- implements: FEATURE-FRONTEND-LEXER.md (SP 920)
- context: lexer.l (SP 1137)
- context: parser.y (SP 5596)
- context: jq-manual.txt (SP 32696)
- context: jq.test (SP 13058)
- context: ARCHITECTURE_compact.md (SP 147)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)

## Build directory changes
- jq
- lexer.py
- tests/test_lexer.py

## Pre-build acceptance observation
- GREEN (prepassed): lexer-literals (FEATURE-FRONTEND-LEXER.md)
  intent: Lexically valid literal and format tokens are accepted through the executable boundary and preserve their supplied values.
  return code: 0
  stdout:
    "alpha"
- RED: lexer-interpolation (FEATURE-FRONTEND-LEXER.md)
  intent: String interpolation lexical boundaries are accepted and produce a value derived from supplied input.
  return code: 1
  stdout:
    compile error: Invalid \escape: line 1 column 8 (char 7)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '"value=\\(.)"'], returncode=3, stdout='', stderr='compile error: Invalid \\escape: line 1 column 8 (char 7)\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "lexer-interpolation.py", line 16, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: lexer-comments-and-operators (FEATURE-FRONTEND-LEXER.md)
  intent: Comments and operator tokens are ignored or recognized without changing the evaluated result.
  return code: 1
  stdout:
    compile error: invalid token
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['./jq', '-c', '1 + . # trailing comment'], returncode=3, stdout='', stderr='compile error: invalid token\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "lexer-comments-and-operators.py", line 16, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): lexer-invalid-escape (FEATURE-FRONTEND-LEXER.md)
  intent: An invalid string escape is rejected as a compile error.
  return code: 0
  stdout:
    compile error: Invalid \escape: line 1 column 3 (char 2)

## Post-build programmatic acceptance
- PASS: lexer-literals (FEATURE-FRONTEND-LEXER.md)
  intent: Lexically valid literal and format tokens are accepted through the executable boundary and preserve their supplied values.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    "alpha"
- PASS: lexer-interpolation (FEATURE-FRONTEND-LEXER.md)
  intent: String interpolation lexical boundaries are accepted and produce a value derived from supplied input.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    "value=7"
- PASS: lexer-comments-and-operators (FEATURE-FRONTEND-LEXER.md)
  intent: Comments and operator tokens are ignored or recognized without changing the evaluated result.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    3
- PASS: lexer-invalid-escape (FEATURE-FRONTEND-LEXER.md)
  intent: An invalid string escape is rejected as a compile error.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
  stdout:
    compile error: invalid escape \v

## Build summary
<reusable-compact filename="lexer.l">
Recognize jq keywords, literals, identifiers, fields, bindings, formats, operators, delimiters, comments, quoted strings, and interpolation boundaries. Reject invalid escapes, characters, and mismatched delimiters as compile errors.
</reusable-compact>

<reusable-compact filename="parser.y">
Lexer tokens must preserve literal values and source locations. Supported tokens include identifiers, fields, bindings, literals, formats, operators, delimiters, keywords, and interpolation markers; lexical errors propagate as compile errors.
</reusable-compact>

<reusable-compact filename="jq.test">
The corpus validates strings, escapes, interpolation, comments, operators, formats, keywords, delimiters, and compile-error exit status 3. Runtime results use compact JSON streams and exit status 5 for runtime errors.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- jq
- lexer.py
- tests/test_lexer.py

SUMMARY:
Implemented located standard-library jq lexing with comments, literals, names, bindings, formats, operators, strings, interpolation validation, and lexical errors. All 4 declared acceptance checks and 8 local tests pass. Full conformance was attempted but hung in an existing broader runtime case before producing a verdict.

BLOCKERS:
- Full supplied conformance suite did not complete; broader runtime work remains.
