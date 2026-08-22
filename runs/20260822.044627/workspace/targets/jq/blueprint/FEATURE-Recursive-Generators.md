# FEATURE: Recursive Generators

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq recursive generator primitives and recursive descent. |
| Depends On  | ARCHITECTURE.md, FEATURE-Conditionals-And-Exception-Flow.md, FEATURE-Reductions-And-Iteration-Control.md, FEATURE-Function-Definitions-And-Recursion.md |
| Provides    | while, until, repeat, recurse, recursive descent |
| Consumes    | generator evaluation, conditionals, user-defined functions |

## Workflow

Implement `while`, `until`, `repeat`, and the zero-argument and parameterized forms of `recurse`. Support recursive descent through `..`, stream-valued updates, termination conditions, error termination for `repeat`, and recursion without incorrect output suppression or duplication.

## Programmatic Acceptance

=== AC flow-006-conformance ===
Intent: The authoritative corpus slice exercising recursive generators executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"while|until|recurse|repeat"
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
=== END AC flow-006-conformance ===

=== AC flow-006-interface ===
Intent: The recursive generator interface executes a terminating recursive transformation.
import subprocess

program = "[while(. < 4; . + 1)]"
payload = "1\n"
result = subprocess.run(
    ["./jq", "-c", program],
    input=payload,
    capture_output=True,
    text=True,
)
assert result.returncode in (0, 5)
=== END AC flow-006-interface ===

## User Acceptance

- None.

## Guardrails

- Ensure recursive generators terminate according to their conditions or caught errors.
- Preserve every generated value in order.
- Do not introduce external runtimes or modify staged sources.
