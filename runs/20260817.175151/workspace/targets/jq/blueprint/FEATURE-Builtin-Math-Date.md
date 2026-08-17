# FEATURE: Builtin Math Date

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq mathematical, numeric-special-value, and UTC date builtins. |
| Depends On  | FEATURE-Core-Values-Operators.md |
| Provides    | math functions, special numbers, date parsing and formatting, epoch conversion |
| Consumes    | jq number semantics |

## Behavior

The interpreter implements standard mathematical functions, floating-point edge cases, NaN and infinity predicates, and jq date functions including `strptime`, `strftime`, `mktime`, `gmtime`, `fromdate`, and `todate` in UTC. Numeric handling follows the recorded native-float decision while preserving required literal behavior.

## Programmatic Acceptance

=== AC math-functions ===
Intent: A supplied numeric input is transformed by jq math functions with the expected Python-computable result.
import json
import math
import subprocess

value = 9.0
expected = math.sqrt(value)
result = subprocess.run(
    ["./jq", "-c", "sqrt"],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC math-functions ===

=== AC math-special-values ===
Intent: Special numeric values are recognized by jq predicates.
import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", '[infinite | isinfinite, nan | isnan]'],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == [True, True]
=== END AC math-special-values ===

=== AC date-roundtrip ===
Intent: A supplied ISO UTC date round-trips through jq epoch conversion.
import json
import subprocess

value = "2015-03-05T23:51:47Z"
result = subprocess.run(
    ["./jq", "-c", "fromdateiso8601 | todateiso8601"],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC date-roundtrip ===

=== AC date-epoch ===
Intent: UTC epoch conversion is consistent with the supplied parsed date.
import json
import subprocess
import datetime

value = "1970-01-01T00:00:00Z"
expected = int(datetime.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())
result = subprocess.run(
    ["./jq", "-c", "fromdateiso8601"],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == expected
=== END AC date-epoch ===

## User Acceptance

- None.

## Guardrails

- Date calculations use UTC where jq specifies UTC and introduce no external dependency.
