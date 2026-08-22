# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines the modular standard-library Python architecture for the standalone jq interpreter. |
| Depends On  | — |
| Provides    | interpreter module boundaries, executable boundary |
| Consumes    | — |

## Intent

The interpreter is a standalone executable named `jq`. It accepts `./jq -c '<program>'`, reads JSON values from standard input, evaluates jq filters as ordered generators, and writes compact JSON values to standard output.

## Technology Stack

- Python 3.11 or newer, using only the standard library.
- POSIX `sh` for the supplied scoring entry point.
- No third-party runtime dependency, network access, package installation, jq binding, or shell-out to another jq executable.

## Modules and Boundaries

| Boundary | Responsibility |
|---|---|
| `jq` executable | Parse command-line arguments, read standard input, invoke the interpreter, serialize outputs, and map failures to exit codes. |
| Lexer | Tokenize jq literals, identifiers, fields, bindings, keywords, operators, delimiters, comments, formats, and interpolated strings. |
| Parser | Produce an AST or equivalent intermediate representation, enforce precedence and static validity, and reject invalid programs. |
| Evaluator | Execute filters as ordered streams, preserving multiplicity, backtracking, Cartesian products, and partial output. |
| Runtime values | Represent JSON values, literal-aware numbers, NaN, infinities, arrays, objects, and immutable transformations. |
| Builtins | Implement jq primitives and standard-library filters over the evaluator's stream model. |
| Paths and assignment | Discover paths and apply immutable reads, writes, updates, and deletions. |
| Diagnostics | Keep compile failures, runtime failures, stderr output, and successful completion distinct. |

The executable boundary must not depend on a system jq command or an external implementation. Parser and evaluator interfaces remain internal to the Python implementation; the only public interface is the executable process contract.

## Runtime Contracts

- Compile failure exits `3`.
- Runtime failure exits `5`.
- Successful completion exits `0`.
- Diagnostics are written to stderr.
- Each produced value is serialized as one compact JSON value per line.
- Values emitted before a runtime failure remain on stdout.
- Generator ordering and multiplicity are observable and must be preserved.

## Module Ownership

| Concern | Owning boundary | Allowed dependencies |
|---|---|---|
| Process and CLI | executable boundary | parser, evaluator, serializer, diagnostics |
| Syntax | lexer and parser | standard-library text handling, AST definitions |
| Evaluation | evaluator | AST, runtime values, builtins, paths |
| Persistence/configuration | none | jq has no persistent store or application configuration |
| File store | none | module loading is excluded by the fixed interface |
| External services | none | network and external runtimes are forbidden |

## Numeric Decision

Use a literal-aware standard-library numeric model. Preserve source/input number spelling where jq semantics require it, perform arithmetic using standard-library numeric operations, and support special floating-point values without adding dependencies.

## Source Role Context

The implementation uses the staged lexer, parser, manual, builtin reference, corpus, and conformance harness as read-only context. The staged harness remains external to the implementation and is never modified.

## Programmatic Acceptance

- None. This specification defines architecture and boundaries; executable behavior is verified by the implementing feature specifications and the terminal conformance story.

## User Acceptance

- None.

## Guardrails

- Do not add third-party dependencies.
- Do not modify files under `sources/`.
- Do not shell out to a system jq executable.
- Do not collapse generator streams into single return values.
- Do not conflate compile exit `3` with runtime exit `5`.
