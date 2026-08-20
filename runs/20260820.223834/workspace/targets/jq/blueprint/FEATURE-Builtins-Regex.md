# FEATURE: Builtins Regex

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Defines jq regular-expression matching, captures, scanning, splitting, and substitution. |
| Depends On | FEATURE-Builtins-Strings.md |
| Provides | `test`, `match`, `capture`, `scan`, `split`, `splits`, `sub`, `gsub` |
| Consumes | string transforms, generator evaluation, interpolation |

## Purpose

Implement jq regular-expression builtins with Python's standard-library regular-expression support, including matching, captures, scanning, splitting, substitution, Unicode offsets, and generator-valued replacement filters.

## Programmatic Acceptance

=== AC builtins-regex-conformance ===
Intent: The scoped authoritative corpus cases covering regex matching, captures, scanning, splitting, and substitution execute and pass.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(test|match|capture|scan|sub|gsub|splits)"
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
=== END AC builtins-regex-conformance ===

## User Acceptance

- None.

## Guardrails

- Regex behavior must remain within Python standard-library capabilities.
- Match offsets must be measured in Unicode codepoints as required by jq.
- Global matches must preserve order and non-overlap.
- Replacement expressions must preserve jq generator semantics.
- No third-party regex engine or jq binding may be introduced.
