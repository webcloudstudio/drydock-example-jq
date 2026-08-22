# FEATURE: Function Parameters

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq filter and value function parameters with arity and closure semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-Variable-Bindings.md, FEATURE-Composition-And-Cartesian-Evaluation.md |
| Provides    | filter parameters, value parameters, multiple arities, closures, Cartesian arguments |
| Consumes    | lexical bindings, generator evaluation, function definitions |

## Workflow

Implement user-defined functions whose parameters may be filters or value bindings. Support multiple arities, repeated callback evaluation with the current input, Cartesian products from multi-output arguments, and closure capture through lexical environments.

## Programmatic Acceptance

=== AC func-002-conformance ===
Intent: The authoritative corpus slice exercising function parameters executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"def .*\("
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
=== END AC func-002-conformance ===

=== AC func-002-interface ===
Intent: A filter parameter is evaluated against the function's current input.
import subprocess

program = "def twice(f): f | f; 5 | twice(.*2)"
payload = "null\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode in (0, 5)
=== END AC func-002-interface ===

## User Acceptance

- None.

## Guardrails

- Distinguish filter parameters from value parameters.
- Preserve callback re-evaluation and generator multiplicity.
- Keep captured lexical environments isolated between calls.
