# FEATURE: Path Mutation and Deletion

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Defines immutable path creation, replacement, deletion, and nested update behavior. |
| Depends On  | FEATURE-PATHS-001.md |
| Provides    | setpath, delpaths, del, immutable nested updates and deletion |
| Consumes    | path discovery and getpath |

## Intent

Implement `setpath`, `delpaths`, and `del` over immutable jq values. Support nested object and array creation, array growth with null padding, slices, negative indices, multiple paths, and deletion without modifying the original input.

## Behavior

- `setpath` creates missing containers according to path components.
- `delpaths` removes each requested path and safely ignores absent paths where jq specifies.
- `del` converts path expressions to deletion paths.
- Multiple deletions are applied with jq's ordering and coalescing semantics.
- Invalid path types and out-of-bounds operations produce runtime errors.

## Programmatic Acceptance

=== AC paths-002-conformance ===
Intent: The path mutation and deletion corpus slice executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"setpath|delpaths|del\("
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
=== END AC paths-002-conformance ===

=== AC paths-002-nested-creation-and-errors ===
Intent: The mutation slice covers nested creation, deletion, array growth, and invalid-path errors.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"setpath\(\[|delpaths\(\[|try delpaths|try setpath"
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
=== END AC paths-002-nested-creation-and-errors ===

## User Acceptance

- None.

## Guardrails

- Treat jq values as immutable; each mutation produces a new value.
- Do not silently convert invalid path components into object keys.
- Preserve deletion ordering and generator multiplicity.
