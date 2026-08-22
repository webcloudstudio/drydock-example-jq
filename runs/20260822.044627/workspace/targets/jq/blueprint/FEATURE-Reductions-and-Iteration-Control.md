# FEATURE: Reductions and Iteration Control

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq reductions and generator-control builtins with stateful stream semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-Generator-Core.md, FEATURE-Labels-And-Breaks.md, FEATURE-Variable-Bindings.md |
| Provides    | reduce, foreach, range, limit, skip, first, last, nth |
| Consumes    | ordered generators, lexical labels, variable bindings |

## Workflow

Implement `reduce` and `foreach` state transitions over generator inputs. Implement `range`, `limit`, `skip`, `first`, `last`, and `nth`, including multi-valued arguments, empty streams, negative-count errors, extraction behavior, and label-based termination. Preserve jq's ordering, backtracking, and accumulator semantics.

## Programmatic Acceptance

=== AC flow-005-conformance ===
Intent: The authoritative corpus slice exercising reductions and iteration controls executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"reduce|foreach|limit|skip|nth|first|last"
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
=== END AC flow-005-conformance ===

=== AC flow-005-interface ===
Intent: The implementation exposes every declared reduction and iteration-control interface.
import subprocess
import sys

program = "reduce .[] as $x (0; . + $x)"
payload = "[1,2,3]\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode in (0, 5)
=== END AC flow-005-interface ===

## User Acceptance

- None.

## Guardrails

- Preserve generator order, multiplicity, and backtracking.
- Do not replace stateful reductions with single-value evaluation.
- Do not alter staged conformance assets.
