# FEATURE: Streaming Transformations

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Reconstruct, truncate, and emit jq streaming representations. |
| Depends On  | ARCHITECTURE.md, FEATURE-Generator-Core.md, FEATURE-Input-Streams.md |
| Provides    | tostream, fromstream, truncate_stream |
| Consumes    | ordered generator evaluation, input stream controls |

## Workflow

Streaming filters represent composite JSON values as ordered path/value events. `tostream` emits
the representation, `truncate_stream` removes a specified number of leading path components, and
`fromstream` reconstructs values from the resulting event stream. Implement these filters with
generator ordering, empty-container markers, truncation, and round-trip behavior matching the
manual and corpus.

## Programmatic Acceptance

=== AC streaming-conformance ===
Intent: The streaming implementation passes every selected corpus case covering tostream, fromstream, and truncate_stream.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"tostream|fromstream|truncate_stream"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC streaming-conformance ===

=== AC streaming-round-trip ===
Intent: A streamed value can be reconstructed without changing its value.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

program = r". as $dot | fromstream($dot | tostream) | . == $dot"
payload = " [0,[1,{\"a\":1},{\"b\":2}]]\n"
result = subprocess.run(
    [f"{os.getcwd()}/jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
    env={**os.environ},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
assert json.loads(result.stdout) is True
=== END AC streaming-round-trip ===

## User Acceptance

- None.

## Guardrails

- Streaming filters must preserve event order and must not use third-party runtimes.
- Invalid stream structures must produce jq-compatible runtime failures.
