# FEATURE: Builtin Format Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq value conversion, JSON serialization, and text-format builtins. |
| Depends On  | FEATURE-Core-Values-Operators.md, FEATURE-Builtin-Strings.md |
| Provides    | tostring, tonumber, toboolean, tojson, fromjson, @text, @json, @html, @uri, @urid, @csv, @tsv, @sh, @base64, @base64d |
| Consumes    | jq values and string builtins |

## Behavior

The interpreter converts numbers, booleans, and JSON strings according to jq semantics. It supports JSON round trips and the documented text, JSON, HTML, URI, CSV, TSV, shell, and Base64 formats, including interpolation and escaping.

## Programmatic Acceptance

=== AC conversion-roundtrip ===
Intent: JSON conversion preserves a supplied composite value.
import json
import subprocess

value = {"items": [1, "two", True], "empty": None}
result = subprocess.run(
    ["./jq", "-c", 'tojson | fromjson'],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC conversion-roundtrip ===

=== AC conversion-types ===
Intent: Numeric and boolean string conversions produce the values represented by supplied inputs.
import json
import subprocess

values = ["12", "true", "false"]
expected = [12, True, False]
program = '[.[0] | tonumber, .[1] | toboolean, .[2] | toboolean]'
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(values) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC conversion-types ===

=== AC conversion-base64 ===
Intent: Base64 encoding and decoding round-trip supplied text.
import json
import subprocess

value = "standard library"
result = subprocess.run(
    ["./jq", "-c", '@base64 | @base64d'],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC conversion-base64 ===

=== AC conversion-formats ===
Intent: The documented format filters return strings for supplied format inputs.
import json
import subprocess

value = ["alpha", "beta"]
result = subprocess.run(
    ["./jq", "-c", '[@csv, @tsv, @json]'],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
formats = json.loads(result.stdout)
assert len(formats) == 3
assert all(isinstance(item, str) for item in formats)
=== END AC conversion-formats ===

## User Acceptance

- None.

## Guardrails

- Formatting and conversion use only standard-library functionality and preserve compact JSON output.
