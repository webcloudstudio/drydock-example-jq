# FEATURE: Strings and Interpolation Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse JSON strings, escapes, interpolation, and format literals. |
| Depends On  | FEATURE-Lexer.md |
| Provides    | JSON string literals, escapes, interpolation, format literals |
| Consumes    | jq tokenization |

## Programmatic Acceptance

=== AC parse-002-interpolation ===
Intent: The authoritative corpus executes the non-empty interpolation and format-literal slice owned by this parser story.

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
=== END AC parse-002-interpolation ===

=== AC parse-002-escapes ===
Intent: The authoritative corpus executes string escape and Unicode cases without compile or runtime failures.

import json
import os
import subprocess
import sys

selector = r"interpolation|@base64|@uri|@html"
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
=== END AC parse-002-escapes ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Preserve interpolation generator multiplicity and ordering.
- Do not modify files under `sources/`.
