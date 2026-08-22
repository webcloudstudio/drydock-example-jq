# FEATURE: Sorting and Grouping

Sorting, grouping, uniqueness, and extrema use jq structural comparison.

## Programmatic Acceptance

=== AC data-002-conformance ===
import json
import os
import subprocess
import sys

SELECT = r"sort|group_by|unique|min|max"

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
tally = report["summary"]
assert sum(tally.values()) > 0, f"selector matched no case: {SELECT}"
assert tally["fail"] == 0 and tally["error"] == 0, tally
assert result.returncode == 0, result.returncode
=== END AC data-002-conformance ===
