# FEATURE: Lexer

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Implements jq lexical analysis for programs, literals, operators, strings, and interpolation. |
| Depends On  | ARCHITECTURE.md |
| Provides    | jq lexer |
| Consumes    | Interpreter architecture |

## Scope

The lexer recognizes identifiers, fields, variable bindings, numeric and string literals, comments, operators, delimiters, formats, module keywords, string interpolation boundaries, and valid JSON escapes. It preserves source positions sufficiently for diagnostics.

## Programmatic Acceptance

=== AC lexer-corpus-slice ===
Intent: The lexer and its integration with the front end pass the corpus cases covering literals, comments, strings, interpolation, formats, and delimiters.

import os
import subprocess
import sys

selector = r"^(true|false|null|1$|\.|@text|@base64|\"inter\\\(|\{a:|\.foo|%::wat)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC lexer-corpus-slice ===

=== AC lexer-invalid-escape ===
Intent: Invalid string escapes are rejected with compile status 3.

import os
import subprocess

program = r'"u\vw"'
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 3
=== END AC lexer-invalid-escape ===

=== AC lexer-comments ===
Intent: Comments and continued comments do not become program tokens.

import os
import subprocess

program = "1, # ignored\n2"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert result.stdout.splitlines() == ["1", "2"]
=== END AC lexer-comments ===

## User Acceptance

- None.

## Guardrails

- Follow `sources/lexer.l` for token boundaries and escape behavior.
- Do not treat comment contents as executable tokens.
- Preserve interpolation and Unicode string content.
- Keep lexer failures on the compile-error path.
