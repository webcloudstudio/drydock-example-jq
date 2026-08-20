# FEATURE: Control Bindings

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Defines lexical variable bindings, destructuring patterns, and binding alternatives. |
| Depends On | FEATURE-Control-Reductions.md |
| Provides | `as` bindings, lexical variables, array and object patterns, `?//` alternatives |
| Consumes | generator evaluation, filter scope, pattern matching |

## Purpose

Implement jq's lexical binding model, including scalar bindings, destructuring, lexical scope, shadowing, alternatives, generator-valued expressions, and error propagation.

## Programmatic Acceptance

=== AC control-bindings-conformance ===
Intent: The scoped authoritative corpus cases covering bindings, patterns, lexical scope, and destructuring alternatives execute and pass.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"( as \$|\?//|\[\$|\{\$)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC control-bindings-conformance ===

## User Acceptance

- None.

## Guardrails

- Variable bindings must not leak outside their lexical scope.
- Destructuring alternatives must preserve generator ordering and final-error behavior.
- No third-party runtime dependency may be introduced.
