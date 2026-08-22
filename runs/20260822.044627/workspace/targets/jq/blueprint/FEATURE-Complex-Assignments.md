# FEATURE: Complex Assignment Edge Cases

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Handles iterated, invalid, numeric-edge, and depth-limited assignment paths. |
| Depends On  | FEATURE-Assignment-Operators.md |
| Provides    | iterated assignment edge cases, array expansion, invalid and deep paths |
| Consumes    | deletion and assignment operators |

## Scope

Complete assignment behavior for iterated paths, empty updates, array expansion, negative and NaN indices, invalid path transitions, and deep path limits. Array and string slice updates follow jq's distinct mutation rules, and failures preserve partial output and runtime exit semantics.

## Programmatic Acceptance

=== AC path-004-conformance ===
Intent: Complex assignment edge cases execute with the required mutation behavior.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", ".[] |= . + 1"],
    input="[1,2,3]\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == [2, 3, 4]

result = subprocess.run(
    ["./jq", "-c", ".a[2] = 7"],
    input="{}\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == {"a": [None, None, 7]}
=== END AC path-004-conformance ===

## User Acceptance

- None.

## Guardrails

- NaN and invalid indices must not silently select or mutate arbitrary elements.
- Depth limits must terminate safely with the specified runtime behavior.
- Empty updates must delete rather than retain stale values.
