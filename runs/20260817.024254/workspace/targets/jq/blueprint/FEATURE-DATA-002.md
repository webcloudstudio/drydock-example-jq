# FEATURE: jq Path Discovery and Mutation

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provide jq path discovery, lookup, replacement, and deletion primitives. |
| Depends On  | FEATURE-DATA-001.md, FEATURE-EVAL-001.md |
| Provides    | path, paths, getpath, setpath, delpaths, del |
| Consumes    | JSON structural operations, generator evaluator |

## Purpose

Implement immutable path operations for nested arrays and objects. Exact paths may describe missing
locations; discovered paths must preserve generator order. Invalid paths and excessive path depth
must raise runtime errors.

## Programmatic Acceptance

=== AC data-002-path-roundtrip ===
Intent: Path lookup and replacement round-trip through the executable.
import json
import subprocess

source = '{"a":{"b":[0,1]}}'
program = '[path(.a.b[1]), getpath(["a","b",1]), setpath(["a","b",1]; 9)]'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
values = [json.loads(line) for line in result.stdout.splitlines()]
assert values[0][0] == ["a", "b", 1]
assert values[0][1] == 1
assert values[0][2]["a"]["b"][1] == 9
=== END AC data-002-path-roundtrip ===

=== AC data-002-discovery ===
Intent: Recursive path discovery returns every non-root structural path.
import json
import subprocess

source = '{"a":[1,{"b":2}]}'
program = '[paths]'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [["a"], ["a", 0], ["a", 1], ["a", 1, "b"]]
=== END AC data-002-discovery ===

=== AC data-002-deletion ===
Intent: Deleting multiple paths removes only the selected members.
import json
import subprocess

source = '{"a":[0,1,2],"b":3}'
program = 'delpaths([["a",1],["b"]])'
result = subprocess.run(["./jq", "-c", program], input=source, text=True, capture_output=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == {"a": [0, 2]}
=== END AC data-002-deletion ===

## User Acceptance

- None.

## Guardrails

- Path operations must not mutate the original input value.
- Do not shell out to a system jq executable or use third-party implementations.
- Preserve missing-path, negative-index, invalid-path, and path-depth behavior defined by the supplied corpus.
