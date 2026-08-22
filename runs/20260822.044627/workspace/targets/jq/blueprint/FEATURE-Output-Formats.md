# FEATURE: Output Formats

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide JSON conversion and jq output-format filters. |
| Depends On  | FEATURE-String-Builtins.md, FEATURE-Json-IO.md |
| Provides    | tostring, tojson, fromjson, @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d |
| Consumes    | string manipulation builtins, JSON serializer |

## Intent

Implement conversion between jq values and JSON text, plus the required text, HTML, URI, CSV, TSV, shell, and base64 format filters. Preserve interpolation behavior and stream ordering.

## Programmatic Acceptance

=== AC text-002-conformance ===
Intent: JSON conversion and output-format filters execute through the candidate executable.

import subprocess

program = '["x"|@text, "x"|@json, "<x>"|@html, "a b"|@uri, "a+b"|@urid, ["a","b"]|@csv, ["a","b"]|@tsv, ["a b"]|@sh, "hi"|@base64, "aGk="|@base64d, ({"x":1}|tojson), ("{\\"x\\":1}"|fromjson)]'
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
values = __import__("json").loads(result.stdout)
assert len(values) == 12
assert values[0] == "x"
assert values[1] == '"x"'
assert values[2] == "&lt;x&gt;"
assert values[3] == "a%20b"
assert values[8] == "aGQgYg==" or values[8] == "aGk="
=== END AC text-002-conformance ===

=== AC text-002-interface ===
Intent: The format-filter interface returns compact JSON output for a representative filter.

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", '"hello world" | @uri'],
    input="null\n",
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
assert json.loads(result.stdout) == "hello%20world"
=== END AC text-002-interface ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Preserve compact JSON values and one output per line.
- Do not modify staged scoring assets.
