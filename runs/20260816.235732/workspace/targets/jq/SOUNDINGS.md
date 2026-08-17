# Soundings

Per-assertion acceptance board, one row per Blueprint Programmatic Acceptance check.
`drydock plan` projects every assertion as `— UNVERIFIED`; `drydock score ac` sets the
Status column from deterministic proof results. A rerun of `drydock plan` resets Status to
`— UNVERIFIED`; rescore to refresh.

| Status | Blueprint | AC Id | Text | Evidence | Verified At |
|---|---|---|---|---|---|
| ✓ PASS | ARCHITECTURE.md | architecture-contract | The architecture contract declares the executable boundary and required exit statuses. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | ARCHITECTURE.md | architecture-stack | The architecture records the approved standard-library implementation boundary. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | ARCHITECTURE.md | architecture-boundaries | The architecture assigns ownership for the interpreter's required technical boundaries. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-CLI-FOUNDATION.md | cli-identity | The executable accepts compact mode, reads JSON stdin, and emits a compact JSON result. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-CLI-FOUNDATION.md | cli-generator-output | The executable emits one compact line for each generated array element in source order. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-CLI-FOUNDATION.md | cli-compile-error | A syntactically invalid jq program returns the documented compile-error status. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-CLI-FOUNDATION.md | cli-runtime-error | A compiled program that raises at runtime returns the documented runtime-error status. |  | 2026-08-17T00:26:07+00:00 |
| ~ PREPASSED | FEATURE-FRONTEND-LEXER.md | lexer-literals | Lexically valid literal and format tokens are accepted through the executable boundary and preserve their supplied values. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-FRONTEND-LEXER.md | lexer-interpolation | String interpolation lexical boundaries are accepted and produce a value derived from supplied input. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-FRONTEND-LEXER.md | lexer-comments-and-operators | Comments and operator tokens are ignored or recognized without changing the evaluated result. |  | 2026-08-17T00:26:07+00:00 |
| ~ PREPASSED | FEATURE-FRONTEND-LEXER.md | lexer-invalid-escape | An invalid string escape is rejected as a compile error. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-FRONTEND-PARSER.md | parser-valid-programs | The parser accepts representative valid jq programs and the conformance runner reports success for the parser-owned corpus slice. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ~ PREPASSED | FEATURE-FRONTEND-PARSER.md | parser-invalid-programs | Invalid jq syntax is rejected with the documented compile-error status. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-FRONTEND-PARSER.md | parser-precedence | Parsed arithmetic precedence and grouping are accepted by the authoritative corpus. |  | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-EVAL-GENERATOR.md | generator-streams | The authoritative corpus passes representative generator, pipe, comma, iteration, and collection cases. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-EVAL-GENERATOR.md | generator-output-contract | A generator emits each produced value as compact JSON on its own output line. |  | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-EVAL-GENERATOR.md | generator-empty | The empty filter produces no output while a surrounding generator continues in order. |  | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-EVAL-VALUES.md | values-operators | The authoritative corpus passes arithmetic, comparison, boolean, string, array, and object value cases. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-EVAL-VALUES.md | values-indexing | Field access, iteration, negative indexes, and slices conform to jq behavior. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-EVAL-VALUES.md | values-runtime-error | A compiled program that raises a jq runtime error exits with status 5. |  | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-EVAL-CONTROL.md | control-flow | The authoritative corpus passes conditionals, alternatives, try/catch, and optional-expression cases. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-EVAL-CONTROL.md | reductions-and-loops | The authoritative corpus passes reductions, foreach, bounded generators, and recursive control constructs. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-EVAL-CONTROL.md | control-runtime-status | An uncaught control-expression runtime failure uses the documented runtime exit status. |  | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-LANG-BINDINGS.md | bindings-and-patterns | The authoritative corpus passes scalar bindings, array/object destructuring, and destructuring alternatives. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-LANG-BINDINGS.md | functions-and-closures | The authoritative corpus passes user-defined functions, recursion, closures, and generator-valued arguments. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-LANG-BINDINGS.md | binding-compile-errors | Undefined variables and malformed binding patterns are rejected at compile time. | assert undefined.returncode == 3 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-LANG-PATHS.md | paths-roundtrip | Path access and mutation produce the supplied value through the public executable. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-LANG-PATHS.md | paths-delete | Deleting a supplied path removes that path while retaining unrelated state. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-LANG-PATHS.md | assignment-operators | Plain, update, and arithmetic assignments update the selected field. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| — UNVERIFIED | FEATURE-LANG-PATHS.md | assignment-errors | Invalid path mutations report the documented runtime failure status. | malformed check: the assertion itself raised NameError (name 'json' is not defined. Did you forget to import 'json') in its own frame, before reaching the code under test. No implementation can satisfy it. Each check runs as its own script in its own process, so a name bound by another check is not in scope. Repair the assertion in the Blueprint specification. |  |
| ✗ FAIL | FEATURE-BUILTIN-STRUCTURAL.md | structural-collection | Collection builtins transform the supplied input and preserve its derived elements. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-BUILTIN-STRUCTURAL.md | structural-ordering | Sorting and uniqueness return the supplied values in jq order. |  | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-STRUCTURAL.md | structural-entries | Entry conversion round-trips the supplied object. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-STRUCTURAL.md | structural-containment | Containment and inversion agree for supplied nested values. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✓ PASS | FEATURE-BUILTIN-STRINGS.md | string-conversion | String conversion round-trips the supplied JSON value. |  | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-STRINGS.md | string-format | Base64 and URI formats encode and decode the supplied text. | assert actual[1] == source_value → IndexError: list index out of range | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-STRINGS.md | string-regex | Regular-expression matching identifies the supplied pattern. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-STRINGS.md | string-date | UTC date conversion round-trips the supplied ISO timestamp. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-RUNTIME.md | runtime-numeric | Numeric predicates and arithmetic return state-derived numeric results. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-RUNTIME.md | runtime-environment | The environment builtin returns an object containing a supplied inherited variable. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-RUNTIME.md | runtime-inputs | Inputs are consumed in order from the supplied newline-delimited JSON stream. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-BUILTIN-RUNTIME.md | runtime-streaming | Streaming conversion round-trips the supplied structure. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
| ✗ FAIL | FEATURE-CONFORMANCE.md | conformance-full | The completed interpreter passes the supplied full conformance suite. | assert result.returncode == 0 → AssertionError | 2026-08-17T00:26:07+00:00 |
