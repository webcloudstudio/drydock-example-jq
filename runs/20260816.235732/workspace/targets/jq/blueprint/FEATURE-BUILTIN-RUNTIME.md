# FEATURE: jq Runtime Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Define jq numeric, environment, input/output, debug, and streaming builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-EVAL-CONTROL.md, FEATURE-BUILTIN-STRUCTURAL.md |
| Provides    | numeric and math builtins, env, input, inputs, debug, stderr, tostream, fromstream, builtins |
| Consumes    | generator evaluator, jq value operations |

## Scope

Implement runtime-oriented jq builtins without external dependencies. Numeric behavior follows jq's IEEE-compatible semantics as far as Python standard-library values permit. Environment and I/O behavior remains process-local and diagnostics remain separate from JSON output.

## Behavior

- Numeric predicates and math functions handle finite, infinite, NaN, rounding, and documented domain errors.
- `env` and `$ENV` expose the process environment.
- `input` and `inputs` consume subsequent JSON values from the same input stream.
- `debug` and `stderr` write diagnostics to stderr while preserving the filter's output contract.
- Streaming helpers convert between path/value streams and reconstructed values.
- `builtins` returns function names with arities.

## Programmatic Acceptance

=== AC runtime-numeric ===
Intent: Numeric predicates and arithmetic return state-derived numeric results.
import json
import subprocess

source_value = [-2, 0, 3]
program = "[map(abs), map(isfinite)]"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == [[abs(item) for item in source_value], [True for _ in source_value]]
=== END AC runtime-numeric ===

=== AC runtime-environment ===
Intent: The environment builtin returns an object containing a supplied inherited variable.
import json
import os
import subprocess

name = "JQ_ACCEPTANCE_SENTINEL"
value = "present"
result = subprocess.run(
    ["./jq", "-c", f"env[{json.dumps(name)}]"],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ, name: value},
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC runtime-environment ===

=== AC runtime-inputs ===
Intent: Inputs are consumed in order from the supplied newline-delimited JSON stream.
import json
import subprocess

values = [1, 2, 3]
result = subprocess.run(
    ["./jq", "-c", "inputs"],
    input="".join(json.dumps(value) + "\n" for value in values),
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == values
=== END AC runtime-inputs ===

=== AC runtime-streaming ===
Intent: Streaming conversion round-trips the supplied structure.
import json
import subprocess

source_value = {"a": [1, 2], "b": True}
result = subprocess.run(
    ["./jq", "-c", ". as $x | fromstream($x | tostream)"],
    input=json.dumps(source_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == source_value
=== END AC runtime-streaming ===

## User Acceptance

- None.

## Guardrails

- Diagnostics from `debug` and `stderr` must never corrupt stdout JSON.
- Do not access the network or install packages.
- Preserve input ordering and generator multiplicity.
