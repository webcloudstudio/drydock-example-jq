# FEATURE: Streaming Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provide jq stream encoding, reconstruction, and path-truncation filters. |
| Depends On  | FEATURE-BUILTINS-006.md |
| Provides    | tostream, fromstream, truncate_stream |
| Consumes    | path engine, generator evaluator |

## Purpose

Implement jq's streaming representation for nested arrays, objects, scalars, and empty containers. Support reconstruction from stream events and truncation of leading path components while preserving event ordering.

## Behavior

- `tostream` emits path/value and container-end stream records in jq order.
- `fromstream` reconstructs JSON values from stream records.
- `truncate_stream` removes the requested number of leading path elements and discards or emits records according to jq semantics.
- Nested values, empty containers, and multiple stream values preserve ordering.
- Invalid stream structures raise runtime errors.

## Programmatic Acceptance

=== AC builtins-007-streaming ===
Intent: The authoritative corpus slice covering tostream, fromstream, and truncate_stream executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"tostream|fromstream|truncate_stream"
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC builtins-007-streaming ===

=== AC builtins-007-roundtrip ===
Intent: The authoritative streaming round-trip cases execute and pass without failures or errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"fromstream|tostream"
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
=== END AC builtins-007-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Preserve stream event ordering and multiplicity.
- Do not confuse jq stream records with ordinary output values.
- Use immutable reconstruction semantics and retain runtime error status 5 for invalid inputs.
