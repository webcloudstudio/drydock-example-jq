# FEATURE: Date and Time Filters

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide UTC date parsing, formatting, and low-level time conversion filters. |
| Depends On  | ARCHITECTURE.md, FEATURE-TEXT-003.md |
| Provides    | fromdate, todate, strptime, strftime, strflocaltime, gmtime, localtime, mktime |
| Consumes    | jq strings and numbers |

## Workflow

Implement the documented date and time filters with Python's standard-library `datetime` and `time` facilities. ISO-8601 convenience filters operate in UTC; low-level conversions preserve jq's broken-down time-array shape and accept the supplied format strings.

## Programmatic Acceptance

=== AC text-004-date-conformance ===
Intent: The authoritative corpus cases covering date and time filters execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"date|strftime|strptime|strflocaltime|gmtime|localtime|mktime"
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
=== END AC text-004-date-conformance ===

=== AC text-004-utc ===
Intent: The selected corpus exercises both ISO convenience filters and low-level UTC conversions.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"fromdate|todate|strptime|strftime|gmtime|mktime"
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
=== END AC text-004-utc ===

## User Acceptance

- None.

## Guardrails

- Date operations must use standard-library facilities and must not depend on the local timezone for UTC filters.
- Do not introduce wall-clock-dependent acceptance expectations.
