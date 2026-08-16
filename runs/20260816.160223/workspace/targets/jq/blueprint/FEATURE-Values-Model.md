# FEATURE: Values and JSON Model

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Define jq values, numeric behavior, JSON parsing, and compact serialization. |
| Depends On  | ARCHITECTURE.md, FEATURE-Eval-Core.md |
| Provides    | JSON value model and serialization |
| Consumes    | ordered generator evaluator |

## Intent

The runtime represents jq null, booleans, strings, arrays, objects, numbers, NaN, and infinities using only Python's standard library. JSON input is parsed as a stream of values and results are serialized as compact JSON lines.

Numeric literals preserve their source representation where jq requires it, while arithmetic follows jq-compatible floating-point behavior. `have_decnum` reports the supported non-decnum branch.

## Behaviors

- JSON values retain jq type distinctions; booleans are not numbers.
- Unicode strings and embedded NUL characters round-trip.
- NaN and infinities are valid jq numeric values where the corpus requires them.
- `tojson`, `fromjson`, `tostring`, `type`, `isnan`, `isinfinite`, and `have_decnum` are available.
- Serialization is compact and produces one complete JSON value per output.

## Programmatic Acceptance

=== AC values-json-roundtrip ===
Intent: The implementation passes the authoritative JSON, value, and serialization corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "tojson|fromjson|tostring|type|embedded NUL|NaN|nan|infinite"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC values-json-roundtrip ===

=== AC values-numeric-literals ===
Intent: The implementation passes the authoritative numeric literal and precision corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "decnum|literal numbers|large|precision|have_decnum"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC values-numeric-literals ===

=== AC values-type-boundaries ===
Intent: The implementation passes the authoritative type and Unicode value corpus slice.
Suite: scoped

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select",
     "type|utf8|Unicode|unicode|length"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC values-type-boundaries ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not introduce a third-party jq implementation or invoke a system jq binary.
- Preserve jq's distinction between booleans and numbers.
