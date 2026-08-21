# FEATURE: Format and JSON Conversion Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provide jq scalar conversion, JSON conversion, and formatting filters. |
| Depends On  | FEATURE-BUILTINS-003.md |
| Provides    | tostring, tonumber, toboolean, tojson, fromjson, @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d |
| Consumes    | core value model, string builtins |

## Purpose

Implement jq's scalar conversion and format filters with compact JSON semantics, Unicode-safe escaping, URI and HTML encoding, tabular and shell formatting, and RFC 4648 base64 conversion.

## Behavior

- `tostring`, `tonumber`, and `toboolean` follow jq's accepted input types and runtime-error behavior.
- `tojson` serializes a value as a JSON string and `fromjson` parses JSON text.
- Format filters produce text according to jq's escaping rules.
- Format strings may combine literal text and interpolated values.
- Invalid conversion or format inputs raise runtime errors.

## Programmatic Acceptance

=== AC builtins-004-conversion ===
Intent: The authoritative corpus slice covering scalar and JSON conversion filters executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"tojson|fromjson|tostring|tonumber|toboolean"
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
=== END AC builtins-004-conversion ===

=== AC builtins-004-formats ===
Intent: The authoritative corpus slice covering jq format filters executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"@"
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
=== END AC builtins-004-formats ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library serialization and encoding facilities.
- Preserve compact JSON value semantics and jq's distinction between `tostring` and `tojson`.
- Do not assert or depend on diagnostic wording.
