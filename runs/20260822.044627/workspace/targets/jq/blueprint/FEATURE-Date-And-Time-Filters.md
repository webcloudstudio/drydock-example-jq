# FEATURE: Date and Time Filters

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implement jq date conversion and broken-down time filters. |
| Depends On  | FEATURE-Type-And-Numeric-Primitives.md, FEATURE-String-Manipulation.md |
| Provides    | fromdate, todate, fromdateiso8601, todateiso8601, strptime, strftime, strflocaltime, gmtime, localtime, mktime |
| Consumes    | numeric values, strings, standard-library date and time facilities |

## Intent

Implement the supplied UTC ISO-8601 conversions and low-level date/time filters. Represent broken-down times in jq's documented array form and preserve the standard-library behavior required by the corpus.

## Programmatic Acceptance

=== AC text-004-conformance ===
Intent: The implementation passes the authoritative date and time corpus slice.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"\b(date|strftime|strptime|gmtime|localtime|mktime|fromdate|todate)\b"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC text-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Date operations must not require network access or third-party packages.
- UTC behavior must remain deterministic for ISO conversions.
- Do not modify the supplied corpus or harness.
