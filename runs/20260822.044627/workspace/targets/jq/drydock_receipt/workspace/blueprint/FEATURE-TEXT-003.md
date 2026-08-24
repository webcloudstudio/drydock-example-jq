# FEATURE: Regular-Expression Filters

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq regular-expression matching, capture, scanning, splitting, and substitution filters. |
| Depends On  | ARCHITECTURE.md, FEATURE-TEXT-002.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | jq strings, generator evaluator |

## Workflow

Implement the regex filters with Python's standard-library `re` module. Map the required jq flags, preserve Unicode codepoint offsets, emit named and unnamed capture structures, support global streams, and implement regex splitting and substitution with interpolation-aware replacement values.

## Programmatic Acceptance

=== AC text-003-regex-conformance ===
Intent: The authoritative corpus cases covering regular-expression filters execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"test\(|match\(|capture\(|scan\(|sub\(|gsub\(|splits\("
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
=== END AC text-003-regex-conformance ===

=== AC text-003-captures ===
Intent: The selected corpus includes matching, named capture, and replacement behavior.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"match\(|capture\(|sub\(|gsub\("
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
=== END AC text-003-captures ===

## User Acceptance

- None.

## Guardrails

- Use only the Python standard library for regular expressions.
- Preserve generator multiplicity and output ordering for global matches and replacement streams.
