# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260820 V1 |
| Description | Defines the standalone jq interpreter modules and execution boundaries. |
| Depends On  | METADATA.md |
| Provides    | lexer boundary, parser boundary, generator evaluator, builtin runtime, executable boundary |
| Consumes    | sources/lexer.l, sources/parser.y, sources/jq-manual.txt, sources/builtin.jq |

## System Shape

The interpreter is a standalone command-line application. The root executable accepts `-c PROGRAM`, parses JSON input values from standard input, evaluates the program as an ordered jq generator, and emits compact JSON output values one per line.

## Modules and Boundaries

| Module | Responsibility |
|--------|----------------|
| Lexer | Tokenizes identifiers, fields, bindings, literals, strings, interpolation, formats, comments, operators, and delimiters. |
| Parser | Builds an AST with jq precedence, associativity, bindings, definitions, patterns, modules, assignments, and control forms. |
| Evaluator | Executes AST filters against immutable values as ordered zero-, one-, or many-value streams. |
| Paths and assignment | Discovers paths and applies immutable updates, replacement, deletion, and arithmetic assignments. |
| Control and bindings | Implements conditionals, labels, reductions, foreach, variables, destructuring, functions, and recursion. |
| Builtins | Provides structural, string, regex, numeric, date, streaming, SQL-style, environment, and I/O filters. |
| Executable wrapper | Validates arguments, reads newline-delimited JSON, emits compact JSON, and maps compile/runtime failures to exit codes 3 and 5. |

## Evaluation Model

Filters are represented as lazy Python generators. Every filter receives an input value and may yield zero, one, or many outputs. Pipe composition evaluates the right-hand filter once for each left-hand output. Comma composition preserves left-to-right ordering. Generator consumers such as reduce, foreach, limit, first, and short-circuiting alternatives must preserve backtracking behavior.

## Values and Numbers

JSON values use standard-library representations. Numeric literals retain source text where output preservation is required, while arithmetic and numeric operations use native floating-point behavior. `have_decnum` returns the supported non-decimal branch.

## Immutability and Paths

Values are treated as immutable. Path expressions identify locations as arrays of string keys and integer indices. Assignment creates replacement structures rather than mutating values visible elsewhere. Path creation, deletion, array growth, invalid-path handling, and depth limits are centralized in the path runtime.

## Error and Exit Boundaries

Compilation failures are reported to stderr and return exit code 3. Runtime failures return exit code 5 after preserving values already emitted. Diagnostics are not part of conformance comparison.

## Technology Stack

- Python 3.11 or newer, using only the standard library for runtime implementation.
- POSIX sh for the supplied conformance entry point.

## Module Ownership

| Boundary | Owner | Allowed dependencies |
|----------|-------|----------------------|
| Lexer and parser | frontend modules | source text, AST definitions |
| Evaluation and values | runtime evaluator | AST, immutable values, generator protocol |
| Paths and assignment | path runtime | evaluator path protocol, immutable values |
| Builtins | builtin runtime | evaluator protocol and standard library |
| Configuration and environment | executable/runtime boundary | Python process environment and stdin |
| Conformance assets | delivery integration | staged `sources/` files only |

## Programmatic Acceptance

=== AC architecture-boundaries ===
Intent: The architecture records every required interpreter boundary and the generator evaluation model.

from pathlib import Path

text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
required = [
    "Lexer", "Parser", "Evaluator", "Paths and assignment",
    "Control and bindings", "Builtins", "Executable wrapper",
    "lazy Python generators", "exit code 3", "exit code 5",
]
for item in required:
    assert item in text
=== END AC ===

=== AC architecture-stack ===
Intent: The architecture records the approved standard-library-only implementation constraint.

from pathlib import Path

text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
assert "Python 3.11" in text
assert "standard library" in text
assert "POSIX sh" in text
=== END AC ===

## User Acceptance

- None.

## Guardrails

- Do not shell out to a system jq executable.
- Do not use a third-party jq implementation or binding.
- Preserve generator ordering, multiplicity, backtracking, and partial runtime output.
- Do not modify files under `sources/`.
