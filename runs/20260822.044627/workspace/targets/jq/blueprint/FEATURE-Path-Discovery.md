# FEATURE: Path Discovery and Projection

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Discovers jq paths and constructs projections from path expressions. |
| Depends On  | FEATURE-Destructuring.md, FEATURE-Accessors.md |
| Provides    | path, paths, pick, path projections |
| Consumes    | destructuring and field/index access |

## Scope

Implement exact and generated path expressions, recursive path enumeration, filtered `paths`, and `pick` projections. Path results preserve jq's ordering and use string object keys and numeric array indices. Invalid path expressions raise runtime errors according to jq semantics.

## Programmatic Acceptance

=== AC path-001-conformance ===
Intent: Path discovery and projection behavior executes successfully for representative path, paths, and pick programs.
Suite: scoped
Requires: executable=python3; scope=test

import subprocess

path_result = subprocess.run(
    ["./jq", "-c", "path(.a)",],
    input='{"a":1}\n',
    capture_output=True,
    text=True,
)
paths_result = subprocess.run(
    ["./jq", "-c", "paths",],
    input='{"a":1,"b":[2]}\n',
    capture_output=True,
    text=True,
)
pick_result = subprocess.run(
    ["./jq", "-c", "pick(.a)",],
    input='{"a":1,"b":2}\n',
    capture_output=True,
    text=True,
)
assert path_result.returncode == 0
assert path_result.stdout.splitlines() == ['["a"]']
assert paths_result.returncode == 0
assert paths_result.stdout.splitlines() == ['["a"]', '["b",0]']
assert pick_result.returncode == 0
assert pick_result.stdout.splitlines() == ['{"a":1}']
=== END AC path-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Path enumeration must preserve traversal order and distinguish empty root paths from descendant paths.
- Projection must not mutate the source value.
