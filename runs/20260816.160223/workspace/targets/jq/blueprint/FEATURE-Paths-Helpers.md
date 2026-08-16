# FEATURE: Paths Helpers

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq nested path mutation, deletion, and projection helpers. |
| Depends On  | FEATURE-Paths-Discovery.md, FEATURE-Values-Model.md |
| Provides    | setpath, delpaths, del, pick |
| Consumes    | path representation, immutable value model |

## Purpose

Implement immutable nested creation, replacement, deletion, projection, missing-path behavior, array index handling, and helper error behavior.

## Behavior

- `setpath` creates missing object and array containers as required and replaces the addressed value.
- `delpaths` removes addressed fields or array elements without mutating the source value.
- `del` derives paths from a path expression and removes them.
- `pick` returns only selected paths while preserving their nested structure.
- Missing values resolve to `null`; invalid path shapes raise runtime errors.
- Multiple paths are processed with jq ordering and overlap semantics.

## Programmatic Acceptance

=== AC paths-helpers-suite ===
Intent: The authoritative corpus passes the path-helper cases owned by this capability.
Suite: scoped

import subprocess

selectors = ["setpath(", "delpaths(", "del(", "pick("]
for selector in selectors:
    result = subprocess.run(
        ["python3", "sources/run_conformance.py", "--select", selector],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0
=== END AC paths-helpers-suite ===

=== AC paths-helpers-roundtrip ===
Intent: Setting, reading, and deleting a nested path produces the declared immutable state transitions.
import json
import subprocess

source = {"a": {"b": 1, "c": 2}}
program = 'setpath(["a","d"]; 3), delpaths([["a","b"]])'
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [
    {"a": {"b": 1, "c": 2, "d": 3}},
    {"a": {"c": 2}},
]
assert actual == expected
assert source == {"a": {"b": 1, "c": 2}}
=== END AC paths-helpers-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Path operations must be immutable and must not alter previously held values.
- Preserve jq behavior for absent paths, negative indices, overlapping paths, and empty path streams.
- Do not modify supplied corpus or harness assets.
