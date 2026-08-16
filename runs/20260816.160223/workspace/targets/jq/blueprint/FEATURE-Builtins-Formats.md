# FEATURE: Formats and Date Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq-compatible serialization, escaping, encoding, and date helpers. |
| Depends On  | ARCHITECTURE.md, FEATURE-Values-Model.md, FEATURE-Builtins-Strings.md |
| Provides    | JSON/text/URI/HTML/CSV/TSV/shell/base64 formats, date and time helpers |
| Consumes    | jq values and string builtins |

## Purpose

Implement jq format filters and standard-library date/time functions without external dependencies.

## Behavior

Support `tojson`, `fromjson`, `@text`, `@json`, `@html`, `@uri`, `@urid`, `@csv`, `@tsv`, `@sh`, `@base64`, and `@base64d`. Implement ISO-8601 conversion plus `strptime`, `strftime`, `strflocaltime`, `gmtime`, `localtime`, and `mktime` where supported by the standard library.

Formatting errors and invalid input types produce runtime errors. JSON output remains compact and structurally valid.

## Programmatic Acceptance

=== AC formats-roundtrip ===
Intent: JSON, URI, HTML, CSV, TSV, shell, and base64 formats produce reversible or contract-defined values.

import json
import subprocess

source = '"!()<>&\'\\"\\t"'
program = '[@text, @json, @html, (@uri | @urid), ([1,.] | @csv), ([1,.] | @tsv), (@base64 | @base64d)]'
result = subprocess.run(["./jq", "-c", program], input=source, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
values = json.loads(result.stdout)
assert values[0] == json.loads(source)
assert json.loads(values[1]) == json.loads(source)
assert values[2] == "!()&lt;&gt;&amp;&apos;&quot;\\t"
assert values[3] == json.loads(source)
assert values[4] == "1,\"!()<>&'\"\"\\t\""
assert values[5] == "1\\t!()<>&'\"\\\\t"
assert values[6] == json.loads(source)
=== END AC formats-roundtrip ===

=== AC dates ===
Intent: ISO date conversion and low-level date formatting round-trip through the jq executable.

import json
import subprocess

date_text = "2015-03-05T23:51:47Z"
program = 'fromdateiso8601 | todateiso8601'
result = subprocess.run(["./jq", "-c", program], input=json.dumps(date_text), capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert json.loads(result.stdout) == date_text
=== END AC dates ===

=== AC format-errors ===
Intent: Invalid format input reports a runtime failure.

import subprocess

result = subprocess.run(
    ["./jq", "-c", '@csv'],
    input='"not-an-array"',
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 5
=== END AC format-errors ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library encoding, URL, JSON, shell-escaping, and datetime facilities.
- Do not introduce locale-dependent behavior where UTC behavior is specified.
- Do not add third-party runtime dependencies.
