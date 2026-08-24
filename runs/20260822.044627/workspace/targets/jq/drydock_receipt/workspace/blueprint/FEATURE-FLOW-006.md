# FEATURE: Recursive Generator Primitives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq recursive generator and recursive-descent primitives. |
| Depends On  | ARCHITECTURE.md, FEATURE-FLOW-005.md |
| Provides    | while, until, repeat, recurse, recursive descent |
| Consumes    | ordered generator evaluator, runtime error model |

## Workflow

Recursive generators repeatedly apply filters while preserving jq stream order and termination behavior.

- `while(cond; update)` emits each qualifying value before continuing.
- `until(cond; next)` continues until its condition succeeds.
- `repeat(exp)` continues until the expression raises an error.
- `recurse` emits the current value and recursively generated descendants.
- `..` provides recursive descent equivalent to zero-argument `recurse`.

## Programmatic Acceptance

=== AC flow-006-conformance ===
Intent: The executable passes the authoritative conformance cases exercising recursive generators and recursive descent.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"while|until|recurse|repeat"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
tally = report["summary"]
assert sum(tally.values()) > 0
assert tally["fail"] == 0 and tally["error"] == 0
assert result.returncode == 0
=== END AC flow-006-conformance ===

## User Acceptance

- Recursive filters terminate and preserve the documented depth-first output order.

## Guardrails

- Do not introduce incorrect termination for generators that intentionally produce repeated values.
- Preserve runtime error behavior for `repeat`.
