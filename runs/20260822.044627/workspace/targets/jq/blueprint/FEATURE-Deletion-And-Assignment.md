# FEATURE: Deletion And Assignment

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq deletion, plain assignment, update assignment, and arithmetic assignment. |
| Depends On  | FEATURE-Path-Primitives.md, FEATURE-Arithmetic-And-Structural-Operators.md, FEATURE-Boolean-And-Alternative-Operators.md |
| Provides    | del, =, |=, +=, -=, *=, /=, %=, //= |
| Consumes    | Path primitives, arithmetic operators, generator evaluation |

## Purpose

Implement jq's immutable path-based mutation operators and deletion behavior.

## Implementation Requirements

- Implement `del(path-expression)`.
- Implement plain assignment with all values produced by the right-hand side.
- Implement update assignment using the selected path value as the update input.
- Implement arithmetic and defined-or assignment operators.
- Support multiple paths and generator-valued left-hand sides.
- Delete paths when an update expression produces `empty`.
- Preserve the original input for sibling expressions evaluated after an assignment.
- Use the first update result for `|=` as specified.

## Programmatic Acceptance

=== AC deletion-assignment-conformance ===
Intent: The authoritative corpus slice covering deletion and assignment operators executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\bdel\(|\|=|\+=|-=|\*=|/=|%=|//="
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
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
=== END AC deletion-assignment-conformance ===

## User Acceptance

- None.

## Guardrails

- Treat jq values as immutable.
- Do not apply plain-assignment RHS filters to the selected path value.
- Do not use the last update result for `|=`.
- Do not leak mutations into sibling outputs or later evaluations of the original input.
