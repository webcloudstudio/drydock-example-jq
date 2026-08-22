# FEATURE: Accessors

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines object-field access, array indexing, optional access, and negative-index behavior. |
| Depends On  | FEATURE-Value-Model.md |
| Provides    | object fields, array indices, optional access, negative indices |
| Consumes    | jq value model |

## Access Semantics

Object fields return the matching value or null when absent. Array indices are zero-based and support negative indices. Invalid access raises a jq runtime error unless the expression is optional, in which case the error is suppressed according to jq semantics.

## Programmatic Acceptance

=== AC value-002-conformance ===
Intent: Field access, negative indexing, and optional access produce the supplied jq behavior.
Requires: executable=python3; scope=test

import json
import subprocess

payload = '{"field":[10,20,30]}\n'
result = subprocess.run(
    ["./jq", "-c", ".field[-1], .missing?, .field[0]"],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [30, None, 10]
assert actual == expected
=== END AC value-002-conformance ===

=== AC value-002-access-contract ===
Intent: Field access, negative indexing, and optional access produce the supplied jq behavior.
Requires: executable=python3; scope=test

import json
import subprocess

payload = '{"field":[10,20,30]}\n'
result = subprocess.run(
    ["./jq", "-c", ".field[-1], .missing?, .field[0]"],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [30, None, 10]
assert actual == expected
=== END AC value-002-access-contract ===

## User Acceptance

- None.

## Guardrails

- Missing fields yield null rather than Python exceptions.
- Negative array indices follow jq indexing rules.
- Optional access suppresses only the applicable runtime access error.
