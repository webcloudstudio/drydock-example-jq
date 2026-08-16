# FEATURE: Paths Discovery

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq path discovery and nested value lookup. |
| Depends On  | ARCHITECTURE.md, FEATURE-Control-Recursion.md, FEATURE-Eval-Core.md |
| Provides    | path, paths, getpath |
| Consumes    | ordered generator evaluator, indexing, recursion |

## Purpose

Implement jq path representations, exact and generated path expressions, recursive path enumeration, filtered paths, and nested lookup through `getpath`.

## Behavior

- `path` emits arrays containing string object keys and integer array indices.
- `paths` emits every non-root path; `paths(f)` emits paths whose selected values satisfy `f`.
- `getpath` returns the value at a path, or `null` for absent paths.
- Invalid path expressions and invalid index types raise runtime errors.
- Path traversal preserves document order and generator ordering.

## Programmatic Acceptance

=== AC paths-discovery-suite ===
Intent: The authoritative corpus passes the path-discovery cases owned by this capability.
Suite: scoped

import subprocess

selectors = ["path(", "[paths", "getpath("]
for selector in selectors:
    result = subprocess.run(
        ["python3", "sources/run_conformance.py", "--select", selector],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0
=== END AC paths-discovery-suite ===

=== AC paths-discovery-roundtrip ===
Intent: A discovered path can be consumed to retrieve the corresponding value.
import json
import subprocess

source = {"a": [{"b": 7}]}
program = "[paths] as $paths | [$paths[] as $p | getpath($p)]"
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(source) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = [source["a"], source["a"][0], source["a"][0]["b"]]
assert actual == [expected]
=== END AC paths-discovery-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Do not confuse the root path `[]` with paths emitted by `paths`.
- Do not mutate the input while discovering or reading paths.
- Do not shell out to jq or use a third-party jq implementation.
