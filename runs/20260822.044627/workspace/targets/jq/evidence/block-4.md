# Evidence: Block 4 · Foundational (block-4)

- block type: block
- date: 2026-08-22
- resulting state: closed/failed
- story points (combined assembled cost): 66947
- execution id: 20260822.181613.175Z-5ac5befb

## Stories built
- Stage and validate immutable conformance assets. (conf-001) [story]

## Acceptance tooling authorization
- FEATURE-Conformance-Assets.md#conformance-assets: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Conformance-Assets.md#conformance-source-integrity: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: FEATURE-Conformance-Assets.md (SP 513)
- context: run_conformance.py (SP 4354)
- context: jq.test (SP 13058)
- context: exclusions.txt (SP 654)
- context: full_test.sh (SP 189)
- context: jq-manual.txt (SP 32696)
- context: parser.y (SP 5596)
- context: lexer.l (SP 1137)
- context: builtin.jq (SP 2408)
- context: ARCHITECTURE_compact.md (SP 154)
- stack: common_compact.md (SP 1179)
- stack: python_compact.md (SP 1534)

## Build directory changes
- tests/test_conformance_assets.py

## Pre-build acceptance observation
- GREEN (prepassed): conformance-assets (FEATURE-Conformance-Assets.md)
  intent: The staged corpus and exclusions parse successfully and remain mutually consistent with the pinned authoritative assets.
  return code: 0
- RED: conformance-source-integrity (FEATURE-Conformance-Assets.md)
  intent: The staged harness exposes the required corpus and exclusion paths and can be imported from the build directory.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      sources = PosixPath('sources')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "conformance-source-integrity.py", line 10, in <module>
        assert run_conformance.CORPUS == sources / "jq.test"
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: conformance-assets (FEATURE-Conformance-Assets.md)
  intent: The staged corpus and exclusions parse successfully and remain mutually consistent with the pinned authoritative assets.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 0
- FAIL: conformance-source-integrity (FEATURE-Conformance-Assets.md)
  intent: The staged harness exposes the required corpus and exclusion paths and can be imported from the build directory.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python3
  provisioning: not required
  return code: 1
  stderr:
    --- drydock: values at failure ---
      sources = PosixPath('sources')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "conformance-source-integrity.py", line 10, in <module>
        assert run_conformance.CORPUS == sources / "jq.test"
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Repair attempts
- attempt 0 (initial build): failed; 1/2 checks model=gpt-5.6-luna; execution 20260822.181425.006Z-1c5cc8b9; reason: programmatic acceptance failed: conformance-source-integrity
- attempt 1 (repair 1): failed; 1/2 checks model=gpt-5.6-luna; execution 20260822.181529.735Z-dcc737fd; reason: programmatic acceptance failed: conformance-source-integrity
- attempt 2 (repair 2): failed; 1/2 checks model=gpt-5.6-luna; execution 20260822.181613.175Z-5ac5befb; stopped: deterministic acceptance score did not improve on 2 consecutive calls; reason: programmatic acceptance failed: conformance-source-integrity

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Source-integrity criterion compares absolute and relative paths.
- detail:
    `run_conformance.CORPUS` is `/.../sources/jq.test` because the immutable harness uses `Path(__file__).resolve()`, while the criterion expects `sources/jq.test`; modifying sources is forbidden.

## Failure
- summary: programmatic acceptance failed: conformance-source-integrity
- detail:
    Block "Block 4 · Foundational" [block-4] failed its acceptance criteria.
      Story "Stage and validate immutable conformance assets." [conf-001] does not meet its own acceptance criteria:
        - AC conformance-source-integrity — The staged harness exposes the required corpus and exclusion paths and can be imported from the build directory.
            assertion: assert run_conformance.CORPUS == sources / "jq.test" → AssertionError
            raised at: conformance-source-integrity.py:10
            process exit code: 1
            values at failure:
              sources = PosixPath('sources')
            check stderr:
              Traceback (most recent call last):
                File "conformance-source-integrity.py", line 10, in <module>
                  assert run_conformance.CORPUS == sources / "jq.test"
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError

## Build summary
<reusable-compact filename="exclusions.txt">
One verbatim jq program per exclusion; comments document reasons. Entries must match corpus programs exactly. Stale entries are harness errors. Excludes only module-loader cases.
</reusable-compact>

<reusable-compact filename="full_test.sh">
Executable scoring entry point. Requires executable ./jq, sets JQ to it, and runs the supplied harness over the full corpus. Exit status is the conformance verdict.
</reusable-compact>

<reusable-compact filename="parser.y">
Defines jq grammar, expressions, filters, functions, imports, variables, generators, assignments, conditionals, patterns, and compile-error behavior. Compile failures must remain distinct from runtime failures.
</reusable-compact>

<reusable-compact filename="lexer.l">
Defines jq tokens, operators, literals, identifiers, bindings, fields, strings/interpolation, comments, formats, and delimiter state validation.
</reusable-compact>

<reusable-compact filename="builtin.jq">
Defines jq standard-library filters for mapping, reduction, iteration, paths, assignment, strings, regex, dates, math, streaming, SQL-style operations, and type predicates.
</reusable-compact>

<reusable-compact filename="jq-manual.txt">
Normative jq language contract: generator semantics, ordering, filtering, variables, functions, reductions, assignments, builtins, regex, modules, I/O, streaming, and numeric behavior.
</reusable-compact>

AC_BROKEN: conformance-source-integrity

RESULT: FAILED

FILES CHANGED:
- tests/test_conformance_assets.py

SUMMARY:
The corpus validation passes: 550 cases and 13 exclusions. Local conformance asset tests pass. The source-integrity acceptance check is impossible as written because the supplied harness intentionally exposes absolute resolved paths, while the criterion compares them to relative paths.

BLOCKERS:
- The acceptance criterion must compare `.resolve()` paths, or the supplied harness contract must change.
- Full pytest collection also fails because `jq_interpreter` is not yet present; that belongs to a later implementation block.

FAILURE_SUMMARY: Source-integrity criterion compares absolute and relative paths.
FAILURE_DETAIL: `run_conformance.CORPUS` is `/.../sources/jq.test` because the immutable harness uses `Path(__file__).resolve()`, while the criterion expects `sources/jq.test`; modifying sources is forbidden.
