# FEATURE: Destructuring Patterns and Alternatives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq destructuring patterns and alternative bindings. |
| Depends On  | FEATURE-FUNC-003.md |
| Provides    | array patterns, object patterns, missing bindings, ?// alternatives |
| Consumes    | lexical bindings, function evaluator |

## Purpose

Support array and object destructuring in `as` bindings, bind absent members as `null`, and backtrack through `?//` alternatives when a pattern or subsequent expression fails.

## Behavior

- Array patterns bind positional elements and use `null` for missing positions.
- Object patterns bind named fields and nested patterns.
- Alternative patterns try later alternatives when an earlier binding fails.
- Variables introduced by successful alternatives remain available to the following filter.
- Errors from the final alternative propagate as runtime errors.

## Programmatic Acceptance

=== AC func-004-conformance ===
Intent: The authoritative corpus slice covering destructuring patterns and alternative bindings executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\?//| as \{"
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
=== END AC func-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve lexical scope and generator backtracking.
- Do not silently convert a final alternative error into a successful value.
