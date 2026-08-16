# FEATURE: Traversal, Streaming, Environment, and Utility Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq traversal, streaming, environment, debugging, and utility builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-Builtins-Collections.md, FEATURE-Builtins-Formats.md, FEATURE-Paths-Discovery.md, FEATURE-Control-Recursion.md |
| Provides    | walk, transpose, bsearch, tostream, fromstream, truncate_stream, env, debug, utility builtins |
| Consumes    | evaluator, paths, values, and string builtins |

## Scope

Implement `walk`, `transpose`, `bsearch`, `tostream`, `fromstream`, `truncate_stream`, `env`, `debug`, `stderr`, `input`, `inputs`, `builtins`, and related documented utility functions. Preserve generator order and jq stream representations.

## Behavior

- `walk` transforms children before their containing arrays or objects.
- `transpose` pads jagged rows with null.
- `bsearch` returns an index or insertion-point encoding.
- `tostream` and `fromstream` round-trip supported JSON values.
- `env` exposes the process environment without mutating it.
- `debug` writes diagnostics to stderr while preserving its input output.
- Utility functions preserve jq stream and error semantics.

## Programmatic Acceptance

=== AC utilities ===
Intent: Traversal, matrix, search, streaming, and environment utilities operate through the jq executable.

import json
import os
import subprocess

program = '[walk(if type == "array" then length else . end), transpose, bsearch(2), (tostream | fromstream), (env | has("PATH"))]'
source = '[[[1,2],[3]], [[1],[2,3]], [1,2,3]]'
result = subprocess.run(
    ["./jq", "-c", program],
    input=source,
    capture_output=True,
    text=True,
    env={**os.environ, "JQ_ACCEPTANCE_MARKER": "present"},
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
values = json.loads(result.stdout)
assert values[0] == [2, 1]
assert values[1] == [[1, 2], [3, None]]
assert values[2] == -1
assert values[3] == json.loads(source)
assert values[4] is True
=== END AC utilities ===

=== AC debug-preserves-output ===
Intent: Debugging writes diagnostics without changing the value stream.

import json
import subprocess

source = "42"
result = subprocess.run(
    ["./jq", "-c", "debug"],
    input=source,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert json.loads(result.stdout) == json.loads(source)
assert result.stderr != ""
=== END AC debug-preserves-output ===

=== AC environment ===
Intent: Environment access reflects an inherited environment variable.

import json
import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "env.JQ_ACCEPTANCE_MARKER"],
    input="null",
    capture_output=True,
    text=True,
    env={**os.environ, "JQ_ACCEPTANCE_MARKER": "present"},
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
assert json.loads(result.stdout) == "present"
=== END AC environment ===

## User Acceptance

- None.

## Guardrails

- Preserve input and output ordering for all generator and streaming utilities.
- Extend inherited environments when invoking tools; never replace the process environment.
- Use only standard-library functionality.
