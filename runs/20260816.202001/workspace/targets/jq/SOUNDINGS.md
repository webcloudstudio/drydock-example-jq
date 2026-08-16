# Soundings

Per-assertion acceptance board, one row per Blueprint Programmatic Acceptance check.
`drydock plan` projects every assertion as `— UNVERIFIED`; `drydock score ac` sets the
Status column from deterministic proof results. A rerun of `drydock plan` resets Status to
`— UNVERIFIED`; rescore to refresh.

| Status | Blueprint | AC Id | Text | Evidence | Verified At |
|---|---|---|---|---|---|
| ✓ PASS | ARCHITECTURE.md | architecture-lexer-contract | The lexer module exposes a callable tokenization boundary. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | ARCHITECTURE.md | architecture-parser-contract | The parser module exposes a callable AST construction boundary. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | ARCHITECTURE.md | architecture-runtime-contract | The runtime module exposes generator evaluation. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | ARCHITECTURE.md | architecture-no-third-party-runtime | The architecture remains executable with the Python standard library. | assert imports <= stdlib → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Source-Staging.md | staging-complete | Every declared source asset is staged at its required build-relative path. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Source-Staging.md | staging-nonempty | Every staged source asset contains imported content. |  | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Source-Staging.md | staging-harness-executable | The supplied scoring entry point is executable by POSIX sh. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Lexer.md | lexer-tokenizes-basic-source | The lexer emits tokens for identity, a field, a number, and a pipe. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Lexer.md | lexer-recognizes-formats | The lexer recognizes format syntax as a format token rather than an invalid character. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Lexer.md | lexer-recognizes-bindings | The lexer recognizes jq variable bindings. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Lexer.md | lexer-rejects-invalid-escape | Invalid string escapes are rejected lexically. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Parser.md | parser-builds-ast | A valid jq program is parsed into a non-null AST. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Parser.md | parser-preserves-precedence | Arithmetic precedence is represented distinctly from addition. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Parser.md | parser-supports-constructors | Array and object construction parse successfully. |  | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Parser.md | parser-rejects-malformed-program | Unterminated syntax is rejected as a compile error by the parser boundary. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Compile-Contract.md | compile-api-separates-errors | The compiler exposes a compile boundary that distinguishes invalid source. |  | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Compile-Contract.md | compile-valid-source-reaches-ast | Valid source crosses compilation and produces an AST. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Compile-Contract.md | compile-cli-status-contract | The executable reports a malformed program with the declared compile status. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ~ PREPASSED | FEATURE-Compile-Contract.md | compile-diagnostics-use-stderr | Compile diagnostics are separated from result output. | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Formats.md | formats-suite | The format implementation passes its authoritative conformance slice. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Formats.md | formats-interface | The executable accepts a format program and completes successfully. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Formats.md | formats-roundtrip | Base64 encoding followed by decoding preserves supplied input. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Generator-Runtime.md | generator-suite | The generator runtime passes its authoritative conformance slice. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Generator-Runtime.md | generator-order | Comma and pipeline preserve ordered stream results. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Generator-Runtime.md | generator-empty | The empty filter produces no output and succeeds. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Core-Values.md | core-values-suite | Core value behavior passes its authoritative conformance slice. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Core-Values.md | core-values-indexing | Field access and iteration return the corresponding supplied values. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Core-Values.md | core-values-construction | Array construction collects all outputs from its generator expression. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Operators.md | operators-suite | Operator behavior passes its authoritative conformance slice. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Operators.md | operators-arithmetic | Arithmetic applies the declared operation to supplied numeric input. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Operators.md | operators-definedor | Defined-or selects the fallback for a null input. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Errors-Control.md | errors-control-suite | Error and control behavior passes its authoritative conformance slice. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Errors-Control.md | errors-runtime-status | An uncaught runtime failure exits with the documented runtime status. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Errors-Control.md | errors-try-catch | try/catch converts a supplied runtime failure into a value. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Errors-Control.md | errors-partial-output | Values emitted before an uncaught runtime failure remain observable. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Functions-Bindings.md | functions-bindings-suite | The supplied conformance corpus passes the functions, closures, bindings, and destructuring cases owned by this feature. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Functions-Bindings.md | functions-generator-arguments | Filter and value parameters preserve jq's distinct evaluation behavior. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Functions-Bindings.md | bindings-and-patterns | Lexical bindings and nested destructuring produce the supplied bound values. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Functions-Bindings.md | undefined-binding-compile-error | Referencing an undefined variable produces the documented compile exit status. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Reductions.md | reductions-suite | The supplied conformance corpus passes the reduction and recursive-control cases owned by this feature. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Reductions.md | reduce-and-foreach | Reduction and foreach preserve accumulator order and extraction behavior. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Reductions.md | range-limit-skip | Range generation, limiting, and skipping preserve ordered stream values. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Reductions.md | negative-count-runtime-error | Unsupported negative limit counts produce the documented runtime exit status. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Structural-Builtins.md | structural-builtins-suite | The supplied conformance corpus passes the collection, structural, path, and transformation cases owned by this feature. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Structural-Builtins.md | structural-round-trip | Entry conversion and structural transformation preserve object contents and keys. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Structural-Builtins.md | structural-ordering | Sorting and uniqueness use jq's structural ordering and remove duplicates. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Structural-Builtins.md | path-update | Path utilities can read, update, and delete nested values. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Regex-Builtins.md | regex-builtins-suite | The supplied conformance corpus passes the string and regular-expression cases owned by this feature. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Regex-Builtins.md | string-transformations | String splitting, joining, trimming, and case conversion preserve supplied input semantics. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Regex-Builtins.md | regex-match-capture | Matching and named capture extraction produce structured match data. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Regex-Builtins.md | regex-invalid-input | Applying a string builtin to a non-string input produces the documented runtime exit status. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Numeric-Builtins.md | numeric-builtins-suite | The supplied conformance corpus passes numeric, math, special-number, and literal-number cases owned by this feature. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Numeric-Builtins.md | numeric-conversion | Numeric conversion accepts numbers and valid numeric strings. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Numeric-Builtins.md | numeric-math | Standard mathematical filters produce numeric results. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Numeric-Builtins.md | numeric-predicates | Numeric predicates distinguish finite, infinite, and NaN values. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Numeric-Builtins.md | invalid-number-conversion | Invalid numeric conversion produces the documented runtime exit status. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Date-JSON-Encoding.md | date-json-roundtrip | JSON conversion preserves supplied values through a public jq round trip. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Date-JSON-Encoding.md | date-utc-roundtrip | ISO date conversion reverses a supplied UTC timestamp. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Date-JSON-Encoding.md | environment-read | Environment access returns a value supplied by the process environment. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-IO-Streaming.md | inputs-order | inputs emits all supplied JSON documents in their original order. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-IO-Streaming.md | stream-roundtrip | tostream followed by fromstream preserves a supplied composite value. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-IO-Streaming.md | stderr-isolation | stderr produces no stdout result while the process completes successfully. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-SQL-Introspection.md | index-build | INDEX creates lookup entries for every supplied row. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-SQL-Introspection.md | membership-stream | IN returns membership results for supplied generated values. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-SQL-Introspection.md | module-compile-rejection | Invalid module metadata is rejected with the compile-error status. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Executable.md | executable-stream | The executable accepts -c and emits one compact result per generated value. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Executable.md | executable-compile-status | A syntactically invalid program exits with status 3. |  | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Executable.md | executable-runtime-status | An uncaught runtime failure exits with status 5 after compilation succeeds. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Focused-Verification.md | focused-lexer-parser | The executable passes bounded lexer and parser conformance selections. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Focused-Verification.md | focused-runtime-builtins | The executable passes bounded runtime and builtin conformance selections. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
| ✓ PASS | FEATURE-Focused-Verification.md | focused-assets-unchanged | The focused verification command completes using the supplied harness and candidate executable. |  | 2026-08-16T20:58:27+00:00 |
| ✗ FAIL | FEATURE-Full-Conformance.md | full-conformance | The completed interpreter passes the supplied full jq conformance suite. | assert result.returncode == 0 → AssertionError | 2026-08-16T20:58:27+00:00 |
