# FEATURE: Streaming Transformations

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq streaming conversion and truncation filters. |
| Depends On  | ARCHITECTURE.md |
| Provides    | tostream, fromstream, truncate_stream |
| Consumes    | ordered generator evaluator, path primitives |

## Workflow

The implementation exposes `tostream`, `fromstream`, and `truncate_stream` as generator-aware filters. Streaming values use jq path/value records, preserve ordering, and reconstruct composite JSON values without mutating the source.

## Programmatic Acceptance

=== AC io-003-conformance ===
Intent: The streaming transformation cases selected from the authoritative corpus execute and pass.
Suite: scoped

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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC io-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Streaming filters must preserve generator order and must not depend on external runtimes or network access.
