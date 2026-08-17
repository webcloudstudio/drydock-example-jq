# FEATURE: Value Semantics

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implements jq operators, indexing, slicing, ordering, numeric behavior, and JSON value semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-GENERATOR.md |
| Provides    | jq value operations, arithmetic, comparison, indexing, slicing |
| Consumes    | generator evaluator |

## Scope

Implement jq arithmetic and boolean operators, equality and ordering, null handling, string and array operations, object merging, field and index access, iteration access, slices, numeric conversion and edge behavior, and runtime failures with exit code 5.

Operations must use jq's type-sensitive semantics and preserve the distinction between booleans and numbers. Indexing and slicing must support optional forms and jq-compatible bounds behavior.

## Programmatic Acceptance

=== AC values-operators ===
Intent: The authoritative corpus passes arithmetic, comparison, boolean, string, array, and object value cases.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^\d+\+\d|^\.\+|^\.a\+\.b|^sort$|^contains\(|^\. <|^if "],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC values-operators ===

=== AC values-indexing ===
Intent: Field access, iteration, negative indexes, and slices conform to jq behavior.
Suite: scoped

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     r"^\.foo|^\.\[\]|^\.\[-|^\.\[.*:"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC values-indexing ===

=== AC values-runtime-error ===
Intent: A compiled program that raises a jq runtime error exits with status 5.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "1 / 0"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC values-runtime-error ===

## User Acceptance

- None.

## Guardrails

- Preserve jq type distinctions and ordering.
- Do not silently coerce incompatible operand types.
- Runtime failures use exit code 5; compile failures remain exit code 3.
