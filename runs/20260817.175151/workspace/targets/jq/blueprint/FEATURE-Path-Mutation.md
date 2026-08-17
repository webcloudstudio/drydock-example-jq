# FEATURE: Path Mutation

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Mutate and delete nested jq paths immutably. |
| Depends On  | FEATURE-Path-Discovery.md |
| Provides    | setpath, delpaths, del |
| Consumes    | path, paths, getpath |

## Intent

Implement immutable nested updates and deletion. Missing object and array containers must be created according to jq semantics. Deletions must remove object keys, array elements, selected slices, and multiple paths without mutating the original input value.

## Programmatic Acceptance

=== AC setpath-creates ===
Intent: setpath creates missing nested containers and stores the supplied value.

import json
import os
import subprocess

payload = None
value = {"ok": True}
program = 'setpath(["a", 0, "b"]; $value)'
# The value is supplied through the jq program so the assertion does not duplicate it.
program = f'setpath(["a", 0, "b"]; {json.dumps(value, separators=(",", ":"))})'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual["a"][0]["b"] == value["ok"]
=== END AC setpath-creates ===

=== AC setpath-preserves-siblings ===
Intent: Updating one nested path preserves unrelated existing fields.

import json
import os
import subprocess

payload = {"a": {"b": 0, "c": 2}, "keep": [1, 2]}
program = 'setpath(["a", "b"]; 9)'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual["a"]["b"] == 9
assert actual["a"]["c"] == payload["a"]["c"]
assert actual["keep"] == payload["keep"]
=== END AC setpath-preserves-siblings ===

=== AC delpaths-and-del ===
Intent: del and delpaths remove only the requested object and array locations.

import json
import os
import subprocess

payload = {"a": 1, "b": 2, "items": ["x", "y", "z"]}
program = 'del(.a), delpaths([["items", 1]])'
result = subprocess.run(
    [os.path.join(os.getcwd(), "jq"), "-c", program],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
outputs = [json.loads(line) for line in result.stdout.splitlines()]
assert outputs[0].get("a") is None
assert outputs[0]["b"] == payload["b"]
assert outputs[1]["items"] == [payload["items"][0], payload["items"][2]]
=== END AC delpaths-and-del ===

## User Acceptance

- None.

## Guardrails

- Updates are immutable and must not alter sibling paths or the original input stream.
- Invalid path types and out-of-bounds mutation cases must produce runtime failure semantics.
- Path-depth protections must prevent uncontrolled recursive allocation.
