# FEATURE: jq Structural Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Define jq collection, structural, ordering, containment, and recursive traversal builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-LANG-PATHS.md |
| Provides    | map, map_values, add, flatten, sort, sort_by, group_by, unique, entries, contains, inside, combinations, transpose, walk |
| Consumes    | jq paths and assignments, generator evaluator |

## Scope

Implement structural builtins using the evaluator's generator model. Builtins must preserve jq ordering and support arrays, objects, nested values, empty streams, and generator-valued arguments.

## Behavior

- Collection builtins preserve stream multiplicity and collect outputs where specified.
- `map` and `map_values` distinguish array collection from first-result updates.
- `add`, `flatten`, sorting, grouping, uniqueness, and containment follow jq type ordering and recursive semantics.
- `to_entries`, `from_entries`, and `with_entries` preserve key/value meaning.
- `combinations`, `transpose`, `walk`, `paths`, and related traversal helpers handle empty and jagged structures.

## Programmatic Acceptance

=== AC structural-collection ===
Intent: Collection builtins transform the supplied input and preserve its derived elements.
import json
import subprocess

source_value = [1, 2, 3]
program = "[map(. + 1), add, flatten]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = [list(map(lambda item: item + 1, source_value)), sum(source_value), source_value]
assert actual == expected
=== END AC structural-collection ===

=== AC structural-ordering ===
Intent: Sorting and uniqueness return the supplied values in jq order.
import json
import subprocess

source_value = [3, 1, 3, 2]
program = "[sort, unique]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = [sorted(source_value), sorted(set(source_value))]
assert actual == expected
=== END AC structural-ordering ===

=== AC structural-entries ===
Intent: Entry conversion round-trips the supplied object.
import json
import subprocess

source_value = {"a": 1, "b": 2}
program = "to_entries | from_entries"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == source_value
=== END AC structural-entries ===

=== AC structural-containment ===
Intent: Containment and inversion agree for supplied nested values.
import json
import subprocess

container = {"a": [1, 2], "b": {"x": 3}}
contained = {"a": [1], "b": {}}
program = f"[contains({json.dumps(contained)}), inside({json.dumps(container)})]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(container) + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == [True, True]
=== END AC structural-containment ===

## User Acceptance

- None.

## Guardrails

- Do not replace generator evaluation with single-value shortcuts.
- Preserve stable output order where jq defines it.
- Keep structural operations within the Python standard library.
