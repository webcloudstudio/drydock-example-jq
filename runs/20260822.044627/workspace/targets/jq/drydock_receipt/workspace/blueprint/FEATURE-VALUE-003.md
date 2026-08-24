# FEATURE: Slices and Collection Iteration

| Field       | Value |
|-------------|-------|
| Version     | 20220822 V1 |
| Description | Define array and string slicing together with array and object value iteration. |
| Depends On  | FEATURE-VALUE-002.md |
| Provides    | array slices, string slices, array iteration, object iteration |
| Consumes    | field and index access |

## Programmatic Acceptance

=== AC value-003-conformance ===
Intent: The authoritative corpus cases exercising slices and collection iteration execute successfully.
Suite: scoped

import json
import os
import subprocess
import sys

select = r"\[.*:|\.\[\]"
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
=== END AC value-003-conformance ===

## User Acceptance

- None.

## Guardrails

- Iteration preserves ordering and emits one value per selected element.
- Out-of-range slices produce valid empty or truncated results according to jq semantics.
- Optional iteration suppresses invalid-input errors while retaining valid outputs.
