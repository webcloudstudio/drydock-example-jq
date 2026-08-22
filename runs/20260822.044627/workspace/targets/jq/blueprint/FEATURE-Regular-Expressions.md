# FEATURE: Regular Expressions

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq regular-expression matching and substitution filters. |
| Depends On  | FEATURE-Output-Formats.md |
| Provides    | test, match, capture, scan, splits, regex split, sub, gsub |
| Consumes    | string manipulation builtins |

## Intent

Implement the standard-library regular-expression surface required by the corpus, including supported flags, named and unnamed captures, Unicode offsets, streaming scans, splitting, and substitutions.

## Programmatic Acceptance

=== AC text-003-conformance ===
Intent: The authoritative corpus cases covering regular-expression filters pass.
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC text-003-conformance ===

=== AC text-003-execution ===
Intent: The regex selector executes a non-empty corpus slice through jq.
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
report = json.loads(result.stdout)
assert report["summary"]["pass"] > 0
assert result.returncode == 0
=== END AC text-003-execution ===

## User Acceptance

- None.

## Guardrails

- Use only the Python standard library.
- Preserve generator multiplicity and match ordering.
- Keep diagnostics on stderr and do not alter staged sources.
