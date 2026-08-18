# FEATURE: Format and Encoding Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provides jq text, JSON, HTML, URI, shell, CSV, TSV, and Base64 formatting filters. |
| Depends On  | FEATURE-String-Builtins.md |
| Provides    | @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d |
| Consumes    | string filters, JSON serialization |

## Purpose

Implement jq format filters and their interpolation rules with deterministic standard-library encoders.

## Behavior

- `@text` and `@json` serialize values according to jq semantics.
- `@html` escapes HTML/XML-sensitive characters.
- `@uri` and `@urid` percent-encode and decode UTF-8 text.
- `@csv`, `@tsv`, and `@sh` format arrays using jq quoting and escaping rules.
- `@base64` and `@base64d` implement RFC 4648 conversion.
- Format prefixes followed by interpolated strings escape interpolated portions only.
- Invalid input produces runtime status 5.

## Programmatic Acceptance

=== AC format-conformance ===
Intent: The implementation passes the authoritative corpus cases for jq formats and encodings.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select",
     r"(^|[^A-Za-z])(@text|@json|@html|@uri|@urid|@csv|@tsv|@sh|@base64d?)"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC format-conformance ===

=== AC format-runtime-status ===
Intent: Unsupported format input produces the documented runtime failure status.
import subprocess

program = r'@csv'
result = subprocess.run(["./jq", "-c", program], input="{}\n", capture_output=True, text=True)
assert result.returncode == 5
=== END AC format-runtime-status ===

## User Acceptance

- None.

## Guardrails

- Implement encodings with Python standard-library modules only.
- Preserve compact JSON output and jq generator ordering.
