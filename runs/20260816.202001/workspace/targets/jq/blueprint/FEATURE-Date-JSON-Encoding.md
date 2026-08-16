# FEATURE: Date, JSON, Encoding, and Environment

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide date, JSON conversion, encoding, and environment builtins for jq programs. |
| Depends On  | FEATURE-Formats.md, FEATURE-Numeric-Builtins.md |
| Provides    | date/time builtins, tojson, fromjson, env, $ENV, encoding helpers |
| Consumes    | JSON values, format filters, Python standard library |

## Purpose

Implement `tojson`, `fromjson`, `env`, `$ENV`, date conversion and formatting functions, and the encoding helpers required by the conformance corpus. All behavior must use Python standard-library facilities and preserve jq stream semantics.

## Behavior

- `tojson | fromjson` round-trips supported JSON values.
- `fromdateiso8601`, `todateiso8601`, `fromdate`, and `todate` use UTC.
- `gmtime`, `localtime`, `mktime`, `strptime`, `strftime`, and `strflocaltime` expose jq-compatible time arrays and formatting.
- `env` and `$ENV` expose the process environment without mutating it.
- JSON encoding remains compact and supports the supported special-number behavior.

## Programmatic Acceptance

=== AC date-json-roundtrip ===
Intent: JSON conversion preserves supplied values through a public jq round trip.

import json
import subprocess

value = {"text": "sample", "items": [1, True, None]}
payload = json.dumps(value, separators=(",", ":"))
result = subprocess.run(["./jq", "-c", "tojson | fromjson"], input=payload + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == value
=== END AC date-json-roundtrip ===

=== AC date-utc-roundtrip ===
Intent: ISO date conversion reverses a supplied UTC timestamp.

import subprocess

timestamp = "2015-03-05T23:51:47Z"
result = subprocess.run(["./jq", "-c", "fromdateiso8601 | todateiso8601"], input=timestamp + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert result.stdout.strip().strip('"') == timestamp
=== END AC date-utc-roundtrip ===

=== AC environment-read ===
Intent: Environment access returns a value supplied by the process environment.

import json
import os
import subprocess

key = "JQ_ACCEPTANCE_VALUE"
value = "acceptance"
result = subprocess.run(
    ["./jq", "-c", "env[$key]"],
    input=json.dumps(key) + "\n",
    capture_output=True,
    text=True,
    env={**os.environ, key: value},
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC environment-read ===

## User Acceptance

- None.

## Guardrails

- Do not access the network or third-party date, JSON, or encoding libraries.
- Do not mutate the process environment.
- Keep diagnostics on stderr and result values on stdout.
