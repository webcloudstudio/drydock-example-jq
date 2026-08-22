# FEATURE: Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Tokenizes jq programs according to the supplied lexical specification. |
| Depends On  | ARCHITECTURE.md |
| Provides    | jq tokens, comments, delimiters, identifiers, literals, bindings |
| Consumes    | interpreter architecture |

## Intent

The lexer recognizes jq keywords, identifiers, field selectors, variable bindings, literals, operators, comments, delimiters, format tokens, and string/interpolation state transitions. Comments are ignored without altering adjacent program structure. Invalid characters and malformed literals are reported as compile failures.

## Programmatic Acceptance

=== AC lexer-basic-syntax ===
Intent: The authoritative lexer-focused corpus slice executes successfully.

import json
import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", r"^(true|false|null|1|\.)$", "--json"],
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
=== END AC lexer-basic-syntax ===

=== AC lexer-comments ===
Intent: Comments are ignored while the surrounding filter remains executable.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "1 # comment\n, 2"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
assert result.stdout.splitlines() == ["1", "2"]
=== END AC lexer-comments ===

=== AC lexer-invalid-token ===
Intent: Invalid lexical input is rejected as a compile failure.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "%::wat"],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 3
=== END AC lexer-invalid-token ===

## User Acceptance

- None.

## Guardrails

- Follow `sources/lexer.l` for token boundaries and lexical states.
- Do not silently reinterpret invalid escapes or characters.
- Preserve comments, delimiters, bindings, and interpolation distinctions for the parser.
