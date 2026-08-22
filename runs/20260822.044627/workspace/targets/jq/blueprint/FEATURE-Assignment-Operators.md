# FEATURE: Deletion and Assignment Operators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implements jq deletion, plain assignment, update assignment, and arithmetic assignment. |
| Depends On  | FEATURE-Path-Primitives.md |
| Provides    | del, =, |=, arithmetic assignments, defined-or assignment |
| Consumes    | getpath, setpath, delpaths |

## Scope

Implement immutable deletion and assignment over exact and iterated path expressions. Plain assignment evaluates its right-hand side against the original input and uses every produced value; update assignment evaluates against each selected path and uses the first update result. Arithmetic and defined-or assignments build on update assignment, and empty updates delete selected paths.

## Programmatic Acceptance

=== AC path-003-conformance ===
Intent: Deletion, plain assignment, update assignment, and arithmetic assignment preserve immutable jq semantics.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "del(.obsolete), (.count = 2), (.count |= . + 3), (.count += 4)"],
    input='{"count":1,"obsolete":true}\n',
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [
    {"count": 1},
    {"count": 2, "obsolete": True},
    {"count": 4, "obsolete": True},
    {"count": 5, "obsolete": True},
]
assert actual == expected
=== END AC path-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Assignments must preserve jq's immutable snapshot semantics.
- Multi-path and generator-valued assignments must preserve output multiplicity and order.
