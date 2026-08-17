# FEATURE: String Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Implement jq string, Unicode, trimming, splitting, and codepoint builtins. |
| Depends On  | FEATURE-Core-Values-Operators.md |
| Provides    | trimming, splitting, joining, case conversion, explode, implode, UTF-8 length |
| Consumes    | jq value semantics |

## Intent

Implement Unicode-aware string operations, including trim variants, prefix and suffix removal, splitting, joining, ASCII case conversion, codepoint conversion, and UTF-8 byte length. Non-string inputs must produce jq-compatible runtime errors.

## Programmatic Acceptance

=== AC string-trimming-and-splitting ===
Intent: Trimming and splitting preserve string content and delimiters.

import json
import os
import subprocess

payload = "  alpha,beta  "
program = '[trim, split(",")]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0] == payload.strip()
assert actual[1] == payload.strip().split(",")
=== END AC string-trimming-and-splitting ===

=== AC prefix-suffix-case ===
Intent: Prefix, suffix, and ASCII case operations transform only the requested characters.

import json
import os
import subprocess

payload = "fooBarfoo"
program = '[ltrimstr("foo"), rtrimstr("foo"), ascii_upcase, ascii_downcase]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0] == payload.removeprefix("foo")
assert actual[1] == payload.removesuffix("foo")
assert actual[2] == "FOOBARFOO"
assert actual[3] == "foobarfoo"
=== END AC prefix-suffix-case ===

=== AC codepoints-and-byte-length ===
Intent: Codepoint conversion and UTF-8 byte length are inverse-compatible for valid text.

import json
import os
import subprocess

payload = "µ"
program = '[explode, explode | implode, utf8bytelength]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[1] == payload
assert actual[2] == len(payload.encode("utf-8"))
assert actual[0] == [ord(character) for character in payload]
=== END AC codepoints-and-byte-length ===

=== AC string-join ===
Intent: join converts supported scalar values and treats null as an empty field.

import json
import os
import subprocess

payload = ["a", 2, True, None]
separator = ","
program = f'join({json.dumps(separator)})'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == separator.join(["a", "2", "true", ""])
=== END AC string-join ===

## User Acceptance

- None.

## Guardrails

- String length and offsets use Unicode codepoints where jq specifies them.
- UTF-8 byte length counts encoded bytes, not Python characters.
- Non-string arguments must raise runtime errors with exit status 5 rather than being silently coerced.
