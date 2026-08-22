# FEATURE: Labels and Breaks

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements lexically scoped labels and generator termination through break expressions. |
| Depends On  | FEATURE-Declarations-And-Control-Syntax.md, FEATURE-Errors-And-Optional-Evaluation.md, FEATURE-Conditionals-And-Exception-Flow.md |
| Provides    | label, break |
| Consumes    | parsed declarations, runtime error flow, generator core |

## Intent

Implement jq's lexical `label $name | ... break $name ...` control mechanism. A break terminates the matching enclosing generator and behaves as though that label expression produced `empty`.

## Behavior

- Labels bind only within their lexical body.
- `break $name` terminates the nearest visible matching label.
- Outputs produced before the break are retained in order.
- Breaks do not leak into unrelated generators or labels.
- A break without a visible label is rejected at compile time.
- Labels and breaks work inside iteration, reductions, conditionals, and nested pipelines.

## Programmatic Acceptance

=== AC flow-004-conformance ===
Intent: The labels and breaks implementation passes every selected conformance case containing label or break syntax.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"label|break"
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
=== END AC flow-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Enforce lexical visibility during compilation.
- Terminate only the matching label scope.
- Preserve outputs emitted before termination and generator ordering.
