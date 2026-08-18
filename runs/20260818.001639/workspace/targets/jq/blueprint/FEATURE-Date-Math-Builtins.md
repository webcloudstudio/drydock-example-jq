# FEATURE: Date and Math Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provides jq date conversion, time decomposition, mathematical, and floating-point helper builtins. |
| Depends On  | FEATURE-Arithmetic-Comparison.md, FEATURE-String-Builtins.md |
| Provides    | date/time builtins, math builtins, numeric predicates |
| Consumes    | arithmetic and string evaluation |

## Purpose

Implement jq's UTC date interfaces, time-structure conversions, standard mathematical functions, and special-number predicates using the Python standard library.

## Behavior

- Support `fromdate`, `todate`, `fromdateiso8601`, and `todateiso8601`.
- Support `strptime`, `strftime`, `strflocaltime`, `mktime`, `gmtime`, and `localtime`.
- Provide standard one-, two-, and three-argument math functions exposed by the corpus.
- Provide `infinite`, `nan`, `isinfinite`, `isnan`, `isfinite`, and `isnormal`.
- Preserve jq numeric conversion and error behavior.
- Time calculations use UTC where jq specifies UTC.

## Programmatic Acceptance

=== AC date-math-conformance ===
Intent: The implementation passes the authoritative corpus cases for date, time, mathematical, and floating-point builtins.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select",
     r"(^|[^A-Za-z])(fromdate|todate|strptime|strftime|strflocaltime|mktime|gmtime|localtime|now|infinite|nan|isfinite|isnormal|isnan|isinfinite|acos|asin|atan|ceil|cos|exp|fabs|floor|log|round|sin|sqrt|tan|trunc)\b"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC date-math-conformance ===

=== AC date-runtime-status ===
Intent: Invalid date input produces the documented runtime failure status.
import subprocess

program = r'fromdate'
result = subprocess.run(["./jq", "-c", program], input="null\n", capture_output=True, text=True)
assert result.returncode == 5
=== END AC date-runtime-status ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library date and math facilities.
- Do not make acceptance dependent on wall-clock output from `now`.
