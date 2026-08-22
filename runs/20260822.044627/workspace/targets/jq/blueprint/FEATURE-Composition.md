# FEATURE: Composition

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implement jq composition, Cartesian evaluation, collection, and object construction. |
| Depends On  | FEATURE-Generator-Core.md |
| Provides    | pipe, comma, argument Cartesian products, collection, object construction |
| Consumes    | ordered generator evaluation |

## Programmatic Acceptance

=== AC core-002-composition ===
Intent: Composition evaluates pipes, comma streams, collections, and object construction.
import json
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", "[.[] | . * 2]"],
    input="[1,2,3]\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == [2, 4, 6]

result = subprocess.run(
    ["./jq", "-c", "[1,2] , [3,4]"],
    input="null\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert [json.loads(line) for line in result.stdout.splitlines()] == [[1, 2], [3, 4]]
=== END AC core-002-composition ===

=== AC core-002-cartesian-products ===
Intent: Composition preserves generator multiplicity and Cartesian argument combinations.
import json
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", "[range(2) as $x | range(2) as $y | [$x,$y]]"],
    input="null\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == [[0, 0], [0, 1], [1, 0], [1, 1]]

result = subprocess.run(
    ["./jq", "-c", "{value: (.a, .b)}"],
    input='{"a":1,"b":2}\n',
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert [json.loads(line) for line in result.stdout.splitlines()] == [{"value": 1}, {"value": 2}]
=== END AC core-002-cartesian-products ===

## User Acceptance

- None.

## Guardrails

- Preserve stream order, multiplicity, and Cartesian evaluation.
- Collection must remove no outputs except those produced by `empty`.
- Do not modify files under `sources/`.
