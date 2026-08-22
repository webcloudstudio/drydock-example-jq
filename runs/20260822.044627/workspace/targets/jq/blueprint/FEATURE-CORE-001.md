# FEATURE: Stream-Valued Filter Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Evaluate jq filters as ordered streams supporting empty, iteration, and range. |
| Depends On  | ARCHITECTURE.md, FEATURE-PARSE-004.md |
| Provides    | ordered generator evaluator |
| Consumes    | expression AST |

## Scope

Implement the evaluator foundation in which every filter consumes one input and yields an ordered stream of zero or more values. Support identity, literals, empty, array and object iteration, recursive stream propagation, range generation, and preservation of output order and multiplicity.

## Programmatic Acceptance

=== AC core-001-conformance ===
Intent: The executable evaluates identity, empty, range, and generator ordering as ordered streams.
Suite: scoped
Requires: executable=python3; scope=test

import subprocess

def run(program, input_text="null\n"):
    return subprocess.run(
        ["./jq", "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
    )

identity = run(".")
assert identity.returncode == 0 and identity.stdout == "null\n"
assert run("empty").returncode == 0 and run("empty").stdout == ""
assert run("range(3)").stdout == "0\n1\n2\n"
=== END AC core-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Never collapse a generator to a single value.
- Preserve backtracking, multiplicity, and partial stream order.
- Avoid external runtimes and third-party jq implementations.
