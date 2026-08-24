# FEATURE: Function Definitions and Recursion

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq function declarations, lexical function scope, and recursion. |
| Depends On  | ARCHITECTURE.md, FEATURE-FUNC-002.md |
| Provides    | def declarations, lexical function scope, redefinition, recursion, forward/self references |
| Consumes     | function parameters, lexical variable bindings |

## Workflow

Function definitions introduce named filters into lexical scope and support recursive evaluation.

- `def name: FILTER;` defines a zero-arity function.
- Parameterized definitions support filter and value parameters.
- Definitions are resolved lexically and may refer to themselves recursively.
- Redefinition replaces only the matching arity for subsequent references.
- Function calls preserve generator ordering, closures, and backtracking.

## Programmatic Acceptance

=== AC func-003-conformance ===
Intent: The executable passes the authoritative conformance cases exercising function definitions, scope, redefinition, and recursion.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"def "
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
=== END AC func-003-conformance ===

## User Acceptance

- Recursive and redefined functions resolve according to jq's lexical scoping rules.

## Guardrails

- Do not resolve function names through mutable global state.
- Preserve self-reference, recursion, and generator backtracking.
