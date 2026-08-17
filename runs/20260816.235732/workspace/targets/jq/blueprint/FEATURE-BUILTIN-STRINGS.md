# FEATURE: jq String and Conversion Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Define jq string, regular-expression, format, conversion, encoding, and date builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-VALUES.md, FEATURE-LANG-BINDINGS.md |
| Provides    | string transforms, regex filters, formats, JSON conversion, base64, URI, CSV, TSV, shell escaping, date functions |
| Consumes    | jq value operations, generator evaluator |

## Scope

Implement the standard-library string and conversion surface described by the jq manual, including Unicode codepoints, regular expressions, interpolation, format filters, JSON conversion, base64, URI, CSV, TSV, shell escaping, and UTC dates.

## Behavior

- String operations use Unicode codepoints and preserve jq's null and type-error behavior.
- Regular-expression filters support matching, captures, scanning, splitting, substitution, and supported flags.
- Format filters produce text for JSON, HTML, URI, CSV, TSV, shell, base64, and inverse formats.
- `tojson` and `fromjson` serialize and parse JSON independently of `tostring`.
- Date functions use UTC and the documented epoch and broken-down time representations.

## Programmatic Acceptance

=== AC string-conversion ===
Intent: String conversion round-trips the supplied JSON value.
import json
import subprocess

source_value = {"a": [1, "x"]}
program = "tojson | fromjson"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == source_value
=== END AC string-conversion ===

=== AC string-format ===
Intent: Base64 and URI formats encode and decode the supplied text.
import json
import subprocess

source_value = "hello world"
program = "[@base64, (@uri | @urid)]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[1] == source_value
assert isinstance(actual[0], str)
=== END AC string-format ===

=== AC string-regex ===
Intent: Regular-expression matching identifies the supplied pattern.
import json
import subprocess

source_value = "abc123"
pattern = r"[0-9]+"
program = f"test({json.dumps(pattern)})"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) is True
=== END AC string-regex ===

=== AC string-date ===
Intent: UTC date conversion round-trips the supplied ISO timestamp.
import json
import subprocess

source_value = "2015-03-05T23:51:47Z"
program = "fromdateiso8601 | todateiso8601"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == source_value
=== END AC string-date ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not assume locale-dependent behavior for UTC date functions.
- Do not compare diagnostics by message text in acceptance logic.
