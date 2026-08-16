# FEATURE: Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Parses jq programs into executable abstract syntax trees using the supplied grammar and precedence rules. |
| Depends On  | ARCHITECTURE.md, FEATURE-Source-Staging.md, FEATURE-Lexer.md |
| Provides    | jq parser and AST |
| Consumes    | jq lexer token stream |

## Scope

The parser consumes lexer tokens and produces an AST suitable for generator evaluation. It implements jq precedence and associativity for pipes, commas, defined-or, assignments, Boolean operators, comparisons, arithmetic, indexing, optional access, and format expressions.

It supports literals, identity, fields, indexes, slices, iterators, arrays, objects, recursive descent, conditionals, try/catch, reductions, foreach, labels, breaks, bindings, destructuring, function definitions and calls, module declarations, imports, and includes.

Static validation rejects malformed syntax, undefined bindings, invalid break labels, invalid object keys, nonconstant module metadata, and nonconstant import paths.

## AST Boundary

Each parsed program exposes an executable AST object or equivalent immutable node graph. Nodes retain construct type and child expressions, while runtime state such as input values and lexical environments remains outside the AST.

## Programmatic Acceptance

=== AC parser-builds-ast ===
Intent: A valid jq program is parsed into a non-null AST.
import jq_parser

ast = jq_parser.parse(".foo | .bar")
assert ast is not None
=== END AC parser-builds-ast ===

=== AC parser-preserves-precedence ===
Intent: Arithmetic precedence is represented distinctly from addition.
import jq_parser

ast = jq_parser.parse("1 + 2 * 2")
rendered = repr(ast)
assert rendered
assert "1" in rendered and "2" in rendered
=== END AC parser-preserves-precedence ===

=== AC parser-supports-constructors ===
Intent: Array and object construction parse successfully.
import jq_parser

for program in ("[.foo, .bar]", "{foo: .bar}", "if . then 1 else 2 end"):
    assert jq_parser.parse(program) is not None
=== END AC parser-supports-constructors ===

=== AC parser-rejects-malformed-program ===
Intent: Unterminated syntax is rejected as a compile error by the parser boundary.
import jq_parser

try:
    jq_parser.parse("{")
except Exception:
    pass
else:
    raise AssertionError("malformed program was accepted")
=== END AC parser-rejects-malformed-program ===

## User Acceptance

- None.

## Guardrails

- Follow `sources/parser.y` for precedence, associativity, and construct coverage.
- Do not defer syntax errors to runtime.
- Do not load excluded module fixtures while validating module grammar.
