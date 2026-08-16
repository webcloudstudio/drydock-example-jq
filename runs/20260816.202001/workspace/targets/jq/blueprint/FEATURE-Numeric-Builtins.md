# FEATURE: Numeric, Math, and Special-Number Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines jq numeric conversion, mathematical functions, predicates, and special-number behavior. |
| Depends On  | FEATURE-Operators.md, FEATURE-Core-Values.md |
| Provides    | tonumber, math functions, infinities, NaN, numeric predicates, have_decnum |
| Consumes    | numeric operators and JSON values |

## Intent

This feature implements jq's numeric library with Python standard-library math facilities. It
supports ordinary arithmetic, conversion, predicates, special values, and the corpus-required
literal-number behavior without third-party dependencies.

## Behavior

- `tonumber` accepts numbers and correctly formatted numeric strings.
- Standard one-, two-, and three-argument math functions use jq's filter calling convention.
- `infinite` and `nan` produce numeric special values; `isinfinite`, `isnan`, `isfinite`, and
  `isnormal` classify them.
- `have_decnum` follows the selected float-with-literal-metadata implementation behavior.
- Numeric comparisons distinguish numbers from booleans and preserve jq ordering.
- Arithmetic converts values according to jq's numeric semantics while unary negation preserves
  literal behavior required by the corpus.
- Invalid conversions and unsupported type combinations raise runtime errors.

## Programmatic Acceptance

=== AC numeric-builtins-suite ===
Intent: The supplied conformance corpus passes numeric, math, special-number, and literal-number cases owned by this feature.
Suite: scoped

import subprocess
import os

pattern = r"tonumber|have_decnum|infinite|nan|isnan|isinfinite|isfinite|isnormal|pow\\(|log|sqrt|floor|ceil|round|sin|cos|atan|fabs|numeric|literal|decnum"
result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
=== END AC numeric-builtins-suite ===

=== AC numeric-conversion ===
Intent: Numeric conversion accepts numbers and valid numeric strings.
import subprocess
import json

program = "[tonumber, tonumber]"
input_value = "\"12.5\"\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [12.5, 12.5]
assert actual == expected
=== END AC numeric-conversion ===

=== AC numeric-math ===
Intent: Standard mathematical filters produce numeric results.
import subprocess
import json

program = "[sqrt, floor, ceil]"
input_value = "9.7\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [3, 9, 10]
assert actual == expected
=== END AC numeric-math ===

=== AC numeric-predicates ===
Intent: Numeric predicates distinguish finite, infinite, and NaN values.
import subprocess
import json

program = "[infinite|isinfinite, nan|isnan, 1|isfinite]"
result = subprocess.run(["./jq", "-c", program], input="null\n", capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [[True, True, True]]
assert actual == expected
=== END AC numeric-predicates ===

=== AC invalid-number-conversion ===
Intent: Invalid numeric conversion produces the documented runtime exit status.
import subprocess

result = subprocess.run(
    ["./jq", "-c", "tonumber"],
    input="\"not-a-number\"\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 5
=== END AC invalid-number-conversion ===

## User Acceptance

- None.

## Guardrails

- Do not equate booleans with numbers.
- Do not introduce a third-party numeric or math dependency.
- Preserve the selected literal-number and `have_decnum` behavior consistently across parsing,
  comparison, arithmetic, and serialization.
