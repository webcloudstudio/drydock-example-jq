# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Defines the standalone Python architecture and module boundaries for the jq interpreter. |
| Depends On  | — |
| Provides    | interpreter module boundaries, jq executable contract |
| Consumes    | — |

## Intent

The application is a standalone jq-language interpreter implemented with Python's standard library. It exposes an executable named `jq`, accepts `-c '<program>'`, reads a stream of JSON texts from standard input, evaluates each program as an ordered generator, and writes compact JSON values to standard output.

## Module Boundaries

| Module area | Responsibility |
|---|---|
| CLI | Argument validation, stdin JSON-text framing, output serialization, and process exit status |
| Lexer | jq tokens, comments, strings, interpolation, formats, operators, delimiters, and source locations |
| Parser/compiler | Precedence, AST construction, static validation, function definitions, bindings, and control syntax |
| Evaluator | Lazy ordered streams, generator multiplicity, backtracking, environments, errors, and control flow |
| Data model | JSON values, numeric representation, equality, ordering, indexing, slicing, and containment |
| Paths and mutation | Path discovery, immutable replacement, deletion, and assignment operators |
| Builtins | Collection, string, regular-expression, formatting, date, math, I/O, streaming, and SQL-style filters |
| Verification | Focused project tests and the supplied conformance harness |

The evaluator must represent filters as lazy Python iterators or equivalent resumable streams. A filter may produce zero, one, or many values, and downstream filters run once for every upstream value. Runtime errors must preserve values already emitted.

## Data and Error Model

Use a literal-preserving hybrid numeric representation: retain source spelling where jq preserves an untouched numeric literal, while using standard-library numeric operations for arithmetic and comparisons. JSON values remain immutable from the evaluator's perspective; assignments produce replacement trees.

Compilation errors are distinct from runtime errors. The CLI returns `3` for syntax or static failures and `5` for runtime failures. Diagnostics are written only to standard error.

## Technology Stack

| Technology | Application |
|---|---|
| Python 3.11 or newer | Lexer, parser, evaluator, data model, builtins, CLI, and focused tests |
| POSIX sh | Supplied conformance entry point |

The implementation uses only Python standard-library modules and never invokes a system jq executable, third-party jq implementation, package installer, or network service.

## Persistence and External Boundaries

The interpreter has no persistent store, database, authentication boundary, or external service. Runtime input and output are confined to standard input, standard output, and standard error. The `input` and `inputs` builtins consume the CLI's remaining JSON input stream.

## Programmatic Acceptance

=== AC architecture-stream-contract ===
Intent: The completed executable accepts the declared compact-filter interface and returns a valid JSON value derived from supplied input.
import json
import subprocess

payload = {"architecture": ["stream", "generator"]}
source = json.dumps(payload)
result = subprocess.run(
    ["./jq", "-c", "."],
    input=source + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == payload
=== END AC architecture-stream-contract ===

=== AC architecture-generator-order ===
Intent: The evaluator preserves ordered generator multiplicity for comma expressions.
import json
import subprocess

input_value = None
expected = [1, 1, 2]
result = subprocess.run(
    ["./jq", "-c", "1, 1, 2"],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == expected
=== END AC architecture-generator-order ===

=== AC architecture-runtime-status ===
Intent: Runtime failures use the documented runtime exit status while keeping diagnostics off standard output.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "error"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
assert result.stdout == ""
=== END AC architecture-runtime-status ===

## User Acceptance

- None.

## Guardrails

- Do not shell out to a system jq executable.
- Do not use third-party jq implementations or bindings.
- Preserve supplied source assets and the acceptance harness.
- Preserve generator ordering, multiplicity, backtracking, and partial output.
- Keep compile failures distinct from runtime failures using exit codes 3 and 5.
