# FEATURE: Control Reductions

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Accumulate ordered generator streams with reduce and foreach. |
| Depends On | FEATURE-Control-Conditionals.md |
| Provides | reduce, foreach |
| Consumes | ordered generators, bindings, patterns, conditionals, lexical breaks |

## Capability

`reduce` and `foreach` preserve ordered generator, binding, extraction, break, error, partial-output, and backtracking semantics.

## Programmatic Acceptance

=== AC control-reductions-suite ===
Intent: The authoritative corpus executes the reduce and foreach cases owned by this story.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(reduce|foreach)"
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
=== END AC control-reductions-suite ===

=== AC control-reductions-compile-status ===
Intent: Reduce and foreach syntax compile under the jq executable contract.
Requires: executable=python3; scope=test

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "reduce .[] as $item (0; . + $item)"],
    input="[1, 2]\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode != 3
assert result.stderr is not None
=== END AC control-reductions-compile-status ===

## User Acceptance

- None.

## Guardrails

- Reduction inputs must be consumed in generator order.
- Accumulator updates must not alter the original input value.
- Foreach extraction must observe each intermediate accumulator exactly once per input output.
- Break and runtime errors must preserve outputs emitted before termination.
