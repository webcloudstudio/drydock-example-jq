# FEATURE: jq Collection and Object Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide jq collection, filtering, sorting, grouping, object, and aggregate builtins. |
| Depends On  | FEATURE-EVAL-003.md, FEATURE-DATA-003.md |
| Provides    | map, select, reduce helpers, sorting, grouping, uniqueness, entries, joins, flattening |
| Consumes    | generator evaluator, structural operations, path mutation |

## Purpose

Implement the collection and object helpers defined by jq, including map/select, sorting and
grouping, uniqueness, min/max, entries conversion, joins, flattening, combinations, transpose,
containment, and related object utilities. Preserve jq ordering and stream multiplicity.

## Programmatic Acceptance

=== AC builtin-001-collections ===
Intent: Mapping and selection preserve array order and filter values.
import json
import subprocess

source = '[1,5,3,0]'
program = 'map(select(. >= 2) | . + 1)'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [6, 4, 2]
=== END AC builtin-001-collections ===

=== AC builtin-001-sorting ===
Intent: Sorting and uniqueness use jq value ordering.
import json
import subprocess

source = '[3,1,3,2]'
program = '[sort, unique]'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [[1, 2, 3, 3], [1, 2, 3]]
=== END AC builtin-001-sorting ===

=== AC builtin-001-objects ===
Intent: Entry conversion and object updates preserve keys and values.
import json
import subprocess

source = '{"a":1,"b":2}'
program = 'to_entries | map(.key |= "x_" + .) | from_entries'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == {"x_a": 1, "x_b": 2}
=== END AC builtin-001-objects ===

=== AC builtin-001-aggregates ===
Intent: Grouping and flattening produce deterministic aggregate values.
import json
import subprocess

source = '[{"k":2},{"k":1},{"k":2}]'
program = '[group_by(.k), ([1,[2],[[3]]] | flatten)]'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [[[{"k": 1}], [{"k": 2}, {"k": 2}]], [1, 2, 3]]
=== END AC builtin-001-aggregates ===

## User Acceptance

- None.

## Guardrails

- Preserve stable jq generator order and multiplicity.
- Object helpers must not discard unrelated keys.
- Collection builtins must use the evaluator and path semantics rather than duplicate incompatible rules.
