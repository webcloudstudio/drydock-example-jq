# FEATURE: Path Discovery

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Discover and read values addressed by jq paths. |
| Depends On  | FEATURE-Core-Indexing.md, FEATURE-Flow-Recursion-Utilities.md |
| Provides    | path, paths, getpath |
| Consumes    | array/object indexing, iteration, recursive generators |

## Intent

Implement exact and generated path discovery over arrays, objects, and recursively nested values. Paths use arrays containing string object keys and numeric array indices.

`path` must preserve paths for existing and non-existing exact locations. `paths` excludes the root path and supports node filters. `getpath` reads one or more paths, returning null for missing values where jq specifies it.

## Programmatic Acceptance

=== AC path-exact-and-read ===
Intent: Exact paths can be materialized and read through the executable.

import json
import os
import subprocess
import sys

payload = {"a": [{"b": 7}]}
program = '[path(.a[0].b), getpath(["a", 0, "b"])]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual[0][-1] == payload["a"][0]["b"]
assert actual[1] == payload["a"][0]["b"]
=== END AC path-exact-and-read ===

=== AC paths-recursive ===
Intent: Recursive path discovery reports non-root paths in traversal order.

import json
import os
import subprocess

payload = {"a": [1, {"b": 2}]}
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", "[paths]"],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert [] not in actual
assert ["a", 0] in actual
assert ["a", 1, "b"] in actual
=== END AC paths-recursive ===

=== AC path-filter ===
Intent: Filtered paths select only locations whose values satisfy the filter.

import subprocess

payload = {"a": [1, "x", 3]}
program = '[paths(type == "number")]'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [["a", 0], ["a", 2]]
=== END AC path-filter ===

## User Acceptance

- None.

## Guardrails

- Path operations must preserve generator ordering and multiplicity.
- Invalid path expressions must raise jq runtime errors rather than silently mutating unrelated values.
- No filesystem module loading is introduced.
