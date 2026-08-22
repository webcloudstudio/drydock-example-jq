# FEATURE: Boolean and Alternative Operators

| Field       | Value |
|-------------|-------|
| Version     | 20220822 V1 |
| Description | Provide jq Boolean, negation, defined-or, and defined-or assignment operators. |
| Depends On  | ARCHITECTURE.md, FEATURE-FLOW-001.md |
| Provides    | and, or, not, defined-or, defined-or assignment |
| Consumes    | ordered generator evaluator, truthiness and comparison |

## Intent

Implement `and`, `or`, `not`, `//`, and `//=` with jq truthiness and generator-aware short-circuiting. False and null are falsey; all other values are truthy. Alternative expressions must emit all valid left-hand outputs or fall back to the right-hand generator.

## Programmatic Acceptance

=== AC flow-002-conformance ===
Intent: The implementation passes the authoritative corpus slice covering Boolean and alternative operators.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"and|or|not|//"
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
=== END AC flow-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not use host-language truthiness in place of jq truthiness.
- Preserve ordering and multiplicity of generator outputs.
- Preserve short-circuit behavior where required.
