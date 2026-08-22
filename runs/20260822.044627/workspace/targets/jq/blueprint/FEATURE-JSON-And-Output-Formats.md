# FEATURE: JSON and Output Formats

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Convert jq values to JSON and supported textual output formats. |
| Depends On  | FEATURE-Value-Model.md, FEATURE-String-Manipulation.md |
| Provides    | tostring, tojson, fromjson, @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d |
| Consumes    | jq value model, string manipulation filters |

## Intent

Implement JSON conversion and jq format filters using only Python standard-library facilities. Preserve compact serialization, escaping, Unicode handling, interpolation, and generator ordering.

## Programmatic Acceptance

=== AC text-002-conformance ===
Intent: The implementation passes the authoritative JSON and output-format corpus slice.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"@text|@json|@html|@uri|@csv|@tsv|@sh|@base64"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC text-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not invoke external JSON, jq, shell, or encoding implementations.
- Keep diagnostics out of standard output.
- Do not modify staged scoring assets.
