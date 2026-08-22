# FEATURE: Object and Containment Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq object-entry, key, membership, and structural containment builtins. |
| Depends On  | FEATURE-Sorting-and-Grouping.md, FEATURE-Value-Model.md |
| Provides    | keys, keys_unsorted, has, in, inside, contains, to_entries, from_entries, with_entries |
| Consumes    | jq value model, structural equality, collection transformations |

## Scope

This feature implements object and array key inspection, membership predicates, recursive containment, conversion between objects and entry arrays, and entry transformations.

## Behavior

- `keys` sorts object keys and returns array indices for arrays.
- `keys_unsorted` preserves object insertion order.
- `has` tests object keys or valid array indices.
- `in` reverses `has`.
- `contains` and `inside` apply recursive jq containment rules to strings, arrays, objects, and scalar values.
- `to_entries`, `from_entries`, and `with_entries` preserve supported key and value spellings.

## Programmatic Acceptance

=== AC data-003-conformance ===
Intent: Object and containment builtins produce the declared structural results.

import json
import subprocess

program = '[keys, keys_unsorted, has("a"), ("a" | in({"a": 1})), contains({"a": 1}), ({"a": 1} | inside({"a": 1, "b": 2})), to_entries, (to_entries | from_entries), (with_entries(.value += 1))]'
result = subprocess.run(
    ["./jq", "-c", program],
    input='{"b":2,"a":1}\n',
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr, file=__import__("sys").stderr)
assert result.returncode == 0
values = json.loads(result.stdout)
assert values[0] == ["a", "b"]
assert values[1] == ["b", "a"]
assert values[2:] == [True, True, False, True, {"b": 2, "a": 1}, {"b": 3, "a": 2}]
=== END AC data-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Object key order must not affect structural equality or containment.
- Preserve insertion order only for `keys_unsorted`.
- Enforce containment depth and type semantics defined by jq.
