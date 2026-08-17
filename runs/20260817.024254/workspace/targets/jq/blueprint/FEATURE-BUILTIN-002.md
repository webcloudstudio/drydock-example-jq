# FEATURE: jq String and Unicode Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide jq string, Unicode, conversion, interpolation, and escaping builtins. |
| Depends On  | FEATURE-DATA-001.md, FEATURE-EVAL-002.md |
| Provides    | string trimming, splitting, joining, case conversion, indexing, escaping, JSON conversion |
| Consumes    | JSON structural operations, generator evaluator |

## Purpose

Implement jq-compatible string and Unicode operations, including trimming, splitting, joining,
indices, case conversion, explode/implode, scalar conversions, JSON conversion, and interpolation.
Use Unicode codepoint semantics and preserve jq runtime errors.

## Programmatic Acceptance

=== AC builtin-002-string-operations ===
Intent: String splitting, joining, trimming, and indexing return jq-compatible values.
import json
import subprocess

source = '"  a,b  "'
program = '[trim, split(","), (split(",") | join("-")), indices("a")]'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == ["a,b", ["  a", "b  "], "  a-b  ", [2]]
=== END AC builtin-002-string-operations ===

=== AC builtin-002-unicode ===
Intent: Explode and implode round-trip Unicode codepoints.
import json
import subprocess

source = '"μé"'
program = 'explode | implode'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == json.loads(source)
=== END AC builtin-002-unicode ===

=== AC builtin-002-conversion ===
Intent: JSON conversion distinguishes tostring from tojson and supports round trips.
import json
import subprocess

source = '["x",1,{"a":2}]'
program = '[.[] | tojson | fromjson]'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == json.loads(source)
=== END AC builtin-002-conversion ===

=== AC builtin-002-error ===
Intent: Invalid scalar conversion produces the documented runtime failure class.
import subprocess

source = '"not-a-number"'
program = 'tonumber'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 5
assert result.stdout == ""
=== END AC builtin-002-error ===

## User Acceptance

- None.

## Guardrails

- Count Unicode strings by codepoint where jq specifies codepoint semantics.
- Preserve embedded NULs, control characters, and non-ASCII characters.
- Diagnostics belong on stderr; conversion failures must not produce fabricated stdout values.
