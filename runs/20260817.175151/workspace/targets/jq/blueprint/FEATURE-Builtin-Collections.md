# FEATURE: Collection Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Implement jq collection, object, containment, ordering, and flattening builtins. |
| Depends On  | FEATURE-Path-Assignment.md, FEATURE-Flow-Recursion-Utilities.md |
| Provides    | collection, object, containment, sorting, grouping, uniqueness, joining, flattening builtins |
| Consumes    | generator evaluation, path assignment |

## Intent

Implement collection and object-oriented builtins including type selectors, length, keys, entries conversion, containment, sorting, grouping, uniqueness, joining, flattening, combinations, transpose, walk, and related operations. Builtins must preserve jq ordering, structural comparison, and generator behavior.

## Programmatic Acceptance

=== AC collection-and-object-builtins ===
Intent: Core collection and object builtins return structurally consistent values.

import json
import os
import subprocess

payload = {"b": 2, "a": 1}
program = '[type, length, keys, to_entries | length]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0] == "object"
assert actual[1] == len(payload)
assert set(actual[2]) == set(payload)
assert actual[3] == len(payload)
=== END AC collection-and-object-builtins ===

=== AC sorting-grouping-uniqueness ===
Intent: Sorting, grouping, and uniqueness use jq structural ordering and keys.

import json
import os
import subprocess

payload = [{"k": 2, "v": "b"}, {"k": 1, "v": "a"}, {"k": 2, "v": "c"}]
program = '[sort_by(.k), group_by(.k), unique_by(.k)]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert [item["k"] for item in actual[0]] == sorted(item["k"] for item in payload)
assert [len(group) for group in actual[1]] == [1, 2]
assert len(actual[2]) == 2
=== END AC sorting-grouping-uniqueness ===

=== AC containment-and-join ===
Intent: Containment and joining implement their respective collection semantics.

import json
import os
import subprocess

payload = ["a", 2, True, None]
program = '[contains(["a", 2]), join("|")]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0] is True
assert actual[1] == "|".join(["a", "2", "true", ""])
=== END AC containment-and-join ===

=== AC flatten-transpose ===
Intent: Flattening and transposition preserve element order and null padding.

import json
import os
import subprocess

payload = [[1], [2, 3]]
program = '[flatten, transpose]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0] == [1, 2, 3]
assert actual[1][0] == [payload[0][0], payload[1][0]]
assert actual[1][1][0] is None
assert actual[1][1][1] == payload[1][1]
=== END AC flatten-transpose ===

## User Acceptance

- None.

## Guardrails

- Structural ordering must distinguish jq types and must not rely on Python's boolean-as-number ordering.
- Collection builtins must preserve generator multiplicity and ordering.
- Builtins must use only Python standard-library facilities.
