# FEATURE: jq Lexical Scanner

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Tokenizes jq programs according to the pinned jq lexer specification. |
| Depends On  | FEATURE-FOUNDATION-002.md |
| Provides    | jq lexer |
| Consumes    | executable jq |

## Scope

The lexer recognizes jq identifiers, field names, variable bindings, numeric and string literals, interpolation boundaries, format tokens, keywords, comments, operators, delimiters, recursive descent, optional and alternative operators, and invalid characters. It preserves string escapes and reports invalid lexical forms for compile-time rejection.

## Programmatic Acceptance

=== AC lexer-conformance-slice ===
Intent: The executable passes the non-empty conformance slice covering lexical forms, literals, strings, formats, delimiters, and invalid module syntax.

import json
import os
import subprocess
import sys

SELECT = r'^(\\.|\\[|\\{|def|if|try|reduce|foreach|module|include|%::|"|@)'

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
tally = report["summary"]
assert sum(tally.values()) > 0
assert tally["fail"] == 0 and tally["error"] == 0
assert result.returncode == 0
=== END AC lexer-conformance-slice ===

=== AC lexer-invalid-escape ===
Intent: An invalid string escape is rejected as a compile-time error.

import subprocess

result = subprocess.run(
    ["./jq", "-c", '"u\\vw"'],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 3
=== END AC lexer-invalid-escape ===

## User Acceptance

- Lexical behavior follows the supplied `sources/lexer.l` contract.

## Guardrails

- Keep source assets under `sources/` read-only.
- Do not delegate lexical scanning to an external jq executable or third-party parser.
