# FEATURE: jq Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Lexical analysis for jq source programs. |
| Depends On  | ARCHITECTURE.md |
| Provides    | jq lexer |
| Consumes    | interpreter architecture |

## Capability

The lexer recognizes jq keywords, identifiers, fields, variable bindings, numeric literals, strings and escapes, interpolation delimiters, format tokens, operators, delimiters, comments, and invalid characters. It preserves source locations needed for diagnostics and reports malformed lexical input as a compile failure.

## Programmatic Acceptance

=== AC lexer-invalid-escape ===
Intent: The lexer rejects a malformed string escape with compile exit status 3.

import os
import subprocess

program = '"u\\vw"'
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
=== END AC lexer-invalid-escape ===

=== AC lexer-module-syntax ===
Intent: The lexer and front end reject malformed module syntax at compile time.

import os
import subprocess

program = 'module []; 0'
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
=== END AC lexer-module-syntax ===

=== AC lexer-conformance ===
Intent: Executed conformance cases exercising lexical syntax pass without failures or errors.

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"\\(|@(?:text|json|html|uri|urid|csv|tsv|sh|base64|base64d)|#"
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
=== END AC lexer-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve Unicode source text and JSON escape semantics.
- Treat comments and whitespace according to `sources/lexer.l`.
- Reject invalid characters and malformed escapes with exit code `3`.
