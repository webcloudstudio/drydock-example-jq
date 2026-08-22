# FEATURE: Field and Index Access

| Field       | Value |
|-------------|-------|
| Version     | 20220822 V1 |
| Description | Define object field access, array and string indexing, optional access, and missing-value behavior. |
| Depends On  | FEATURE-VALUE-001.md |
| Provides    | field access, index access, optional access, negative indices, missing values |
| Consumes    | ordered generator evaluator, jq value model |

## Programmatic Acceptance

=== AC value-002-conformance ===
Intent: The authoritative corpus cases exercising field and index access execute successfully.
Suite: scoped

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
tally = report["summary"]
assert sum(tally.values()) > 0
assert tally["fail"] == 0 and tally["error"] == 0
assert result.returncode == 0
=== END AC value-002-conformance ===

## User Acceptance

- None.

## Guardrails

- Missing object fields produce `null`.
- Optional access suppresses access errors without suppressing valid outputs.
- Negative array indices follow jq's end-relative indexing semantics.
