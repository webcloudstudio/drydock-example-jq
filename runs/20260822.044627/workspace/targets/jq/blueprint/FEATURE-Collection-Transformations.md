# FEATURE: Collection Transformations

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq collection transformation builtins with generator-preserving behavior. |
| Depends On  | FEATURE-Reductions-And-Iteration-Control.md, FEATURE-Deletion-And-Assignment.md, FEATURE-Type-And-Numeric-Primitives.md |
| Provides    | map, map_values, select, add, flatten, transpose, combinations, walk |
| Consumes    | generator evaluator, operators, path mutation |

## Workflow

Collection filters transform arrays and objects while preserving jq stream order and multiplicity. Implement `map`, `map_values`, `select`, `add`, `flatten`, `transpose`, `combinations`, and recursive `walk` using the established evaluator and immutable update semantics. Empty generators, nested arrays, jagged matrices, and recursive values must follow the manual and `sources/builtin.jq`.

## Programmatic Acceptance

=== AC data-001-conformance ===
Intent: The collection transformation implementation passes representative declared map and flatten behaviors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess

jq = os.path.join(os.getcwd(), "jq")

mapped = subprocess.run(
    [jq, "-c", "map(. * 2)"],
    input="[1,2,3]",
    capture_output=True,
    text=True,
)
assert mapped.returncode == 0
assert json.loads(mapped.stdout) == [2, 4, 6]

flattened = subprocess.run(
    [jq, "-c", "flatten"],
    input="[[1],[2,3]]",
    capture_output=True,
    text=True,
)
assert flattened.returncode == 0
assert json.loads(flattened.stdout) == [1, 2, 3]

=== END AC data-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering, multiplicity, and backtracking.
- Do not mutate input values in place.
- Use only Python standard-library facilities.
