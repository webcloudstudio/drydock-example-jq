# FEATURE: Conditionals and Exception Flow

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq conditional branching, try/catch handling, and optional error suppression. |
| Depends On  | FEATURE-Errors-And-Optional-Evaluation.md, FEATURE-Truthiness-And-Comparison.md, FEATURE-Boolean-And-Alternative-Operators.md |
| Provides    | if/then/elif/else/end, try/catch, optional filter operator |
| Consumes    | jq truthiness, runtime error flow, generator evaluation |

## Intent

Implement control flow over jq generator streams. Conditions may produce multiple values, and each truthy or falsey result selects its corresponding branch independently.

## Behavior

- `if A then B else C end` evaluates branches for each output of `A`.
- Missing `else` defaults to identity.
- `elif` chains preserve jq branch ordering and fallback behavior.
- `try EXP catch HANDLER` catches runtime errors and evaluates the handler with the error value.
- `try EXP` suppresses errors and produces no replacement output.
- `EXP?` is equivalent to `try EXP`.
- Outputs produced before an uncaught runtime error remain available to the process boundary.

## Programmatic Acceptance

=== AC flow-003-conformance ===
Intent: The conditional and exception-flow implementation passes every selected conformance case containing the owned syntax.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\bif\b|\btry\b|\?"
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
=== END AC flow-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve partial output before runtime failure.
- Catch only runtime errors within the protected expression.
- Keep compile failures distinct from runtime failures.
