# FEATURE: Value Model

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines the internal representation and serialization of jq values, including special numbers. |
| Depends On  | FEATURE-Truthiness-and-Comparison.md |
| Provides    | null, booleans, numbers, strings, arrays, objects, NaN, infinities |
| Consumes    | truthiness, equality, and ordering |

## Value Contract

The interpreter represents JSON-compatible nulls, booleans, numbers, strings, arrays, and objects using standard-library facilities. Numeric handling preserves literal-aware behavior required by the corpus and supports NaN and infinities where jq exposes them. Serialization emits valid JSON-compatible output for the harness.

## Programmatic Acceptance

=== AC value-001-conformance ===
Intent: The authoritative corpus special-number and number-serialization cases execute without failures.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"nan|infinite|tojson|fromjson"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
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
=== END AC value-001-conformance ===

=== AC value-001-special-values ===
Intent: The implementation accepts and processes the special numeric values exercised by jq.
Requires: executable=python3; scope=test

import json
import subprocess

input_value = "null\n"
result = subprocess.run(
    ["./jq", "-c", "infinite, nan | type"],
    input=input_value,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == ["number", "number"]
=== END AC value-001-special-values ===

## User Acceptance

- None.

## Guardrails

- No third-party numeric or jq implementation may be used.
- NaN and infinity handling must remain compatible with the supplied harness.
- Numeric formatting must not introduce non-JSON output lines.
