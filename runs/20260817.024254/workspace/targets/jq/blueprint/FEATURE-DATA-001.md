# FEATURE: JSON Values and Structural Operations

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | jq JSON values, indexing, slicing, iteration, typing, equality, ordering, containment, and numeric behavior are compatible with the corpus. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-001.md, FEATURE-EVAL-002.md |
| Provides    | JSON values, indexing, slicing, iteration, type, equality, ordering, containment |
| Consumes    | generator evaluator |

## Intent

This capability defines jq's immutable JSON value model and structural operations using Python's standard library. It covers null, booleans, numbers, strings, arrays, and objects, including Unicode-aware behavior and jq-compatible numeric edge cases.

## Behavior

- JSON values retain jq's distinctions between null, booleans, numbers, strings, arrays, and objects.
- Object keys and array indices support jq indexing and optional indexing behavior.
- Slices work for arrays and strings with omitted, negative, fractional, and out-of-range bounds.
- Iteration preserves array order and object value traversal.
- `type`, `length`, Unicode byte length, equality, ordering, and containment follow jq semantics.
- Numbers support literal-preserving output where required and floating-point arithmetic compatibility.
- Compact serialization emits one valid JSON value per line, including jq-compatible handling of non-finite values.

## Programmatic Acceptance

=== AC data-001-structure ===
Intent: The implementation passes the authoritative corpus cases for JSON values, indexing, slicing, iteration, typing, and Unicode lengths.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"Types and Values|Field access|Array/String Slice|Array/Object Value Iterator|Slicing|length|utf8bytelength|type"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC data-001-structure ===

=== AC data-001-ordering ===
Intent: The implementation passes the authoritative corpus cases for equality, ordering, sorting order, and containment.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"equality|comparison|sort|contains|inside|keys|has\("
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC data-001-ordering ===

=== AC data-001-numbers ===
Intent: The implementation passes the authoritative corpus cases for numeric literals, floating-point behavior, NaN, infinity, and compact JSON conversion.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

pattern = r"number|numbers|nan|infinite|decnum|literal number|tojson|fromjson"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC data-001-numbers ===

## User Acceptance

- None.

## Guardrails

- Do not conflate booleans with numbers.
- Preserve immutable value semantics across structural operations.
- Do not shell out for JSON parsing, serialization, or numeric behavior.
