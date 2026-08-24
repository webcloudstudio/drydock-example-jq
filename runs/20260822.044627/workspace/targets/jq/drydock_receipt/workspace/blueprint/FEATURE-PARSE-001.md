# FEATURE: jq Lexical Scanner

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Tokenizes jq literals, identifiers, operators, delimiters, comments, and bindings. |
| Depends On  | ARCHITECTURE.md |
| Provides    | jq lexer and token stream |
| Consumes    | JSON input and filter source |

## Scope

Implement lexical scanning according to the supplied `sources/lexer.l` and `sources/parser.y` references. The scanner recognizes numeric literals, identifiers, field selectors, variable bindings, keywords, operators, delimiters, comments, and format tokens, while preserving source locations needed for diagnostics.

Lexical errors must be reported as compile failures and must not be confused with runtime errors.

## Programmatic Acceptance

=== AC lexer-conformance ===
Intent: The lexer and front end pass the corpus slice containing primitive literals and identity syntax.

import json
import os
import subprocess
import sys

select = r"^(true|false|null|1|\.)$"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC lexer-conformance ===

=== AC lexer-rejects-invalid-source ===
Intent: An invalid lexical character is rejected with the compile-failure status.

import subprocess

result = subprocess.run(
    ["./jq", "-c", "%::wat"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC lexer-rejects-invalid-source ===

=== AC lexer-comments ===
Intent: Comments do not alter evaluation of the surrounding jq program.

import subprocess

program = "1 # comment\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout.splitlines() == ["1"]
=== END AC lexer-comments ===

## User Acceptance

- None.

## Guardrails

- Follow the token forms and delimiter behavior defined by `sources/lexer.l`.
- Preserve comments as non-semantic input.
- Reject invalid characters at compile time.
- Do not modify the supplied lexer or parser reference files.
