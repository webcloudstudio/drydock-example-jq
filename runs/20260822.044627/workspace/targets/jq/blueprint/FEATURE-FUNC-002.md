# FEATURE: Function Parameters

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq filter parameters, value parameters, and multi-arity calls. |
| Depends On  | ARCHITECTURE.md, FEATURE-FUNC-001.md |
| Provides    | filter parameters, value parameters, function arities, Cartesian function calls |
| Consumes    | lexical variable bindings, generator evaluator |

## Workflow

User-defined functions accept filter parameters as reusable generators and value parameters as captured values.

- Regular identifiers in parameter lists represent filter parameters.
- `$`-prefixed parameters represent value parameters.
- Arguments preserve jq's generator and Cartesian-product semantics.
- Functions support multiple arities and repeated parameter invocation.
- Closures retain the lexical environment active at definition and call sites.

## Programmatic Acceptance

=== AC func-002-conformance ===
Intent: The executable passes the authoritative conformance cases exercising filter and value function parameters.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"def .*\("
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
tally = report["summary"]
assert sum(tally.values()) > 0
assert tally["fail"] == 0 and tally["error"] == 0
assert result.returncode == 0
=== END AC func-002-conformance ===

## User Acceptance

- Function arguments behave as filters or values according to their declaration form.

## Guardrails

- Do not eagerly collapse filter arguments to one value.
- Preserve repeated invocation and Cartesian output behavior.
