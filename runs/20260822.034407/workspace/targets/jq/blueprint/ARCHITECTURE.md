# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Architecture for a standalone Python standard-library jq interpreter. |
| Depends On  | COMPASS.md, TECHNOLOGY_STACK.md |
| Provides    | interpreter architecture, CLI boundary, evaluator boundaries |
| Consumes    | — |

## System Boundaries

The interpreter is a standalone executable named `jq`. It accepts `-c '<program>'`, reads JSON values from standard input, evaluates the jq program as an ordered generator, and emits compact JSON values one per line.

The implementation is organized into:

- lexical analysis and source locations;
- parsing and AST construction;
- generator evaluation and runtime control flow;
- immutable JSON values, paths, assignments, and builtins;
- CLI argument, input, output, and exit-code handling.

The supplied files under `sources/` are read-only conformance and language references. They are never modified by the implementation.

## Evaluation Model

Every filter evaluates against one input value and produces an ordered stream of zero or more values. Pipelines feed each output into the next filter, while comma expressions concatenate streams. Evaluation must preserve multiplicity, cartesian behavior, backtracking, and values emitted before a runtime error.

Compile failures return exit `3`. Runtime failures return exit `5`. Successful completion returns exit `0`.

## Technology Stack

Python 3.11 or newer and its standard library are used for the interpreter. POSIX `sh` is used only by the supplied scoring entry point. No third-party runtime dependency, network access, package installation, system jq process, or jq binding is permitted.

Numbers use Python floating-point arithmetic while retaining original literal spellings where required for serialization. `have_decnum` reports false.

## Module Ownership

| Boundary | Owner | Responsibility |
|---|---|---|
| Lexer | frontend lexer module | Tokens, strings, comments, locations, invalid characters |
| Parser | frontend parser module | Grammar, precedence, AST, compile diagnostics |
| Evaluator | core evaluator module | Streams, filters, environments, runtime control |
| Paths and updates | path subsystem | Discovery, access, mutation, deletion, assignments |
| Builtins | builtin subsystem | Standard jq functions and formats |
| CLI | executable entry point | Arguments, JSON input/output, exit status |

## Programmatic Acceptance

=== AC architecture-contract ===
Intent: The architecture contract exposes the required interpreter boundary and exit-code constants.

from pathlib import Path

compass = Path("COMPASS.md").read_text(encoding="utf-8")
assert "standalone interpreter" in compass
assert "exit `3`" in compass
assert "exit `5`" in compass
=== END AC architecture-contract ===

=== AC architecture-assets ===
Intent: The architecture preserves the complete, mutually consistent, read-only language and conformance asset boundary.

import sys
from pathlib import Path

sys.path.insert(0, "sources")
import run_conformance as harness

required = [
    Path("sources/jq-manual.txt"),
    Path("sources/jq.test"),
    Path("sources/lexer.l"),
    Path("sources/parser.y"),
]
for asset in required:
    assert asset.read_text(encoding="utf-8")

cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
excluded = harness.apply_exclusions(
    cases, harness.parse_exclusions(harness.EXCLUSIONS)
)
assert len(cases) == 550
assert len(excluded) == 13
=== END AC architecture-assets ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library functionality.
- Do not shell out to a system jq executable.
- Do not modify files under `sources/`.
- Preserve generator ordering, multiplicity, backtracking, and partial runtime output.
