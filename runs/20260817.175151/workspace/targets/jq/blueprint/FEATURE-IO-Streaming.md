# FEATURE: IO Streaming

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq streaming serialization, reconstruction, and stream truncation builtins. |
| Depends On  | FEATURE-Path-Discovery.md, FEATURE-Flow-Recursion-Utilities.md |
| Provides    | tostream, fromstream, truncate_stream |
| Consumes    | path discovery and recursive generators |

## Behavior

The interpreter implements jq's compact path/value streaming representation. `tostream` emits a representation that `fromstream` can reconstruct, and `truncate_stream` removes the requested number of leading path elements while preserving stream ordering and values.

## Programmatic Acceptance

=== AC streaming-roundtrip ===
Intent: A supplied JSON value round-trips through tostream and fromstream.
import json
import subprocess

value = {"items": [1, {"name": "jq"}], "active": True}
result = subprocess.run(
    ["./jq", "-c", "fromstream(tostream)"],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC streaming-roundtrip ===

=== AC streaming-shape ===
Intent: tostream emits a stream of two-element path/value records for supplied scalar leaves.
import json
import subprocess

value = {"a": 1, "b": 2}
result = subprocess.run(
    ["./jq", "-c", '[tostream | select(length == 2)]'],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
records = json.loads(result.stdout)
assert records
assert all(isinstance(record, list) and len(record) == 2 for record in records)
assert all(isinstance(record[0], list) for record in records)
=== END AC streaming-shape ===

=== AC streaming-truncate ===
Intent: truncate_stream removes the requested leading path component from stream records.
import json
import subprocess

stream = [[["root", 0], "a"], [["root", 1], "b"]]
expected = [[[0], "a"], [[1], "b"]]
program = "1 | truncate_stream(" + ",".join(json.dumps(item) for item in stream) + ")"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == expected
=== END AC streaming-truncate ===

=== AC streaming-nested-roundtrip ===
Intent: Nested arrays and objects survive stream reconstruction.
import json
import subprocess

value = [[0, [1]], {"x": [2, 3]}]
result = subprocess.run(
    ["./jq", "-c", ". as $value | fromstream($value | tostream) == $value"],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) is True
=== END AC streaming-nested-roundtrip ===

## User Acceptance

- None.

## Guardrails

- Streaming transformations preserve path order, value multiplicity, and JSON-compatible representations.
