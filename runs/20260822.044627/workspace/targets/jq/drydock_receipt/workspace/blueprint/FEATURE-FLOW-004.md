# FEATURE: Labels and Breaks

| Field       | Value |
|-------------|-------|
| Version     | 20220822 V1 |
| Description | Provide lexically scoped jq labels and break control flow. |
| Depends On  | ARCHITECTURE.md, FEATURE-FLOW-003.md |
| Provides    | label and break control flow |
| Consumes    | ordered generator evaluator, runtime error model |

## Intent

Implement `label $name | ...` and `break $name` with lexical scope. A break must terminate only its corresponding enclosing generator, suppress subsequent outputs from that scope, and compile-fail when no visible label exists.

## Programmatic Acceptance

=== AC flow-004-conformance ===
Intent: The implementation passes the authoritative corpus slice covering labels and breaks.
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC flow-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Labels are lexical, not dynamically resolved.
- Break must not leak outputs from the terminated generator.
- Reject undefined labels at compile time with exit code 3.
