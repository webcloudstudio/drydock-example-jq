# FEATURE: Generator Errors and Optional Evaluation

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define empty streams, runtime errors, optional evaluation, try/catch, and partial output behavior. |
| Depends On  | ARCHITECTURE.md, FEATURE-CORE-002.md |
| Provides    | empty, error, optional operator, try/catch, partial runtime output |
| Consumes    | ordered generator evaluator |

## Programmatic Acceptance

=== AC core-003-conformance ===
Intent: The executable evaluates optional errors and try/catch while preserving runtime failure distinction.
Suite: scoped

import subprocess

def run(program, input_text="null\n"):
    return subprocess.run(
        ["./jq", "-c", program],
        input=input_text,
        capture_output=True,
        text=True,
    )

optional = run('error("x")?')
assert optional.returncode == 0 and optional.stdout == ""
caught = run('try error("x") catch .')
assert caught.returncode == 0 and caught.stdout == '"x"\n'
uncaught = run('error("x")')
assert uncaught.returncode == 5
=== END AC core-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Preserve generator ordering and values emitted before a runtime failure.
- Do not treat runtime failures as compile failures.
