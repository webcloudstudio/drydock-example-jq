# FEATURE: Builtins IO

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Provide jq input, diagnostic, environment, and source-location builtins. |
| Depends On | FEATURE-Builtins-Streaming.md |
| Provides | input, inputs, debug, stderr, env, ENV, $__loc__ |
| Consumes | stdin JSON stream, process environment, jq output streams |

## Scope

This feature implements `input` and `inputs` over the shared JSON input stream, `debug` and `stderr` side effects, environment snapshots through `env` and `$ENV`, and source-location values through `$__loc__`.

## Programmatic Acceptance

=== AC builtins-io-conformance ===
Intent: The environment and I/O builtin corpus slice executes and passes with at least one selected case.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(input|inputs|debug|stderr|env|ENV|__loc__)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC builtins-io-conformance ===

## User Acceptance

- I/O and diagnostic behavior is distinguishable between JSON output and stderr effects.

## Guardrails

- Preserve input ordering and generator semantics for `input` and `inputs`.
- Diagnostics must not be compared or emitted as ordinary JSON results.
- Do not modify staged scoring assets.
