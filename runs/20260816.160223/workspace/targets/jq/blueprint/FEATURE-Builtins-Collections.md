# FEATURE: Builtins Collections

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq collection, ordering, grouping, containment, and object helpers. |
| Depends On  | FEATURE-Paths-Assignment.md, FEATURE-Language-Functions.md, FEATURE-Values-Comparison.md |
| Provides    | map, map_values, add, sort, sort_by, group_by, unique, unique_by, min, max, entries, containment, object helpers |
| Consumes    | evaluator, jq values, paths, comparison semantics |

## Purpose

Implement standard collection and object builtins over arrays and objects, including generator-aware mapping, ordering, grouping, uniqueness, reductions, containment, entries, and recursive traversal helpers.

## Behavior

- `map` collects all outputs from its filter; `map_values` retains only the first output per member and drops members producing `empty`.
- `add` combines numbers, strings, arrays, and objects using jq addition semantics.
- Sorting uses jq’s total type ordering and preserves stable ordering for equal keys.
- Grouping and uniqueness sort by the requested filter and retain jq-defined representatives.
- `min`, `max`, `min_by`, and `max_by` return `null` for empty arrays.
- `to_entries`, `from_entries`, and `with_entries` preserve supported key/value aliases.
- `contains` and `inside` recurse through arrays, objects, and strings.

## Programmatic Acceptance

=== AC builtins-collections-suite ===
Intent: The authoritative corpus passes the collection and object-builtin cases owned by this capability.
Suite: scoped

import subprocess

selectors = ["map(", "map_values(", "add", "sort", "group_by", "unique", "min", "max", "to_entries", "from_entries", "with_entries", "contains(", "inside("]
for selector in selectors:
    result = subprocess.run(
        ["python3", "sources/run_conformance.py", "--select", selector],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0
=== END AC builtins-collections-suite ===

=== AC builtins-collections-roundtrip ===
Intent: Collection transformations preserve the expected members and object structure.
import json
import subprocess

source = [{"k": 2}, {"k": 1}, {"k": 1}]
program = "{sorted: (sort_by(.k)), unique: (unique_by(.k)), entries: (to_entries)}"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = {
    "sorted": [{"k": 1}, {"k": 1}, {"k": 2}],
    "unique": [{"k": 1}, {"k": 2}],
    "entries": [{"key": "0", "value": {"k": 2}}, {"key": "1", "value": {"k": 1}}, {"key": "2", "value": {"k": 1}}],
}
assert actual == expected
=== END AC builtins-collections-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering and cartesian argument behavior.
- Use jq structural comparison and type ordering rather than Python’s boolean-as-number ordering.
- Do not mutate collection inputs while computing results.
