# FEATURE: Deletion and Assignment Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq deletion and assignment operators over path expressions. |
| Depends On  | FEATURE-PATH-002.md |
| Provides    | del, =, |=, +=, -=, *=, /=, %=, //=
| Consumes    | path discovery, getpath, setpath, delpaths |

## Purpose

Implement jq's immutable deletion, plain assignment, update assignment, and arithmetic assignment semantics.

## Behavior

- `del` removes values selected by one or more path expressions.
- Plain assignment evaluates the right-hand side against the original input and uses every produced value.
- Update assignment evaluates the right-hand side against each selected value and uses the first result.
- Arithmetic assignments apply the corresponding operator to selected values.
- Defined-or assignment replaces false or null values with the right-hand result.
- Multi-path assignments preserve jq's output ordering and multiplicity.

## Programmatic Acceptance

=== AC path-003-conformance ===
Intent: The authoritative corpus slice covering deletion and assignment operators executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"=|\|=|\+="
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
=== END AC path-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Assignment must produce immutable values and must not leak mutations between outputs.
- Preserve the distinction between `=` and `|=`.
- Empty update streams delete the selected path.
