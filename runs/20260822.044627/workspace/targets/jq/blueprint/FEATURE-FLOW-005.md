# FEATURE: Reductions and Iteration Controls

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq reductions and generator iteration-control builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-FLOW-004.md |
| Provides    | reduce, foreach, range, limit, skip, first, last, nth |
| Consumes    | ordered generator evaluator, lexical labels, variable bindings |

## Workflow

Reduction and iteration controls consume ordered generator streams and preserve jq's state, ordering, Cartesian argument, backtracking, and short-circuit semantics.

- `reduce EXP as $var (INIT; UPDATE)` accumulates each generated value.
- `foreach EXP as $var (INIT; UPDATE; EXTRACT)` emits intermediate extracted values.
- `range` supports one, two, and three argument forms.
- `limit`, `skip`, `first`, `last`, and `nth` operate on generated streams.
- Invalid negative counts for `limit`, `skip`, and `nth` raise runtime errors.

## Programmatic Acceptance

=== AC flow-005-conformance ===
Intent: The executable passes the authoritative conformance cases exercising reductions and iteration controls.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"reduce|foreach|limit|skip|nth|first|last"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
tally = report["summary"]
assert sum(tally.values()) > 0
assert tally["fail"] == 0 and tally["error"] == 0
assert result.returncode == 0
=== END AC flow-005-conformance ===

## User Acceptance

- Reduction and iteration filters preserve output ordering and generator multiplicity.

## Guardrails

- Do not replace generator evaluation with single-value evaluation.
- Preserve runtime errors and partial output semantics.
