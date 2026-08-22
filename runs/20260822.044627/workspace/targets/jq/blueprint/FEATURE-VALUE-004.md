# FEATURE: Type and Numeric Primitives

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq type, length, numeric conversion, predicate, and math primitives. |
| Depends On  | ARCHITECTURE.md, FEATURE-VALUE-001.md, FEATURE-VALUE-003.md |
| Provides    | type, length, utf8bytelength, numeric predicates, conversions, math builtins |
| Consumes    | jq value model, ordered generator evaluator |

## Intent

Implement `type`, `length`, `utf8bytelength`, numeric predicates, `tonumber`, `toboolean`, `tostring`, and the standard math functions exercised by the corpus. Preserve jq's stream behavior, numeric equivalence, Unicode codepoint semantics, and runtime errors for invalid input types.

## Programmatic Acceptance

=== AC value-004-conformance ===
Intent: The implementation passes the authoritative corpus slice covering type, length, numeric predicates, conversions, and math functions.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"length|type|sqrt|floor|tonumber"
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
=== END AC value-004-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Preserve jq's distinction between booleans and numbers.
- Do not replace authoritative corpus verification with hand-picked examples.
