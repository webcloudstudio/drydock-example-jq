# FEATURE: jq Interpolation and Formats

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Implements jq string interpolation and supported format filters. |
| Depends On  | FEATURE-Lexer.md, FEATURE-Parser.md |
| Provides    | interpolation, @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d |
| Consumes    | jq lexer token stream, jq parser and AST |

## Intent

Implement interpolated strings and format filters using standard-library codecs and escaping rules. Interpolations are generator-valued and preserve output order.

## Scope

- Parse and evaluate `\(expression)` inside strings.
- Implement text, JSON, HTML, URI, URI-decoding, CSV, TSV, shell, Base64, and Base64-decoding formats.
- Preserve literal text surrounding escaped interpolations.
- Report invalid format inputs as runtime errors.

## Programmatic Acceptance

=== AC formats-suite ===
Intent: The format implementation passes its authoritative conformance slice.
Suite: scoped

import subprocess

result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", r"@|interpolation"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC formats-suite ===

=== AC formats-interface ===
Intent: The executable accepts a format program and completes successfully.

import json
import subprocess

program = '@base64'
value = "format input"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert result.stdout.strip()
=== END AC formats-interface ===

=== AC formats-roundtrip ===
Intent: Base64 encoding followed by decoding preserves supplied input.

import json
import subprocess

value = "round trip"
program = "@base64 | @base64d"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
decoded = json.loads(result.stdout)
assert decoded == value
=== END AC formats-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library codecs and escaping facilities.
- Keep diagnostics on stderr and formatted values on stdout.
- Do not modify supplied corpus or harness assets.
