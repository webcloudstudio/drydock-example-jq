# FEATURE: Regular Expressions

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq regular-expression matching, scanning, splitting, and substitution filters. |
| Depends On  | FEATURE-String-Manipulation.md, FEATURE-Literals-And-Interpolation.md, FEATURE-Composition-And-Cartesian-Evaluation.md |
| Provides    | test, match, capture, scan, split, splits, sub, gsub |
| Consumes    | string values, interpolation, generator evaluation |

## Intent

Implement the regex filter family with Python standard-library regular expressions. Support required flags, named and unnamed captures, Unicode code-point offsets and lengths, streams, splitting, substitution, and global substitution.

## Programmatic Acceptance

=== AC text-003-conformance ===
Intent: The implementation passes the authoritative regular-expression corpus slice.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"test\(|match\(|capture\(|scan\(|sub\(|gsub\("
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
=== END AC text-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only standard-library regex facilities.
- Preserve stream multiplicity and match ordering.
- Never compare or gate on diagnostic wording.
