# ARCHITECTURE: jq

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Modular standard-library Python architecture for a standalone jq interpreter. |
| Depends On  | — |
| Provides    | interpreter architecture, executable boundary, generator evaluation model |
| Consumes    | — |

## Architecture

The implementation is a modular Python executable named `jq` at the application root. The process boundary parses `-c '<program>'`, reads JSON values from standard input, evaluates the parsed filter as an ordered generator, and serializes each produced value as one compact JSON value per output line.

The implementation is divided into:

- CLI and process boundary: argument validation, input framing, output serialization, diagnostics, and exit codes.
- Lexer and parser: jq tokenization, precedence, syntax validation, and AST construction.
- Value model: JSON values, numeric literals, NaN, infinities, immutable update helpers, and structural comparison.
- Evaluator: generator execution, lexical environments, function calls, backtracking, errors, labels, and reductions.
- Builtins: accessors, operators, collections, strings, regular expressions, dates, paths, assignments, I/O, and streaming.

Values are treated immutably at jq-language boundaries. Filters yield zero or more values; downstream filters execute once for every upstream value, preserving order and multiplicity.

### Module ownership

| Boundary | Owner | Responsibility |
|---|---|---|
| CLI and process execution | executable entry point | `-c`, stdin, stdout, stderr, exit status |
| Lexical analysis | lexer module | tokens, comments, literals, interpolation states |
| Syntax | parser module | AST and compile errors |
| Runtime values | value module | JSON-compatible values and numeric behavior |
| Evaluation | evaluator module | streams, environments, control flow, errors |
| Builtins | builtin modules | jq primitives and standard-library definitions |
| Paths and mutation | path module | path discovery and immutable updates |
| Conformance | staged `sources/` assets | corpus execution and scoring |

No system `jq`, third-party jq implementation, package installation, network access, or external runtime dependency is permitted.

## Technology Stack

- Python 3.11 or newer, using only the standard library.
- POSIX `sh` for the supplied scoring entry point.

## Programmatic Acceptance

=== AC architecture-boundary ===
Intent: The implementation exposes the declared executable boundary and remains runnable with the standard-library runtime.

from pathlib import Path
import os
import subprocess
import sys

executable = Path("jq")
assert executable.is_file()
assert os.access(executable, os.X_OK)

result = subprocess.run(
    [sys.executable, "-c", "import json, decimal, math, re, datetime, time"],
    capture_output=True,
    text=True,
)
assert result.returncode == 0
=== END AC architecture-boundary ===

=== AC architecture-conformance-start ===
Intent: The staged conformance assets can be imported and parsed from the declared architecture boundary.

import sys

sys.path.insert(0, "sources")
import run_conformance as harness

cases = harness.parse_corpus(harness.CORPUS.read_text(encoding="utf-8"))
excluded = harness.apply_exclusions(
    cases, harness.parse_exclusions(harness.EXCLUSIONS)
)
assert cases
assert excluded
=== END AC architecture-conformance-start ===

## User Acceptance

- None.

## Guardrails

- Do not shell out to a system `jq`.
- Do not use a third-party jq implementation or binding.
- Preserve generator ordering, multiplicity, backtracking, and immutable value semantics.
- Keep staged scoring assets unchanged.
