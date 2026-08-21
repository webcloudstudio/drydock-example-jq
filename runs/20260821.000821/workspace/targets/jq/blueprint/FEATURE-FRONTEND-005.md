# FEATURE: Destructuring and Alternative Patterns

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Support jq destructuring patterns and fallback alternatives. |
| Depends On  | FEATURE-FRONTEND-004.md |
| Provides    | array patterns, object patterns, missing bindings, ?// alternatives |
| Consumes    | jq parser, lexical bindings, generator runtime |

## Scope

Implement array and object patterns, null bindings for missing members, repeated alternative patterns, and fallback when a pattern or downstream expression fails.

## Programmatic Acceptance

=== AC frontend-005-patterns ===
Intent: The implementation passes the executing conformance cases for array and object destructuring.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r" as \$| as \["
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
=== END AC frontend-005-patterns ===

=== AC frontend-005-alternatives ===
Intent: The implementation passes the executing conformance cases for ?// alternative destructuring.
Suite: scoped

import json
import os
import subprocess
import sys

selector = r"\?//"
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
=== END AC frontend-005-alternatives ===

## User Acceptance

- None.

## Guardrails

- Missing pattern members bind to null.
- Alternative patterns must preserve bindings from the successful branch only.
- Downstream errors must trigger the next alternative where jq specifies that behavior.
