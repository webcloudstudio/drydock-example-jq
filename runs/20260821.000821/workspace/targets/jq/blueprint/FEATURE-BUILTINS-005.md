# FEATURE: Date and Mathematics Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provide jq date, time, mathematical, and numeric-predicate builtins. |
| Depends On  | FEATURE-BUILTINS-004.md |
| Provides    | date conversion, time decomposition, math functions, numeric predicates |
| Consumes    | core numeric operators, format and JSON conversions |

## Purpose

Implement UTC date parsing and formatting, broken-down time conversion, standard mathematical functions, infinities, NaN, and numeric predicates using Python's standard library.

## Behavior

- ISO date conversion and low-level time filters use UTC semantics.
- `gmtime`, `mktime`, `strptime`, `strftime`, and related filters preserve jq-compatible broken-down time fields.
- Standard one-, two-, and three-argument mathematical functions evaluate numeric inputs.
- `infinite`, `nan`, `isinfinite`, `isnan`, `isfinite`, and `isnormal` follow jq numeric behavior.
- Invalid numeric or time inputs raise runtime errors.

## Programmatic Acceptance

=== AC builtins-005-date ===
Intent: The authoritative corpus slice covering date and time conversion executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"date|strftime|strptime|mktime|gmtime"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC builtins-005-date ===

=== AC builtins-005-math ===
Intent: The authoritative corpus slice covering mathematical functions and numeric predicates executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"pow\(|sin|cos|sqrt|floor|infinite|nan|isfinite|isnan|isnormal"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC builtins-005-math ===

## User Acceptance

- None.

## Guardrails

- Use UTC for jq date functions whose specification requires UTC.
- Use only Python standard-library time and math facilities.
- Preserve jq runtime error behavior for invalid dates, formats, and numeric inputs.
