# FEATURE: Core Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq arithmetic, type-directed operators, comparisons, boolean logic, and alternatives. |
| Depends On  | ARCHITECTURE.md, FEATURE-Core-Values.md |
| Provides    | arithmetic, concatenation, merge, equality, ordering, boolean, alternative, optional operators |
| Consumes    | generator evaluator, jq values |

## Intent

This feature implements jq's numeric, string, array, object, and null-aware operators; recursive merge; equality and ordering; boolean operators; defined-or; unary negation; and operator error behavior.

## Programmatic Acceptance

=== AC core-operators-conformance ===
Intent: The interpreter passes the authoritative corpus cases covering jq operators and comparisons.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"(^|[^\w])(?:\+|-|\*|/|%|==|!=|<=|>=|//|and|or)(?:$|[^\w])|(?:\+=|-=|\*=|/=|%=|//=)"
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
=== END AC core-operators-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not coerce incompatible jq types implicitly.
- Preserve jq truthiness: only false and null are false-valued.
- Preserve ordered generator evaluation and partial output before runtime errors.
