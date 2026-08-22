# FEATURE: Type and Numeric Primitives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq type inspection, numeric conversion, measurement, and mathematical primitives. |
| Depends On  | FEATURE-Value-Model.md, FEATURE-Field-And-Index-Access.md, FEATURE-Truthiness-And-Comparison.md |
| Provides    | type, length, utf8bytelength, tonumber, toboolean, numeric predicates, floor, sqrt, math primitives |
| Consumes    | jq values, comparison semantics |

## Intent

Implement jq's type and numeric builtins using Python's standard library. Support type inspection, lengths, UTF-8 byte counts, numeric and boolean conversion, finite/NaN predicates, rounding, square roots, and the mathematical functions exercised by the corpus.

Numbers must preserve jq-compatible equality and serialization behavior, including NaN and infinities. Invalid input types and conversions raise jq runtime errors.

## Behavior

- `type` returns jq's six type names.
- `length` handles null, strings, arrays, objects, and numbers; booleans are invalid.
- `utf8bytelength` accepts strings and counts UTF-8 bytes.
- `tonumber` and `toboolean` preserve existing values and convert valid strings.
- Numeric predicates distinguish finite, infinite, NaN, and normal values.
- `floor`, `sqrt`, and required standard math functions follow jq numeric semantics.

## Programmatic Acceptance

=== AC value-004-conformance ===
Intent: The type and numeric primitive implementation passes every selected conformance case containing the owned numeric and type syntax.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"length|type|sqrt|floor|tonumber"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC value-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not silently coerce invalid jq values.
- Preserve generator ordering and runtime error behavior.
