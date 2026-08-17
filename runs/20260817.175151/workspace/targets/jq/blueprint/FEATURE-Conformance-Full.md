# FEATURE: Full Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Verify the completed jq interpreter against the complete supplied conformance corpus. |
| Depends On  | FEATURE-CLI-Entrypoint.md, FEATURE-CLI-Exit-Semantics.md, FEATURE-CLI-Documentation.md, FEATURE-Front-Lexer.md, FEATURE-Front-Parser.md, FEATURE-Front-Validation.md, FEATURE-Core-Generators.md, FEATURE-Core-Indexing.md, FEATURE-Core-Values-Operators.md, FEATURE-Core-Construction.md, FEATURE-Flow-Bindings.md, FEATURE-Flow-Functions.md, FEATURE-Flow-Control-Errors.md, FEATURE-Flow-Reduce.md, FEATURE-Flow-Recursion-Utilities.md, FEATURE-Path-Discovery.md, FEATURE-Path-Mutation.md, FEATURE-Path-Assignment.md, FEATURE-Builtin-Collections.md, FEATURE-Builtin-Strings.md, FEATURE-Builtin-Regex.md, FEATURE-Builtin-Format-Conversion.md, FEATURE-Builtin-Math-Date.md, FEATURE-IO-Input-Diagnostics.md, FEATURE-IO-Streaming.md, FEATURE-Conformance-Staging.md |
| Provides    | Completed jq release verdict |
| Consumes    | executable jq, staged conformance harness |

## Purpose

This terminal feature assembles the completed interpreter and executes the supplied scoring entry point. The full corpus, declared exclusions, executable contract, compile/runtime status behavior, output ordering, and runtime partial-output behavior are judged by the authoritative harness.

## Assembly Contract

The application root contains an executable `jq`, and the staged `sources/full_test.sh` remains the release entry point. The command runs from the completed application root and is not filtered, redirected, or reinterpreted.

## Programmatic Acceptance

=== AC conformance-full ===
Intent: The completed interpreter passes the supplied full conformance gate.

Suite: full
Requires: executable=python3; scope=test
Requires: executable=sh; scope=test

import os
import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": os.path.join(os.getcwd(), "jq")},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC conformance-full ===

## User Acceptance

- None.

## Guardrails

- This is the sole whole-corpus acceptance check.
- The scoring assets must remain unchanged.
- Acceptance is determined only by the scoring command's exit status; diagnostic output is printed only to support investigation.
