# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-08-22
- resulting state: closed/verified
- story points (combined assembled cost): 10201
- execution id: 20260822.180626.371Z-122a84e1

## Stories built
- Define the standalone interpreter architecture and module boundaries. (architecture) [story]

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- compass: COMPASS.md (SP 3420)
- implements: ARCHITECTURE.md (SP 1018)
- stack: common.md (SP 1807)
- stack: python.md (SP 3892)

## Build directory changes
- jq
- jq_interpreter/__init__.py
- jq_interpreter/ast.py
- jq_interpreter/builtins.py
- jq_interpreter/cli.py
- jq_interpreter/diagnostics.py
- jq_interpreter/errors.py
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
- jq_interpreter/lexer.py
- jq_interpreter/parser.py
- jq_interpreter/paths.py
- jq_interpreter/runtime.py
- tests/test_architecture.py

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
- Executable: `./jq -c '<program>'`; compact JSON lines on stdout.
- Exit codes: `0` success, `3` compile failure, `5` runtime failure; diagnostics on stderr.
- Standard-library Python only; no external jq, dependencies, networking, or persistence.
- Modules: CLI, lexer, parser/AST, evaluator streams, runtime values, builtins, paths/assignment, diagnostics.
- Preserve generator ordering, multiplicity, backtracking, immutable transformations, and partial output.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- jq
- jq_interpreter/__init__.py
- jq_interpreter/ast.py
- jq_interpreter/builtins.py
- jq_interpreter/cli.py
- jq_interpreter/diagnostics.py
- jq_interpreter/errors.py
- jq_interpreter/evaluator.py
- jq_interpreter/interpreter.py
- jq_interpreter/lexer.py
- jq_interpreter/parser.py
- jq_interpreter/paths.py
- jq_interpreter/runtime.py
- tests/test_architecture.py

SUMMARY:
Established the standalone Python interpreter architecture, executable boundary, module contracts, exit-code handling, streaming identity behavior, immutable path reads, and foundational tests. All 5 tests pass. No staged conformance suite was run because this architecture specification declares no programmatic acceptance.

BLOCKERS:
- None
