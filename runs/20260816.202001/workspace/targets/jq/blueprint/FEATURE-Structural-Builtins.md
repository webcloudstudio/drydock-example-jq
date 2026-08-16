# FEATURE: Collection and Structural Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Defines jq builtins for collection, structure, paths, containment, and recursive transformation. |
| Depends On  | FEATURE-Reductions.md, FEATURE-Core-Values.md, FEATURE-Operators.md |
| Provides    | collection, sorting, grouping, uniqueness, containment, entries, walking, flattening, transpose, paths |
| Consumes    | core values, paths, assignments, reductions |

## Intent

This feature implements structural builtins expressed over arrays, objects, paths, and recursive
values. Builtins must retain jq's type ordering, stable generator behavior, immutable value model,
and path semantics.

## Behavior

- Collection helpers include `map`, `map_values`, `add`, `join`, `flatten`, `transpose`, and
  `combinations`.
- Ordering helpers include `sort`, `sort_by`, `group_by`, `unique`, `unique_by`, `min`, and
  `max_by`.
- Object helpers include `to_entries`, `from_entries`, and `with_entries`.
- Structural predicates include `contains`, `inside`, `arrays`, `objects`, `iterables`, `scalars`,
  `values`, and related selectors.
- `walk` recursively transforms children before their containing array or object.
- `path`, `paths`, `getpath`, `setpath`, `delpaths`, `pick`, and `del` preserve path order and
  path creation/deletion rules.
- Invalid types and invalid paths raise jq runtime errors.

## Programmatic Acceptance

=== AC structural-builtins-suite ===
Intent: The supplied conformance corpus passes the collection, structural, path, and transformation cases owned by this feature.
Suite: scoped

import subprocess
import os

pattern = r"map|map_values|sort|group_by|unique|contains|inside|to_entries|from_entries|with_entries|flatten|transpose|combinations|walk|path|paths|getpath|setpath|delpaths|pick|del\\("
result = subprocess.run(
    ["python3", "sources/run_conformance.py", "--select", pattern],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": "./jq"},
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
=== END AC structural-builtins-suite ===

=== AC structural-round-trip ===
Intent: Entry conversion and structural transformation preserve object contents and keys.
import subprocess
import json

program = "with_entries(.key |= \"x_\" + .)"
input_value = '{"a":1,"b":2}\n'
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [{"x_a": 1, "x_b": 2}]
assert actual == expected
=== END AC structural-round-trip ===

=== AC structural-ordering ===
Intent: Sorting and uniqueness use jq's structural ordering and remove duplicates.
import subprocess
import json

program = "[sort, unique]"
input_value = "[3,1,3,2]\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [[1, 2, 3], [1, 2, 3]]
assert actual == expected
=== END AC structural-ordering ===

=== AC path-update ===
Intent: Path utilities can read, update, and delete nested values.
import subprocess
import json

program = "[getpath([\"a\",\"b\"]), setpath([\"a\",\"b\"]; 2), delpaths([[\"a\",\"b\"]])]"
input_value = '{"a":{"b":1,"c":3}}\n'
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [1, {"a": {"b": 2, "c": 3}}, {"a": {"c": 3}}]
assert actual == expected
=== END AC path-update ===

## User Acceptance

- None.

## Guardrails

- Preserve jq's null/boolean/number/string/array/object ordering.
- Do not mutate the original input value while computing an assignment or path update.
- Do not silently reinterpret invalid path expressions as ordinary values.
