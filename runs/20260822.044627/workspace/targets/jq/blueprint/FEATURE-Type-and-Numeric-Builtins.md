# FEATURE: Type and Numeric Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define jq type inspection, length, conversion, numeric predicates, and mathematical builtins. |
| Depends On  | FEATURE-Slices-and-Iteration.md, FEATURE-Value-Model.md |
| Provides    | type, length, utf8bytelength, numeric predicates, tonumber, tostring, arithmetic math builtins |
| Consumes    | jq value model, field and index access |

## Intent

This capability supplies jq's standard type and numeric primitives using Python's standard library. It preserves jq truth about value kinds, Unicode byte lengths, numeric conversion, special values, and mathematical operations.

## Behavior

- `type` returns jq's six value-type names.
- `length` handles null, strings, arrays, objects, and numbers according to jq semantics and rejects booleans.
- `utf8bytelength` counts UTF-8 bytes for strings and rejects other types.
- `tonumber`, `toboolean`, and `tostring` perform jq-compatible conversions.
- `nan`, `infinite`, `isnan`, `isinfinite`, `isfinite`, and `isnormal` support special numeric values.
- Standard-library math functions required by the corpus are exposed with jq generator semantics.
- Numeric equality and serialization remain compatible with the literal-aware value model.

## Programmatic Acceptance

=== AC value-004-conformance ===
Intent: The authoritative corpus slice covering type, length, numeric predicates, conversion, and math builtins executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", "length|type|sqrt|floor|tonumber", "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC value-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not silently coerce booleans into numbers.
- Preserve jq's distinction between numeric values and boolean values.
