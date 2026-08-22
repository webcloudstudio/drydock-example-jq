# FEATURE: Conditionals and Exceptions

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Define jq conditional branching, optional evaluation, try/catch, and runtime error propagation. |
| Depends On  | FEATURE-Boolean-and-Alternative-Operators.md, FEATURE-Error-and-Optional-Evaluation.md |
| Provides    | if, elif, else, try, catch, optional branches |
| Consumes    | boolean and alternative operators, generator evaluation, runtime diagnostics |

## Intent

This capability controls branching and exception flow across jq's ordered generator streams.

## Behavior

- `if`, `elif`, and `else` evaluate branches according to jq false/null truthiness.
- Multiple condition outputs independently select branches.
- An omitted `else` behaves as the identity filter.
- `try EXP catch HANDLER` catches runtime errors and evaluates the handler with the error value.
- `try EXP` suppresses errors as `empty`.
- The `?` suffix provides optional evaluation.
- Outputs emitted before an uncaught runtime error remain on stdout and the process exits 5.

## Programmatic Acceptance

=== AC flow-003-conformance ===
Intent: Conditionals and exception handling produce the declared branch and error behavior.
import json
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", "if . then \"yes\" else \"no\" end"],
    input="false\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == "no"

result = subprocess.run(
    ["./jq", "-c", "try error(\"boom\") catch ."],
    input="null\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == "boom"
=== END AC flow-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Compile errors must remain distinct from runtime errors.
- Error messages are diagnostic only; acceptance relies on exit status and structured outputs.
- Preserve partial output before an uncaught runtime failure.
