# FEATURE: Index And Membership Utilities

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq index search, binary search, quantifier, emptiness, and SQL-style membership utilities. |
| Depends On  | FEATURE-Truthiness-And-Comparison.md, FEATURE-Reductions-And-Iteration-Control.md, FEATURE-Object-Entries-And-Containment.md |
| Provides    | indices, index, rindex, bsearch, all, any, isempty, IN |
| Consumes    | comparison semantics, generator evaluator |

## Workflow

Implement substring and contiguous-array index searches, binary search over sorted arrays, short-circuiting `all` and `any`, emptiness detection, and SQL-style `IN` forms. Preserve generator behavior and avoid evaluating unnecessary values after a decisive quantifier result.

## Programmatic Acceptance

=== AC data-004-conformance ===
Intent: The authoritative corpus slice covering index, membership, quantifier, and emptiness utilities executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"indices|index\(|rindex|bsearch|any|all|IN\("
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
=== END AC data-004-conformance ===

## User Acceptance

- None.

## Guardrails

- `all` and `any` must preserve jq truthiness and short-circuit behavior.
- Array searches require contiguous structural matches.
- Do not coerce unrelated jq types during membership checks.
