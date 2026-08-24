# FEATURE: JSON and Output Format Filters

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide JSON conversion and jq output-format filters with standard-library escaping semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-TEXT-001.md, FEATURE-VALUE-001.md |
| Provides    | tostring, tojson, fromjson, @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d |
| Consumes    | jq value model, string manipulation |

## Workflow

Implement conversion filters and format filters using only Python standard-library facilities. Preserve interpolation behavior, compact JSON conversion, Unicode handling, escaping rules, and generator ordering. Support HTML, URI, shell, CSV, TSV, Base64, and inverse Base64 formats described by the manual.

## Programmatic Acceptance

=== AC text-002-scoped-conformance ===
Intent: The authoritative corpus cases covering JSON conversion and output formats execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"@text|@json|@html|@uri|@urid|@csv|@tsv|@sh|@base64|@base64d|tojson|fromjson|tostring"
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
=== END AC text-002-scoped-conformance ===

=== AC text-002-formats ===
Intent: The corpus exercises the declared format families rather than an empty selector.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"@html|@uri|@base64|@csv|@tsv|@sh"
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
=== END AC text-002-formats ===

## User Acceptance

- None.

## Guardrails

- Do not shell out to jq or use third-party formatting libraries.
- Preserve stdout JSON-lines behavior and send diagnostics only to stderr.
