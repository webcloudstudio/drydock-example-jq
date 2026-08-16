# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-08-16
- resulting state: closed/verified
- story points (combined assembled cost): 67472
- execution id: 20260816.203700.681Z-e766cdd6

## Stories built
- Stage the supplied jq sources and conformance assets. (source-staging) [story]

## Reusable compacts
- full_test_compact.md
- run_conformance_compact.md
- exclusions_compact.md
- jq_compact.md
- jq-manual_compact.md
- lexer_compact.md
- parser_compact.md
- builtin_compact.md

## Stacked context
- compass: COMPASS.md (SP 3836)
- implements: FEATURE-Source-Staging.md (SP 624)
- context: full_test.sh (SP 189)
- context: run_conformance.py (SP 4354)
- context: exclusions.txt (SP 654)
- context: jq.test (SP 13058)
- context: jq-manual.txt (SP 32696)
- context: lexer.l (SP 1137)
- context: parser.y (SP 5596)
- context: builtin.jq (SP 2408)
- context: ARCHITECTURE_compact.md (SP 160)
- stack: python_compact.md (SP 1534)
- stack: common_compact.md (SP 1179)

## Build directory changes
- sources/INSTRUCTIONS.md
- tests/test_source_staging.py

## Pre-build acceptance observation
- RED: staging-complete (FEATURE-Source-Staging.md)
  intent: Every declared source asset is staged at its required build-relative path.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      paths = ['sources/INSTRUCTIONS.md', 'sources/builtin.jq', 'sources/exclusions.txt', 'sources/full_test.sh', 'sources/jq-manual.txt', 'sources/jq.test', 'sources/lexer.l', 'sources/parser.y', 'sources/run_conformance.py']
    --- drydock: end values ---
    Traceback (most recent call last):
      File "staging-complete.py", line 14, in <module>
        assert all(Path(path).is_file() for path in paths)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: staging-nonempty (FEATURE-Source-Staging.md)
  intent: Every staged source asset contains imported content.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      self = PosixPath('sources/INSTRUCTIONS.md')
      follow_symlinks = True
    --- drydock: end values ---
    Traceback (most recent call last):
      File "staging-nonempty.py", line 14, in <module>
        assert all(Path(path).stat().st_size > 0 for path in paths)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "staging-nonempty.py", line 14, in <genexpr>
        assert all(Path(path).stat().st_size > 0 for path in paths)
                   ^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pathlib.py", line 840, in stat
        return os.stat(self, follow_symlinks=follow_symlinks)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: 'sources/INSTRUCTIONS.md'
- GREEN (prepassed): staging-harness-executable (FEATURE-Source-Staging.md)
  intent: The supplied scoring entry point is executable by POSIX sh.
  return code: 0

## Post-build programmatic acceptance
- PASS: staging-complete (FEATURE-Source-Staging.md)
  intent: Every declared source asset is staged at its required build-relative path.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: staging-nonempty (FEATURE-Source-Staging.md)
  intent: Every staged source asset contains imported content.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- PASS: staging-harness-executable (FEATURE-Source-Staging.md)
  intent: The supplied scoring entry point is executable by POSIX sh.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="full_test.sh">
Runs `sources/run_conformance.py` from the application root with `JQ="$PWD/jq"`. Requires executable `./jq`; preserves harness exit status.
</reusable-compact>

<reusable-compact filename="run_conformance.py">
Parses `sources/jq.test`, applies exact exclusions, runs each case via `JQ`, compares structural JSON output and exit codes. Exit 0 means no failures/errors; 1 means candidate failure; 2 means harness fault. Compile errors must exit 3; runtime errors may exit 5.
</reusable-compact>

<reusable-compact filename="exclusions.txt">
Declares only module-loader corpus cases as skipped. Entries must match corpus program lines exactly; stale entries are harness errors.
</reusable-compact>

<reusable-compact filename="jq.test">
Pinned jq 1.8.2 conformance corpus. Cases contain program, input, and expected output lines; `%%FAIL` cases require compile exit 3.
</reusable-compact>

<reusable-compact filename="jq-manual.txt">
Normative jq language specification covering filters, generators, operators, builtins, control flow, variables, regex, modules, dates, streaming, and assignment.
</reusable-compact>

<reusable-compact filename="lexer.l">
Defines jq lexical tokens, comments, strings/interpolation, literals, identifiers, bindings, formats, operators, and delimiter state validation.
</reusable-compact>

<reusable-compact filename="parser.y">
Defines jq grammar, precedence, associativity, syntax validation, functions, patterns, modules, conditionals, generators, assignments, and compile-time diagnostics.
</reusable-compact>

<reusable-compact filename="builtin.jq">
Reference definitions for jq builtins including map/select, reductions, recursion, paths, strings, regex, control flow, dates, streaming, traversal, SQL-style helpers, and assignment support.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- sources/INSTRUCTIONS.md
- tests/test_source_staging.py

SUMMARY:
Staged the missing authoritative `INSTRUCTIONS.md`; verified all nine source assets are present, non-empty, and byte-stable. Added deterministic pytest coverage for asset staging and harness executability. Tests passed.

BLOCKERS:
- None
