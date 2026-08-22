# FEATURE: Value Model

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines the immutable jq value model, numeric behavior, special numbers, and JSON conversion support. |
| Depends On  | ARCHITECTURE.md |
| Provides    | null, booleans, numbers, strings, arrays, objects, NaN, infinities, numeric literal preservation |
| Consumes    | interpreter architecture, standard-library numeric and JSON facilities |

## Scope and Behavior

The implementation represents jq null, booleans, numbers, strings, arrays, and objects without third-party dependencies. Values are treated immutably by evaluation and assignment operations.

Numbers support ordinary finite values, NaN, positive infinity, and negative infinity where jq exposes them. Numeric literals retain the precision and representation required by the corpus when no arithmetic conversion occurs; arithmetic may use the implementation's floating-point representation as specified by the source.

JSON conversion must support the corpus's special-number behavior and compact serialization conventions. Structural values remain safe to serialize without cycles.

## Programmatic Acceptance

=== AC value-001-conformance ===
Intent: The conformance corpus cases exercising special numbers and JSON conversion execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"nan|infinite|tojson|fromjson"
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
=== END AC value-001-conformance ===

=== AC value-001-round-trip ===
Intent: A supplied JSON value survives conversion to JSON text and back as the same value.
import json
import subprocess

value = {"a": [1, 2], "b": "text", "ok": True}
source = json.dumps(value, separators=(",", ":")) + "\n"
result = subprocess.run(
    ["./jq", "-c", "tojson | fromjson"],
    input=source,
    capture_output=True,
    text=True,
)
assert result.returncode == 0
assert json.loads(result.stdout) == value
=== END AC value-001-round-trip ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not shell out to jq or use a third-party jq binding.
- Preserve input and generator values without accidental mutation.
