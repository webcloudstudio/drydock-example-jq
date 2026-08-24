# FEATURE: Conditionals and Exception Flow

| Field       | Value |
|-------------|-------|
| Version     | 20220822 V1 |
| Description | Provide jq conditional branching, try/catch handling, and optional evaluation. |
| Depends On  | ARCHITECTURE.md, FEATURE-FLOW-002.md |
| Provides    | if, then, elif, else, try, catch, optional control flow |
| Consumes    | ordered generator evaluator, runtime error model |

## Intent

Implement `if`/`then`/`elif`/`else`/`end`, `try`/`catch`, and the `?` optional operator. Branches must run once per condition output, preserve generator ordering, suppress only the errors requested by the filter, and retain outputs produced before an uncaught runtime error.

## Programmatic Acceptance

=== AC flow-003-conformance ===
Intent: The implementation passes the authoritative corpus slice covering conditionals, try/catch, and optional evaluation.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"if |try |\?"
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
=== END AC flow-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Keep compile failures distinct from runtime failures.
- Do not compare or normalize diagnostic text as a correctness oracle.
- Preserve partial stdout output before runtime failure.
