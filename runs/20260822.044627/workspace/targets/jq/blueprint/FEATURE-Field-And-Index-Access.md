# FEATURE: Field and Index Access

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines jq object-field, array-index, string-index, optional-access, and negative-index behavior. |
| Depends On  | ARCHITECTURE.md, FEATURE-Value-Model.md, FEATURE-Generator-Core.md, FEATURE-Filter-Grammar.md |
| Provides    | object fields, array indices, string indices, optional access, negative indices, missing values |
| Consumes    | jq values, generator evaluation, parsed access expressions |

## Scope and Behavior

Identifier fields such as `.foo` access object keys and return `null` for missing object fields. Bracket access supports computed string keys, array indices, and string indices. Array indices are zero-based and accept negative values when in range.

Accessing an invalid type or invalid index raises a runtime error unless the expression uses `?`, in which case the error is suppressed. Missing array elements and missing object fields follow jq's documented null behavior. Access must preserve generator ordering when the key or index expression produces multiple values.

## Programmatic Acceptance

=== AC value-002-conformance ===
Intent: The conformance corpus cases exercising field and index access execute and pass.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\.[A-Za-z]|\[[-0-9]"
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
=== END AC value-002-conformance ===

=== AC value-002-access ===
Intent: Field, negative-index, missing-field, and optional access behave through the executable interface.
import json
import subprocess

input_value = {"items": [10, 20, 30], "name": "jq"}
source = json.dumps(input_value) + "\n"
program = "[.name, .missing, .items[-1], .items[99]?]"
result = subprocess.run(["./jq", "-c", program], input=source, capture_output=True, text=True)
assert result.returncode == 0
assert json.loads(result.stdout) == ["jq", None, 30, None]
=== END AC value-002-access ===

## User Acceptance

- None.

## Guardrails

- Do not treat absent fields as Python exceptions when jq requires `null`.
- Do not confuse boolean indices with numeric indices.
- Optional access suppresses runtime errors without suppressing valid null results.
