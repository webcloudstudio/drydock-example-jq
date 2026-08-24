# FEATURE: jq Literals and String Interpolation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse jq literals, strings, escapes, interpolation, and format expressions. |
| Depends On  | ARCHITECTURE.md, FEATURE-PARSE-001.md |
| Provides    | JSON literals, jq strings, escapes, interpolation, format literals |
| Consumes    | jq lexer and token stream |

## Scope

This story extends the lexer and parser with JSON-compatible numeric, boolean, and null literals; quoted jq strings; Unicode and JSON escapes; `\(expression)` interpolation; and `@text`, `@json`, `@uri`, and related format literals. Invalid escapes and malformed interpolation must be compile failures with exit status 3.

## Programmatic Acceptance

=== AC parse-002-conformance ===
Intent: The executable passes every selected corpus case covering interpolation, URI formatting, and Base64 formatting.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"interpolation|@base64|@uri"
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
=== END AC parse-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Preserve Unicode code points and jq generator behavior during interpolation.
- Do not alter any file under `sources/`.
