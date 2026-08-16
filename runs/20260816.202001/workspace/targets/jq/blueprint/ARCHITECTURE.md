# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines the standalone Python standard-library architecture and executable boundaries for the jq interpreter. |
| Depends On  | — |
| Provides    | jq interpreter architecture, executable boundary |
| Consumes    | stdin JSON stream, jq filter source, standard-library runtime |

## Intent

Build a standalone jq 1.8.2-compatible interpreter in Python. The executable reads filter programs supplied through `-c`, evaluates JSON inputs as ordered generator streams, and writes compact JSON results one per line.

## Architecture

| Module | Ownership |
|---|---|
| `jq_lexer.py` | Source tokenization, comments, literals, strings, interpolation, identifiers, bindings, operators, and delimiters. |
| `jq_parser.py` | Precedence-aware parsing, AST construction, static validation, function and module declarations. |
| `jq_runtime.py` | Generator evaluation, values, environments, errors, paths, assignments, control flow, and builtin dispatch. |
| `jq_builtins.py` | Standard-library implementations of jq builtin filters. |
| `jq_cli.py` | `-c` argument handling, JSON input decoding, result serialization, stderr diagnostics, and exit codes. |
| `jq` | Executable wrapper delegating to the Python CLI. |

Filters are represented as AST nodes evaluated against an input value and lexical environment. Evaluation yields an ordered stream, permitting zero, one, or many results. Pipelines evaluate their right side once per left-side result; comma expressions concatenate streams in source order.

## Runtime Contracts

- Compile failures produce exit status `3` and diagnostics only on stderr.
- Runtime failures produce exit status `5`; values emitted before the failure remain on stdout.
- Successful completion produces exit status `0`.
- Result values are compact JSON texts, one per line.
- No third-party package, network access, system jq binary, or subprocess jq implementation is permitted.
- Numeric values use Python floating-point behavior with literal metadata retained where required by the corpus.
- JSON object key order is not semantically significant, while generator result order is significant.

## Module Boundaries

The lexer exposes tokens and source locations to the parser. The parser exposes an executable AST to the runtime. The runtime owns evaluation and calls builtin implementations through a registry. The CLI is the only layer that reads process arguments or serializes result streams.

No layer shells out to another interpreter. Diagnostics are separated from result output at the CLI boundary.

## Technology Stack

- Python 3.11 or newer, standard library only.
- POSIX `sh` for the supplied scoring entry point.

## Programmatic Acceptance

=== AC architecture-lexer-contract ===
Intent: The lexer module exposes a callable tokenization boundary.
import jq_lexer

assert callable(jq_lexer.tokenize)
=== END AC architecture-lexer-contract ===

=== AC architecture-parser-contract ===
Intent: The parser module exposes a callable AST construction boundary.
import jq_parser

assert callable(jq_parser.parse)
=== END AC architecture-parser-contract ===

=== AC architecture-runtime-contract ===
Intent: The runtime module exposes generator evaluation.
import jq_runtime
import inspect

assert callable(jq_runtime.evaluate)
assert inspect.isgeneratorfunction(jq_runtime.evaluate)
=== END AC architecture-runtime-contract ===

=== AC architecture-no-third-party-runtime ===
Intent: The architecture remains executable with the Python standard library.
import ast
from pathlib import Path

source = Path("jq_runtime.py").read_text(encoding="utf-8")
tree = ast.parse(source)
imports = {
    node.names[0].name.split(".")[0]
    for node in ast.walk(tree)
    if isinstance(node, ast.Import) and node.names
}
for node in ast.walk(tree):
    if isinstance(node, ast.ImportFrom) and node.module:
        imports.add(node.module.split(".")[0])

stdlib = {"argparse", "ast", "base64", "copy", "datetime", "decimal", "functools",
          "itertools", "json", "math", "operator", "os", "re", "sys", "time",
          "types", " unicodedata".strip()}
assert imports <= stdlib
=== END AC architecture-no-third-party-runtime ===

## User Acceptance

- None.

## Guardrails

- Do not modify supplied scoring assets.
- Do not shell out to jq or require network access.
- Preserve ordered generator semantics and partial output before runtime failure.
