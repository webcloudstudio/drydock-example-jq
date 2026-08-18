# FEATURE: Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Proves the completed jq interpreter against the supplied jq 1.8.2 conformance corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-Conformance-Staging.md, FEATURE-Executable-Contract.md, FEATURE-Lexer.md, FEATURE-Parser.md, FEATURE-Compile-Diagnostics.md, FEATURE-Generator-Core.md, FEATURE-Primitive-Filters.md, FEATURE-Arithmetic-Comparison.md, FEATURE-Conditionals.md, FEATURE-Runtime-Errors.md, FEATURE-Functions.md, FEATURE-Bindings.md, FEATURE-Reducers.md, FEATURE-Path-Discovery.md, FEATURE-Path-Mutation.md, FEATURE-Assignments.md, FEATURE-Structural-Builtins.md, FEATURE-String-Builtins.md, FEATURE-Regex-Builtins.md, FEATURE-Format-Builtins.md, FEATURE-Date-Math-Builtins.md, FEATURE-IO-Builtins.md, FEATURE-SQL-Metadata-Builtins.md, FEATURE-Module-Grammar.md |
| Provides    | complete jq conformance proof |
| Consumes    | executable jq, staged conformance corpus, all implemented language and builtin capabilities |

## Purpose

The completed application must pass every runnable case in the supplied jq 1.8.2 corpus, while preserving the declared exclusions and the interpreter's compile-time and runtime exit-code contract.

## Verification

The terminal verification runs `sh sources/full_test.sh` from the application root. The supplied script checks that `./jq` is executable, supplies `JQ`, invokes the unchanged conformance runner, and returns its verdict.

## Programmatic Acceptance

=== AC complete-conformance ===
Intent: The completed interpreter passes the supplied full jq conformance suite.
Suite: full

import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=subprocess.sys.stderr)
assert result.returncode == 0
=== END AC complete-conformance ===

## User Acceptance

- None.

## Guardrails

- This is the only story that runs the unfiltered conformance suite.
- The supplied corpus, exclusions, runner, and scoring script remain unmodified.
- The full suite's exit status is the acceptance verdict; diagnostics are printed only for troubleshooting.
