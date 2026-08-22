# FEATURE: Errors and Optional Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq empty results, runtime errors, optional evaluation, try/catch, and partial output behavior. |
| Depends On  | ARCHITECTURE.md, FEATURE-Generator-Core.md, FEATURE-Composition-And-Cartesian-Evaluation.md, FEATURE-Process-Contract.md |
| Provides    | empty, runtime error propagation, optional filters, try/catch, partial output |
| Consumes    | ordered generators, executable process contract, parsed expressions |

## Scope and Behavior

Runtime evaluation must distinguish an empty generator from a value of `null`. Errors propagate through ordinary evaluation and terminate the process with exit code 5, while `try` and the optional operator suppress or transform errors according to jq semantics.

A filter may emit values before a later runtime error. Those values remain on stdout, diagnostics go to stderr, and the process exits with the runtime-error status. `try EXP catch HANDLER` evaluates the handler with the error value; `try EXP` uses an empty result as its handler. `EXP?` is equivalent to `try EXP`.

## Programmatic Acceptance

=== AC core-003-conformance ===
Intent: The conformance corpus cases exercising try, error, optional evaluation, and partial output execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"try|error|\?"
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC core-003-conformance ===

=== AC core-003-runtime-contract ===
Intent: Runtime failures use the documented runtime exit status while successful optional evaluation completes normally.
import json
import os
import subprocess

program = "try (error(\"x\")) catch ."
input_value = "null\n"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 0
assert result.stderr == ""
assert json.loads(result.stdout) == "x"

program = "1, error(\"x\")"
result = subprocess.run(["./jq", "-c", program], input=input_value, capture_output=True, text=True)
assert result.returncode == 5
assert json.loads(result.stdout.splitlines()[0]) == 1
=== END AC core-003-runtime-contract ===

## User Acceptance

- None.

## Guardrails

- Do not convert `empty` into `null`.
- Do not discard values emitted before a runtime error.
- Do not compare or require diagnostic wording.
- Compile failures remain distinct from runtime failures.
