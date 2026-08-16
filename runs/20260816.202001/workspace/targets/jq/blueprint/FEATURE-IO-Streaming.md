# FEATURE: I/O and Streaming

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide jq input, diagnostic-output, and streaming conversion builtins. |
| Depends On  | FEATURE-Reductions.md, FEATURE-Date-JSON-Encoding.md |
| Provides    | input, inputs, debug, stderr, tostream, fromstream, truncate_stream |
| Consumes    | stdin stream, stdout result stream, stderr diagnostics |

## Purpose

Implement the supported I/O and streaming builtins while preserving ordered generator behavior. `input` and `inputs` consume JSON values from the remaining stdin stream; `debug` and `stderr` write diagnostics without contaminating stdout; streaming builtins convert between values and path/value event streams.

## Behavior

- `inputs` emits every remaining JSON input in order.
- `input` emits exactly the next JSON input or raises the jq-compatible end-of-input error.
- `stderr` emits no result and writes its input as raw diagnostic data.
- `debug` preserves its input result while writing a diagnostic.
- `tostream` and `fromstream` round-trip supported JSON values.
- `truncate_stream` removes the requested leading path components.

## Programmatic Acceptance

=== AC inputs-order ===
Intent: inputs emits all supplied JSON documents in their original order.

import json
import subprocess

values = [1, {"value": 2}, [3]]
result = subprocess.run(["./jq", "-c", "inputs"], input="\n".join(json.dumps(v) for v in values) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == values
=== END AC inputs-order ===

=== AC stream-roundtrip ===
Intent: tostream followed by fromstream preserves a supplied composite value.

import json
import subprocess

value = {"a": [1, {"b": True}], "c": None}
payload = json.dumps(value, separators=(",", ":"))
result = subprocess.run(["./jq", "-c", "tostream | fromstream"], input=payload + "\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC stream-roundtrip ===

=== AC stderr-isolation ===
Intent: stderr produces no stdout result while the process completes successfully.

import subprocess

value = "diagnostic"
result = subprocess.run(["./jq", "-c", "stderr"], input='"' + value + '"\n', capture_output=True, text=True)
assert result.returncode == 0
assert result.stdout == ""
assert value in result.stderr
=== END AC stderr-isolation ===

## User Acceptance

- None.

## Guardrails

- Never redirect diagnostics into the JSON result stream.
- Preserve partial stdout output if a later input or stream operation fails.
- Do not modify supplied scoring assets.
