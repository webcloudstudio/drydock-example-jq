# FEATURE: Collection Transforms

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq collection transformation builtins with generator-aware recursive behavior. |
| Depends On  | FEATURE-Complex-Assignments.md, FEATURE-Generator-Core.md |
| Provides    | map, map_values, select, add, flatten, transpose, combinations, walk |
| Consumes    | assignment operators, ordered generator evaluation |

## Scope

This feature implements collection transformation filters over arrays and objects. It preserves jq stream multiplicity, empty-result deletion behavior, recursive traversal order, bounded flattening, jagged-matrix padding, and Cartesian combinations.

## Behavior

- `map` collects all outputs produced for each input element.
- `map_values` updates each element or object value using the first produced result and removes values producing `empty`.
- `select` preserves the input only for truthy predicates.
- `add` reduces array or generated values using jq addition.
- `flatten` supports unlimited and bounded depth, rejecting negative depth.
- `transpose` pads jagged rows with `null`.
- `combinations` produces ordered Cartesian combinations.
- `walk` transforms children before their containing array or object.

## Programmatic Acceptance

=== AC data-001-conformance ===
Intent: Collection transformation builtins preserve collection shape, ordering, and Cartesian behavior.
Requires: executable=python3; scope=test

import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "map(. * 2), map_values(. + 1), select(length == 2), add, flatten(1), transpose, combinations"],
    input='[1,2]\n',
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual[0] == [2, 4]
assert actual[1] == [2, 3]
=== END AC data-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Preserve generator ordering and multiplicity.
- Do not modify files under `sources/`.
