# FEATURE: Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Tokenizes jq source according to the supplied jq lexer specification. |
| Depends On  | ARCHITECTURE.md, FEATURE-Source-Staging.md |
| Provides    | jq lexer token stream |
| Consumes    | interpreter architecture, jq source text |

## Scope

The lexer converts jq source text into tokens carrying token kind, source spelling or decoded literal, and source location. It recognizes whitespace and comments, keywords, identifiers, field selectors, variable bindings, numeric literals, quoted strings, interpolation boundaries, format tokens, operators, delimiters, and invalid characters.

String escape validation must reject unsupported escapes while preserving valid JSON escapes. Comment handling must support line continuation with a trailing backslash. Delimiter state must detect mismatched closing characters.

## Token Categories

- Keywords: `as`, `def`, `if`, `then`, `else`, `elif`, `end`, `reduce`, `foreach`, `and`, `or`, `try`, `catch`, `label`, `break`, `import`, `include`, `module`.
- Literals: JSON-compatible numbers and quoted string fragments.
- Names: identifiers, dotted fields, and `$` bindings.
- Formats: `@text`, `@json`, `@html`, `@uri`, `@urid`, `@csv`, `@tsv`, `@sh`, `@base64`, and `@base64d`.
- Operators: arithmetic, comparison, assignment, defined-or, optional, recursive descent, comma, pipe, and delimiters.

## Programmatic Acceptance

=== AC lexer-tokenizes-basic-source ===
Intent: The lexer emits tokens for identity, a field, a number, and a pipe.
import jq_lexer

tokens = list(jq_lexer.tokenize(".foo | 42"))
kinds = [getattr(token, "kind", getattr(token, "type", None)) for token in tokens]
assert len(tokens) >= 4
assert all(kind is not None for kind in kinds)
=== END AC lexer-tokenizes-basic-source ===

=== AC lexer-recognizes-formats ===
Intent: The lexer recognizes format syntax as a format token rather than an invalid character.
import jq_lexer

tokens = list(jq_lexer.tokenize('@json'))
spellings = [getattr(token, "value", getattr(token, "text", None)) for token in tokens]
assert any(value in ("json", "@json") for value in spellings)
=== END AC lexer-recognizes-formats ===

=== AC lexer-recognizes-bindings ===
Intent: The lexer recognizes jq variable bindings.
import jq_lexer

tokens = list(jq_lexer.tokenize("$item"))
spellings = [getattr(token, "value", getattr(token, "text", None)) for token in tokens]
assert any(value in ("item", "$item") for value in spellings)
=== END AC lexer-recognizes-bindings ===

=== AC lexer-rejects-invalid-escape ===
Intent: Invalid string escapes are rejected lexically.
import jq_lexer

try:
    list(jq_lexer.tokenize(r'"u\vw"'))
except Exception:
    pass
else:
    raise AssertionError("invalid escape was accepted")
=== END AC lexer-rejects-invalid-escape ===

## User Acceptance

- None.

## Guardrails

- Keep token source locations available for compile diagnostics.
- Do not reinterpret strings, interpolation, comments, or escape sequences outside the supplied lexer specification.
