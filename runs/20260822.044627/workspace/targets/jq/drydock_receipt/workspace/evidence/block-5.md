# Evidence: Block 5 · Foundational (block-5)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 66764
- execution id: 20260822.195319.493Z-08895953

## Stories built
- Stage and validate immutable conformance assets. (CONF-001) [story]

## Acceptance tooling authorization
- FEATURE-CONF-001.md#conf-001-assets: executable=python3; scope=test; authorization=existing Target environment

## Reusable compacts
- full_test_compact.md
- exclusions_compact.md
- jq-manual_compact.md
- parser_compact.md
- lexer_compact.md
- builtin_compact.md

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-CONF-001.md (SP 339)
- context: run_conformance.py (SP 4354)
- context: full_test.sh (SP 189)
- context: exclusions.txt (SP 654)
- context: jq.test (SP 13058)
- context: jq-manual.txt (SP 32696)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: builtin.jq (SP 2408)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- tests/test_conf_001_acceptance.py

## Pre-build acceptance observation
- GREEN (prepassed): conf-001-assets (FEATURE-CONF-001.md)
  intent: The staged corpus parses into the authoritative case set and all declared exclusions match cases.
  return code: 0

## Post-build programmatic acceptance
- PASS: conf-001-assets (FEATURE-CONF-001.md)
  intent: The staged corpus parses into the authoritative case set and all declared exclusions match cases.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="full_test.sh">
Executable `./jq` must exist and be executable. Runs the full corpus via `JQ="$PWD/jq" exec python3 sources/run_conformance.py`; exits nonzero on interface or conformance failure.
</reusable-compact>

<reusable-compact filename="exclusions.txt">
Contains 13 verbatim corpus program lines excluded due to unavailable module-loader fixtures. Exclusions must match corpus programs exactly; stale entries are errors.
</reusable-compact>

<reusable-compact filename="jq-manual.txt">
Normative jq language specification: filters, generators, operators, builtins, variables, functions, paths, assignments, regex, dates, I/O, streaming, and modules.
</reusable-compact>

<reusable-compact filename="parser.y">
Defines jq grammar, precedence, literals, filters, functions, imports, modules, variables, destructuring, assignments, reductions, conditionals, errors, and object/array construction. Compile failures must map to exit code 3.
</reusable-compact>

<reusable-compact filename="lexer.l">
Defines jq lexical tokens, comments, operators, identifiers, fields, bindings, literals, strings/interpolation, formats, and delimiter state handling.
</reusable-compact>

<reusable-compact filename="builtin.jq">
Defines jq standard-library functions including collection, path, string, regex, generator, reduction, assignment, date, streaming, SQL-style, and type-selection builtins.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- tests/test_conf_001_acceptance.py

SUMMARY:
Staged assets validated in process: 550 corpus cases and 13 exclusions. Full local test suite passes: 21 tests.

BLOCKERS:
- None
