# FEATURE: IO Input Diagnostics

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Provides jq additional-input, diagnostic, environment, and source-location builtins. |
| Depends On  | FEATURE-Flow-Control-Errors.md, FEATURE-Builtin-Format-Conversion.md |
| Provides    | input, inputs, debug, stderr, env, $ENV, $__loc__ |
| Consumes    | executable jq, generator evaluator |

## Behavior

The interpreter supports consuming additional newline-delimited JSON inputs, exposing the process environment, emitting diagnostics to stderr, and producing source-location objects. Diagnostic side effects must not corrupt JSON values emitted on stdout.

## Programmatic Acceptance

=== AC io-inputs ===
Intent: inputs consumes all JSON values after the first input.
import json
import subprocess

values = [1, 2, 3]
expected = values[1:]
result = subprocess.run(
    ["./jq", "-c", "inputs"],
    input="\n".join(json.dumps(value) for value in values) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert [json.loads(line) for line in result.stdout.splitlines()] == expected
=== END AC io-inputs ===

=== AC io-environment ===
Intent: env exposes an environment mapping containing a supplied variable.
import json
import os
import subprocess

name = "JQ_ACCEPTANCE_MARKER"
value = "present"
result = subprocess.run(
    ["./jq", "-c", "env"],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ, name: value},
)
assert result.returncode == 0
assert json.loads(result.stdout)[name] == value
=== END AC io-environment ===

=== AC io-debug-stderr ===
Intent: debug preserves the input value on stdout while writing diagnostics separately.
import json
import subprocess

value = {"message": "debug"}
result = subprocess.run(
    ["./jq", "-c", "debug"],
    input=json.dumps(value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
assert result.stderr
=== END AC io-debug-stderr ===

=== AC io-location ===
Intent: The location builtin returns a structured file and line value.
import json
import subprocess

result = subprocess.run(
    ["./jq", "-c", "$__loc__"],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
location = json.loads(result.stdout)
assert set(location) == {"file", "line"}
assert isinstance(location["file"], str)
assert isinstance(location["line"], int)
=== END AC io-location ===

## User Acceptance

- None.

## Guardrails

- Diagnostics are written to stderr and never replace or contaminate stdout JSON values.
