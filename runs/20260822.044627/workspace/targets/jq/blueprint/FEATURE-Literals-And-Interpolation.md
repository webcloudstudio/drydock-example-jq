# FEATURE: Literals and Interpolation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Parse and evaluate jq literals, escapes, format filters, and string interpolation. |
| Depends On  | FEATURE-Lexer.md |
| Provides    | JSON string escapes, Unicode literals, string interpolation, format tokens |
| Consumes    | jq lexer, interpreter architecture |

## Scope

This capability handles JSON-compatible literals, Unicode and escaped string content, `\(expression)` interpolation, and format tokens such as `@uri`, `@base64`, and `@text`. Invalid escapes and malformed interpolation are compile-time errors.

## Programmatic Acceptance

=== AC literals-interpolation-conformance ===
Intent: The authoritative corpus slice exercising interpolation and format tokens executes and passes with no failures or errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"interpolation|@base64|@uri"
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC literals-interpolation-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Invalid escapes and malformed interpolation must return compile exit status 3.
- Format escaping must not alter literal text outside interpolated expressions.
