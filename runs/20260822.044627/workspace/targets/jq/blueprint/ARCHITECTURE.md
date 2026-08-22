# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Standard-library Python architecture for a standalone jq interpreter. |
| Depends On  | COMPASS.md, TECHNOLOGY_STACK.md |
| Provides    | jq interpreter architecture, executable boundary, parser, evaluator, runtime |
| Consumes    | — |

## System Overview

The application is an executable named `jq` at the application root. It accepts `-c '<program>'`, reads JSON values from standard input, evaluates the jq program as an ordered generator, and writes compact JSON values one per line.

The implementation is composed of:

- CLI and process boundary.
- Lexer and recursive-descent or precedence parser.
- AST and compiled filter representation.
- Generator evaluator with lexical environments.
- jq value, numeric, accessor, assignment, builtin, and runtime-error layers.
- Streaming JSON input and output serialization.

All runtime code uses Python 3.11+ standard-library modules only. The implementation must not invoke, import, or bind to another jq implementation.

## Module Boundaries

| Module | Responsibility |
|---|---|
| `jq` | Executable entry point and command-line validation |
| `jq_runtime.py` or equivalent | Input stream, evaluation context, errors, output serialization |
| `jq_lexer.py` or equivalent | Tokens, comments, literals, strings, interpolation markers |
| `jq_parser.py` or equivalent | AST construction, precedence, declarations, syntax validation |
| `jq_eval.py` or equivalent | Ordered generator evaluation, environments, functions, control flow |
| `jq_values.py` or equivalent | jq values, numeric handling, comparison, access, mutation |
| `jq_builtins.py` or equivalent | Builtin filters and standard-library implementations |

The concrete module filenames may vary, but responsibilities remain isolated at these boundaries.

## Evaluation Model

Every filter receives one input and yields an ordered stream of zero or more outputs. Pipes evaluate the right-hand filter once per left-hand output. Commas concatenate streams. Filter arguments remain generators, while value arguments are evaluated and bound as values. Runtime errors propagate through the stream and preserve outputs already emitted.

Assignments operate immutably over paths and return replacement values rather than mutating shared input objects.

## Process Contract

- Compile success and complete execution exit `0`.
- Compile or static failure exit `3`.
- Runtime failure exit `5`.
- Diagnostics are written to standard error.
- Output is compact JSON, one generated value per line.
- Partial output before a runtime failure is preserved.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Interpreter, parser, evaluator, builtins, CLI |
| POSIX sh | Supplied conformance entry point |

Only Python standard-library facilities are permitted at runtime.

## Source and Test Asset Boundary

The supplied files under `sources/` are immutable inputs. The implementation reads them when required but does not modify them. The conformance runner is external to the interpreter and remains the authority for corpus comparison.

## Programmatic Acceptance

=== AC architecture-runtime ===
Intent: The declared runtime stack is available using only Python standard-library modules.

import importlib

modules = ["json", "decimal", "math", "re", "datetime", "time", "base64", "unicodedata", "itertools", "functools", "dataclasses", "argparse", "sys"]
for module in modules:
    assert importlib.import_module(module) is not None
=== END AC architecture-runtime ===

=== AC architecture-contract ===
Intent: The staged conformance runner exposes the process exit-code contract required by the architecture.

import sys
sys.path.insert(0, "sources")
import run_conformance as harness

assert harness.EXIT_COMPILE_ERROR == 3
assert harness.EXIT_RUNTIME_ERROR == 5
assert harness.PASS == "pass"
assert harness.FAIL == "fail"
assert harness.ERROR == "error"
=== END AC architecture-contract ===

## User Acceptance

- None.

## Guardrails

- Do not shell out to a system `jq`.
- Do not use a third-party jq implementation or binding.
- Do not modify files under `sources/`.
- Preserve generator ordering, multiplicity, backtracking, and partial runtime output.
