# FEATURE: jq Values and Numeric Model

| Field       | Value |
|-------------|-------|
| Version     | 20220822 V1 |
| Description | Define jq's JSON value kinds, special numeric values, and numeric serialization behavior. |
| Depends On  | FEATURE-CORE-004.md |
| Provides    | null, boolean, number, string, array, object, NaN, infinity values |
| Consumes    | JSON input reader |

## Programmatic Acceptance

=== AC value-001-conformance ===
Intent: The authoritative corpus cases exercising jq values and special numeric behavior execute successfully.
Suite: scoped

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
tally = report["summary"]
assert sum(tally.values()) > 0
assert tally["fail"] == 0 and tally["error"] == 0
assert result.returncode == 0
=== END AC value-001-conformance ===

## User Acceptance

- None.

## Guardrails

- Use only Python standard-library facilities.
- Do not introduce a third-party jq value implementation or external runtime.
- Serialize non-finite values according to jq behavior rather than emitting invalid JSON tokens.
