# FEATURE: Builtins Numeric

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Provide date, mathematics, numeric conversion, and special-value jq builtins. |
| Depends On | FEATURE-Builtins-Regex.md |
| Provides | date, time, math, numeric, infinity, NaN, decnum builtins |
| Consumes | jq generator evaluator, jq value and comparison semantics |

## Scope

This feature implements date and time conversion, `strptime`, `strftime`, `mktime`, standard mathematical functions, numeric conversion, infinities, NaN, numeric comparison, literal preservation, and `have_decnum` behavior.

## Programmatic Acceptance

=== AC builtins-numeric-conformance ===
Intent: The numeric and date builtin corpus slice executes and passes with at least one selected case.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(date|time|strftime|strptime|mktime|sin|cos|sqrt|pow|nan|infinite|decnum|tonumber)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC builtins-numeric-conformance ===

## User Acceptance

- Numeric behavior follows the supplied jq specification and corpus.

## Guardrails

- Use only Python standard-library functionality; do not add numeric or date dependencies.
- Do not modify staged scoring assets.
