# FEATURE: Complex Assignment Edges

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines edge-case behavior for iterated, empty, fractional, invalid, and deep assignments. |
| Depends On  | FEATURE-Deletion-And-Assignment.md, FEATURE-Path-Primitives.md |
| Provides    | Iterated path assignment, empty-update deletion, array expansion, assignment depth protections |
| Consumes    | Assignment operators, path primitives |

## Purpose

Complete assignment semantics for complex path expressions and adversarial boundary cases.

## Implementation Requirements

- Apply assignments across iterated and multi-path selections in generator order.
- Treat an update producing `empty` as deletion.
- Expand arrays with `null` values when setting beyond their current length.
- Handle negative, fractional, NaN, and out-of-range indexes according to jq semantics.
- Reject invalid string updates and invalid array path components with runtime errors.
- Enforce assignment path depth limits.
- Preserve partial output behavior when a later assignment fails.

## Programmatic Acceptance

=== AC complex-assignment-conformance ===
Intent: The complex assignment implementation passes representative declared path update and empty-update deletion behaviors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess

jq = os.path.join(os.getcwd(), "jq")

updated = subprocess.run(
    [jq, "-c", ".a |= . + 1"],
    input='{"a":1}',
    capture_output=True,
    text=True,
)
assert updated.returncode == 0
assert json.loads(updated.stdout) == {"a": 2}

deleted = subprocess.run(
    [jq, "-c", "del(.a)"],
    input='{"a":1,"b":2}',
    capture_output=True,
    text=True,
)
assert deleted.returncode == 0
assert json.loads(deleted.stdout) == {"b": 2}

=== END AC complex-assignment-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not silently clamp invalid assignment indexes when jq specifies an error.
- Do not discard valid outputs produced before a later runtime failure.
- Do not exceed configured path depth limits through recursive or iterated assignments.
