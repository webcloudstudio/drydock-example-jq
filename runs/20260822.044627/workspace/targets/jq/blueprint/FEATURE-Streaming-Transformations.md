# FEATURE: Streaming Transformations

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Implement jq streaming conversion and truncation filters over the fixed process boundary. |
| Depends On  | FEATURE-Path-Discovery.md, FEATURE-Generator-Core.md, FEATURE-Collection-Transformations.md |
| Provides    | tostream, fromstream, truncate_stream |
| Consumes    | ordered generators, path discovery, JSON values |

## Purpose

Implement the streaming value representation described by the jq manual while retaining the fixed non-streaming CLI interface. `tostream` emits path/value stream records, `fromstream` reconstructs values, and `truncate_stream` removes leading path components.

## Behavior

- `tostream` emits stream records in jq traversal order, including container termination records.
- `fromstream` reconstructs arrays, objects, scalars, empty containers, and multiple streamed values.
- `truncate_stream` consumes an integer depth and emits records with that many leading path components removed.
- Invalid stream structures and invalid truncation depths follow jq runtime-error behavior.
- The implementation uses only the standard library and preserves generator ordering.

## Programmatic Acceptance

=== AC streaming-conformance ===
Intent: The streaming filters pass the executed conformance cases selected by their syntax.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"tostream|fromstream|truncate_stream"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", select, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC streaming-conformance ===

=== AC streaming-roundtrip ===
Intent: A streamed value can be reconstructed without changing its value.
import json
import os
import subprocess

source = "[0,[1,{\"a\":2}]]"
program = ". as $dot | fromstream($dot|tostream) | . == $dot"
result = subprocess.run(
    ["./jq", "-c", program],
    input=source + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [True]
assert actual == expected
=== END AC streaming-roundtrip ===

=== AC streaming-truncation ===
Intent: Truncating a stream removes the requested leading path depth.
import json
import subprocess

stream = "[[0],\"a\"],[[1,0],\"b\"],[[1,0]],[[1]]"
program = "truncate_stream(1|[[0],\"a\"],[[1,0],\"b\"],[[1,0]],[[1]])"
result = subprocess.run(
    ["./jq", "-c", program],
    input="1\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
expected = [[[0], "b"], [[0]]]
assert actual == expected
=== END AC streaming-truncation ===

## User Acceptance

- None.

## Guardrails

- Do not add a streaming command-line mode; these filters operate within the fixed `-c` interface.
- Do not shell out to jq or use a third-party implementation.
- Preserve stream record order and multiplicity.
- Do not modify files under `sources/`.
