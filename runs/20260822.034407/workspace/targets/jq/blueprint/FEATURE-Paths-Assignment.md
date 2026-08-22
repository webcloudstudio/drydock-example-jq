# FEATURE: Paths Assignment

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq plain, update, arithmetic, and defined-or assignments. |
| Depends On  | FEATURE-Paths-Mutation.md |
| Provides    | =, |=, +=, -=, *=, /=, %=, //= |
| Consumes    | path mutation and deletion |

## Intent

This feature implements generator-based left-hand-side path selection, plain and update assignments, arithmetic assignment operators, defined-or assignment, immutable results, deletion on empty updates, and correct right-hand-side evaluation.

## Programmatic Acceptance

=== AC paths-assignment-conformance ===
Intent: The interpreter passes the authoritative corpus cases covering jq assignment operators and generator-produced path updates.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"(?:^|[^\w])(?:\|=|\+=|-=|\*=|/=|%=|//=|=)(?:$|[^\w])"
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
=== END AC paths-assignment-conformance ===

## User Acceptance

- None.

## Guardrails

- Assignment results must be immutable snapshots.
- Plain assignment must use the original input for RHS evaluation.
- Update assignment must use the selected path value and only the first RHS output.
- Empty update streams must delete the selected path.
