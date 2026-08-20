# FEATURE: Delivery Conformance

| Field       | Value |
|-------------|-------|
| Version     | 20260820 V1 |
| Description | Prove the completed jq interpreter passes the authoritative conformance corpus. |
| Depends On  | METADATA.md, ARCHITECTURE.md, FEATURE-Delivery-Assets.md, FEATURE-Frontend-Lexer.md, FEATURE-Frontend-Parser.md, FEATURE-Frontend-Diagnostics.md, FEATURE-Core-Generators.md, FEATURE-Core-Expressions.md, FEATURE-Core-Errors.md, FEATURE-Core-Utilities.md, FEATURE-Paths-Discovery.md, FEATURE-Paths-Mutation.md, FEATURE-Paths-Assignment.md, FEATURE-Control-Conditionals.md, FEATURE-Control-Reductions.md, FEATURE-Control-Bindings.md, FEATURE-Control-Functions.md, FEATURE-Builtins-Structural.md, FEATURE-Builtins-Strings.md, FEATURE-Builtins-Regex.md, FEATURE-Builtins-Numeric.md, FEATURE-Builtins-Streaming.md, FEATURE-Builtins-IO.md, FEATURE-Delivery-Executable.md, README.md |
| Provides    | complete jq conformance verification |
| Consumes    | ./jq, sources/full_test.sh, sources/run_conformance.py, sources/jq.test, sources/exclusions.txt |

## Intent

This terminal integration story runs the supplied scoring entry point after every implementation and delivery story has completed. The entry point is authoritative and is the sole release verdict for the interpreter.

## Verification

Run `sh sources/full_test.sh` from the application root. The command must execute the complete corpus, honor only the declared exclusions, and exit successfully without modifying any staged source asset.

## Programmatic Acceptance

=== AC suite-conformance ===
Intent: The completed interpreter passes the authoritative full conformance suite.
Suite: full
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=subprocess.stderr)
assert result.returncode == 0
=== END AC suite-conformance ===

## User Acceptance

- The completed standalone jq interpreter is accepted when the supplied scoring entry point exits successfully.

## Guardrails

- Run the supplied `sources/full_test.sh` exactly as staged.
- This is the only story permitted to run the unfiltered corpus.
- Do not modify, filter, skip, reinterpret, or regenerate files under `sources/`.
- Do not assert on diagnostic or summary text; the scoring command's exit status is the acceptance verdict.
