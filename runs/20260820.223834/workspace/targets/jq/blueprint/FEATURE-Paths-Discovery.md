# FEATURE: Paths Discovery

| Field | Value |
|-------|-------|
| Version | 20260820 V1 |
| Description | Discover, enumerate, and read values through jq path expressions. |
| Depends On | ARCHITECTURE.md, FEATURE-Core-Utilities.md |
| Provides | path, paths, getpath |
| Consumes | ordered generator evaluation, indexing, recursion, filtering |

## Capability

Path discovery evaluates exact and generated path expressions against immutable jq values. `path`, `paths`, and `getpath` preserve path ordering, generator multiplicity, and jq absent-value behavior.

## Programmatic Acceptance

=== AC paths-discovery-suite ===
Intent: The authoritative corpus executes the path, paths, and getpath cases owned by this story.
Suite: behavioral
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

SELECT = r"(path|paths|getpath)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", SELECT, "--json"],
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
=== END AC paths-discovery-suite ===

=== AC paths-discovery-protocol ===
Intent: Path discovery remains a successful executable jq program under the required interface.
Requires: executable=python3; scope=test

import os
import subprocess

result = subprocess.run(
    ["./jq", "-c", "[paths]"],
    input="[1,[2]]\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
assert result.stderr is not None
=== END AC paths-discovery-protocol ===

## User Acceptance

- None.

## Guardrails

- Do not mutate the input while discovering or reading paths.
- Preserve path ordering and generator multiplicity.
- Do not treat the root path as a member of `paths`.
- Do not resolve excluded module-loader cases through filesystem access.
