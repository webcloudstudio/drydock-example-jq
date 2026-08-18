# FEATURE: Regular-Expression Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provides jq regular-expression matching, capture, scanning, splitting, and replacement filters. |
| Depends On  | FEATURE-String-Builtins.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | string filters, generator evaluator |

## Purpose

Implement jq regular-expression builtins using Python's standard-library `re` module. Support jq flags, named and unnamed captures, Unicode codepoint offsets, global matching, stream-valued results, and replacement interpolation.

## Behavior

- `test` returns boolean match results.
- `match` emits match objects with offsets, lengths, strings, and captures.
- `capture` collects named captures into objects.
- `scan` emits matched strings or capture arrays.
- `split` emits one array; `splits` emits a stream.
- `sub` replaces the first match and `gsub` replaces all matches.
- Invalid input and invalid expressions raise jq runtime errors with exit status 5.
- Generator-valued replacement filters preserve output ordering.

## Programmatic Acceptance

=== AC regex-conformance ===
Intent: The implementation passes the authoritative corpus cases for regex matching, captures, scanning, splitting, and replacement.
Suite: scoped
Requires: executable=python3; scope=test

import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select",
     r"(^|[^A-Za-z])(test|match|capture|scan|split|splits|sub|gsub)\("],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC regex-conformance ===

=== AC regex-compile-status ===
Intent: Invalid regular-expression programs are rejected with the documented runtime failure status.
import subprocess

program = r'"x" | test("[")'
result = subprocess.run(["./jq", "-c", program], input="null\n", capture_output=True, text=True)
assert result.returncode == 5
=== END AC regex-compile-status ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not shell out to jq or use third-party regular-expression bindings.
