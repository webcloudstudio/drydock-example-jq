# FEATURE: Complete Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Verify the completed interpreter against the entire supplied jq conformance corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-Executable-Entry-Point.md, FEATURE-Process-Contract.md, FEATURE-JSON-IO-Boundary.md, FEATURE-Lexer.md, FEATURE-Literals-And-Interpolation.md, FEATURE-Filter-Grammar.md, FEATURE-Declarations-And-Control-Syntax.md, FEATURE-Generator-Core.md, FEATURE-Composition-And-Cartesian-Evaluation.md, FEATURE-Errors-And-Optional-Evaluation.md, FEATURE-Truthiness-And-Comparison.md, FEATURE-Value-Model.md, FEATURE-Field-And-Index-Access.md, FEATURE-Slices-And-Iteration.md, FEATURE-Type-And-Numeric-Primitives.md, FEATURE-Arithmetic-And-Structural-Operators.md, FEATURE-Boolean-And-Alternative-Operators.md, FEATURE-Conditionals-And-Exception-Flow.md, FEATURE-Labels-And-Breaks.md, FEATURE-Reductions-And-Iteration-Control.md, FEATURE-Recursive-Generators.md, FEATURE-Variable-Bindings.md, FEATURE-Function-Parameters.md, FEATURE-Function-Definitions-And-Recursion.md, FEATURE-Destructuring-Patterns.md, FEATURE-Path-Discovery.md, FEATURE-Path-Primitives.md, FEATURE-Deletion-And-Assignment.md, FEATURE-Complex-Assignment-Edges.md, FEATURE-Collection-Transformations.md, FEATURE-Sorting-And-Grouping.md, FEATURE-Object-Entries-And-Containment.md, FEATURE-Index-And-Membership-Utilities.md, FEATURE-String-Manipulation.md, FEATURE-JSON-And-Output-Formats.md, FEATURE-Regular-Expressions.md, FEATURE-Date-And-Time-Filters.md, FEATURE-Input-Streams.md, FEATURE-Diagnostics-And-Stderr.md, FEATURE-Streaming-Transformations.md, FEATURE-Conformance-Asset-Staging.md, FEATURE-Scoped-Conformance-Verification.md |
| Provides    | complete conformance release verification |
| Consumes    | executable jq, all interpreter capabilities, staged conformance assets |

## Purpose

Run the supplied scoring entry point once the complete interpreter is assembled. This is the terminal verification story and the project-level technical acceptance gate.

## Behavior

- `sources/full_test.sh` verifies that `./jq` is executable.
- The script invokes the supplied conformance runner over the complete corpus.
- The candidate must return zero for every executed valid case and exit 3 for every marked compile failure.
- Declared module-loader exclusions remain skipped by the supplied exclusion list.
- The story does not modify, filter, reinterpret, or replace the scoring assets.

## Programmatic Acceptance

=== AC complete-conformance ===
Intent: The completed executable passes the supplied full jq conformance suite.
Suite: full
Requires: executable=sh; scope=test
Requires: executable=python3; scope=test

import os
import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh"],
    capture_output=True,
    text=True,
    env={**os.environ},
)
print(result.stdout)
print(result.stderr, file=os.sys.stderr)
assert result.returncode == 0
=== END AC complete-conformance ===

=== AC executable-interface-final ===
Intent: The final executable accepts the fixed compact filter interface and completes successfully.
import json
import subprocess

program = "."
payload = '{"status":"ready"}\n'
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [json.loads(payload)]
assert actual == expected
=== END AC executable-interface-final ===

## User Acceptance

- None.

## Guardrails

- This is the only story permitted to invoke `sh sources/full_test.sh`.
- It is terminal and depends on every implementation and conformance story.
- Do not add selectors, skips, output reinterpretation, or exit-code substitution.
- Do not modify any file under `sources/`.
- The full-suite exit status is the acceptance verdict; diagnostics are for evidence only.
