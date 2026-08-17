# FEATURE: jq Paths and Assignment

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Define jq path discovery, access, deletion, and immutable assignment semantics. |
| Depends On  | ARCHITECTURE.md, FEATURE-LANG-BINDINGS.md, FEATURE-EVAL-VALUES.md |
| Provides    | path, getpath, setpath, delpaths, del, plain assignment, update assignment, arithmetic assignment |
| Consumes    | generator evaluator, jq bindings, jq value operations |

## Purpose

This capability implements jq's path model and all assignment forms. Values remain immutable from the language user's perspective; each assignment evaluates against the original input and emits a modified value.

## Behavior

- `path`, `getpath`, `setpath`, `delpaths`, and `del` operate on arrays of string and integer path components.
- Missing object and array intermediates are created according to jq semantics.
- Negative array indices address existing elements where supported; invalid mutation indices raise runtime errors.
- Plain assignment evaluates the right-hand side against the original input and emits one result per right-hand-side output.
- Update assignment evaluates the right-hand side against each selected old value and uses its first output; `empty` deletes the selected path.
- `+=`, `-=`, `*=`, `/=`, `%=`, and `//=` are update assignments.
- Generated paths and multiple selected paths preserve jq order and multiplicity.

## Programmatic Acceptance

=== AC paths-roundtrip ===
Intent: Path access and mutation produce the supplied value through the public executable.
import json
import subprocess

path = ["a", "b"]
value = 7
source = json.dumps({"a": {"b": 0}})
program = f"setpath({json.dumps(path)}; {value}) | getpath({json.dumps(path)})"
result = subprocess.run(["./jq", "-c", program], input=source + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual == value
=== END AC paths-roundtrip ===

=== AC paths-delete ===
Intent: Deleting a supplied path removes that path while retaining unrelated state.
import json
import subprocess

source_value = {"a": 1, "b": 2}
deleted_key = "a"
program = f"del(.{deleted_key})"
result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
expected = dict(source_value)
expected.pop(deleted_key)
assert actual == expected
=== END AC paths-delete ===

=== AC assignment-operators ===
Intent: Plain, update, and arithmetic assignments update the selected field.
import json
import subprocess

source_value = {"n": 2}
programs = [".n = 4", ".n |= . + 1", ".n += 3"]
expected_values = [{"n": 4}, {"n": 3}, {"n": 5}]
for program, expected in zip(programs, expected_values):
    result = subprocess.run(["./jq", "-c", program], input=json.dumps(source_value) + "\n", capture_output=True, text=True)
    assert result.returncode == 0
    assert json.loads(result.stdout) == expected
=== END AC assignment-operators ===

=== AC assignment-errors ===
Intent: Invalid path mutations report the documented runtime failure status.
import subprocess

result = subprocess.run(["./jq", "-c", "try (.[-2] = 0) catch ."], input="[]\n", capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) is not None

result = subprocess.run(["./jq", "-c", ".[-2] = 0"], input="[]\n", capture_output=True, text=True)
assert result.returncode == 5
=== END AC assignment-errors ===

## User Acceptance

- None.

## Guardrails

- Do not mutate input values in place.
- Do not shell out to another jq implementation.
- Preserve path order, generator multiplicity, and stderr-only diagnostics.
