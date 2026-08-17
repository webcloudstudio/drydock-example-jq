# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Architecture for a standalone Python standard-library jq interpreter. |
| Depends On  | COMPASS.md, TECHNOLOGY_STACK.md |
| Provides    | interpreter module boundaries, CLI process contract |
| Consumes    | — |

## Intent

The application is a standalone executable named `jq` that evaluates jq filters over JSON input. It is implemented entirely in Python using the standard library and must not invoke another jq implementation.

## System Boundaries

The root executable owns argument validation, stdin decoding, output serialization, diagnostics, and process exit codes. Interpreter modules own lexical analysis, parsing, AST construction, generator evaluation, bindings, paths, assignments, control flow, and builtins.

Imported corpus and specification assets remain under `sources/` and are read-only build context. The application must not modify, filter, or reinterpret them.

## Module Ownership

| Module | Responsibility |
|---|---|
| `jq` | Executable process boundary and `-c` interface |
| Lexer | Tokens, literals, strings, interpolation, comments, operators, and source locations |
| Parser | jq grammar, precedence, syntax validation, and AST construction |
| Runtime | Generator evaluation, environments, errors, labels, and stream behavior |
| Values | jq-compatible JSON values, ordering, arithmetic, indexing, and serialization |
| Paths | Path discovery, access, mutation, deletion, and assignment |
| Builtins | Standard jq functions implemented with Python standard-library facilities |

Generators are the primary runtime abstraction. Every filter receives one input and may yield zero, one, or many outputs. Pipes evaluate the right-hand filter once for every left-hand output; commas preserve left-to-right order and multiplicity.

## Process Contract

The executable accepts `./jq -c '<program>'`, reads JSON values from stdin, writes one compact JSON value per output line to stdout, and sends diagnostics to stderr.

Exit status `0` means successful compilation and execution. Exit status `3` means compilation or static failure. Exit status `5` means a runtime failure after compilation. Outputs produced before a runtime failure remain valid.

## Technology Stack

- Python 3.11 or newer, standard library only, for the interpreter and acceptance tooling.
- POSIX `sh` for the supplied acceptance entry point.

## Guardrails

- Do not shell out to, wrap, import, or bind any third-party or system jq implementation.
- Do not use network access or install packages.
- Preserve generator backtracking, output order, and multiplicity.
- Keep diagnostics on stderr and JSON results on stdout.
- Keep supplied scoring assets unchanged.

## Programmatic Acceptance

=== AC architecture-contract ===
Intent: The architecture contract declares the executable boundary and required exit statuses.

from pathlib import Path

text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
required = [
    "standalone executable named `jq`",
    "Exit status `0`",
    "Exit status `3`",
    "Exit status `5`",
    "Generators are the primary runtime abstraction",
]
for token in required:
    assert token in text
=== END AC architecture-contract ===

=== AC architecture-stack ===
Intent: The architecture records the approved standard-library implementation boundary.

from pathlib import Path

text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
assert "Python 3.11 or newer, standard library only" in text
assert "POSIX `sh`" in text
assert "third-party or system jq implementation" in text
=== END AC architecture-stack ===

=== AC architecture-boundaries ===
Intent: The architecture assigns ownership for the interpreter's required technical boundaries.

from pathlib import Path

text = Path("ARCHITECTURE.md").read_text(encoding="utf-8")
modules = ["Lexer", "Parser", "Runtime", "Values", "Paths", "Builtins"]
for module in modules:
    assert f"| {module} |" in text
=== END AC architecture-boundaries ===

## User Acceptance

- None.

## Guardrails

- None.
