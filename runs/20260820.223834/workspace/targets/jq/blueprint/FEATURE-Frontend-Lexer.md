# FEATURE: Frontend Lexer

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Tokenizes jq programs according to the supplied lexical specification. |
| Depends On | ARCHITECTURE.md, FEATURE-Delivery-Assets.md |
| Provides | jq token stream |
| Consumes | sources/lexer.l, sources/jq.test, sources/jq-manual.txt |

## Scope

Implement lexical recognition for whitespace, comments, Unicode, numeric literals, JSON strings and escapes, interpolation, formats, identifiers, fields, bindings, module names, delimiters, and jq operators.

## Programmatic Acceptance

=== AC lexer-corpus ===
Intent: The lexer and its dependent frontend pass the executable corpus slice covering literal, field, format, definition, module, and invalid-character syntax.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"^(true|false|null|[-0-9]|\.|@|def|module|include|%::)"
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
=== END AC lexer-corpus ===

=== AC lexer-unicode-comments ===
Intent: The lexer-dependent frontend executes corpus cases containing Unicode literals, comments, escapes, and interpolation.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(unicode|interpolation|escape|comment|byte order mark|\\u03bc|\\\()"
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
=== END AC lexer-unicode-comments ===

## User Acceptance

- None.

## Guardrails

- Preserve embedded Unicode whitespace and newline behavior required by the corpus.
- Reject invalid escapes and invalid lexical characters with compile exit 3.
- Do not modify the supplied lexer specification or corpus.
