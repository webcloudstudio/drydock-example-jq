# FEATURE: Regular-Expression Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provide jq-compatible regular-expression matching, capture, scanning, splitting, and substitution filters. |
| Depends On  | FEATURE-BUILTINS-002.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | string builtins, generator evaluation |

## Purpose

Implement jq regular-expression builtins using Python standard-library facilities. Support jq pattern and flag arguments, global matching, named and unnamed captures, Unicode codepoint offsets, regex splitting, and substitution streams.

## Behavior

- `test` emits Boolean match results.
- `match` emits match objects with offset, length, string, and captures.
- `capture` collects named captures into an object.
- `scan` emits matching strings or capture arrays.
- `split` and `splits` support jq's string and regex forms.
- `sub` and `gsub` support interpolation against named captures and generator-valued replacements.
- Invalid regular-expression inputs raise jq runtime errors and preserve prior generator output.

## Programmatic Acceptance

=== AC builtins-003-regex ===
Intent: The authoritative corpus slice covering regex matching, captures, scanning, splitting, and substitution executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"test\(|match\(|capture\(|scan\(|sub\(|gsub\("
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
=== END AC builtins-003-regex ===

=== AC builtins-003-regex-split ===
Intent: The authoritative corpus slice containing regex split and substitution streams passes with no failed or errored cases.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"split\(|splits\(|sub\(|gsub\("
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
=== END AC builtins-003-regex-split ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library regular-expression facilities.
- Do not shell out to jq or use a third-party regex or jq implementation.
- Preserve generator ordering and output values produced before runtime errors.
