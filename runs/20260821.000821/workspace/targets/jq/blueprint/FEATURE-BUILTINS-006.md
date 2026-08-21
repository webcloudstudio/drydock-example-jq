# FEATURE: Environment, Diagnostics, and I/O Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Provide jq input, environment, diagnostic, location, and builtin-introspection filters. |
| Depends On  | FEATURE-BUILTINS-005.md |
| Provides    | input, inputs, debug, stderr, env, $ENV, $__loc__, builtins |
| Consumes    | CLI stdin/stdout/stderr boundary, generator evaluator |

## Purpose

Implement jq's process-facing filters while preserving the executable's stream model. Additional inputs are consumed from stdin in order; environment views expose process state; diagnostics use stderr without contaminating JSON stdout; location and builtin introspection return jq-compatible values.

## Behavior

- `input` consumes one subsequent JSON input and `inputs` emits all remaining inputs.
- `debug` and `stderr` write diagnostics to stderr while preserving the specified stdout stream.
- `env` and `$ENV` expose the process environment.
- `$__loc__` produces source-location metadata.
- `builtins` emits the available builtin name/arity entries.
- Input exhaustion and runtime errors follow jq's stream and error behavior.

## Programmatic Acceptance

=== AC builtins-006-io ===
Intent: The authoritative corpus slice covering input, inputs, diagnostics, environment, and source locations executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"input|inputs|debug|stderr|env|\$ENV|\$__loc__"
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
=== END AC builtins-006-io ===

=== AC builtins-006-builtins ===
Intent: The authoritative corpus slice covering builtin introspection executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"builtins"
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
=== END AC builtins-006-builtins ===

## User Acceptance

- None.

## Guardrails

- Diagnostics must never replace or corrupt JSON values written to stdout.
- Extend the inherited environment when invoking the conformance harness.
- Do not depend on environment variables having values beyond those supplied by the process.
