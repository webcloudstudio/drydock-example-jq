# FEATURE: Builtins Strings

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Defines jq string transformations, encoding conversions, interpolation, and format filters. |
| Depends On | FEATURE-Builtins-Structural.md |
| Provides | string transforms, JSON conversion, URI, HTML, CSV, TSV, shell, base64 formats |
| Consumes | generator evaluation, structural builtins, regular strings |

## Purpose

Implement jq string and encoding functionality using Python standard-library facilities, including transformations, conversions, interpolation, formats, Unicode, and JSON escaping.

## Programmatic Acceptance

=== AC builtins-strings-conformance ===
Intent: The scoped authoritative corpus cases covering string, encoding, conversion, interpolation, and format builtins execute and pass.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(@|split|join|trim|explode|implode|tostring|tojson|fromjson|ascii_)"
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC builtins-strings-conformance ===

## User Acceptance

- None.

## Guardrails

- Unicode whitespace and codepoint handling must follow the supplied specification.
- Format filters must not conflate JSON serialization with plain string conversion.
- Diagnostics must remain on stderr and never corrupt JSON stdout.
- No network or third-party package may be used.
