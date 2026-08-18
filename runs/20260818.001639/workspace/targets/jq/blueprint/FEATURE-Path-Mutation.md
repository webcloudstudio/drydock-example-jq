# FEATURE: Path Mutation

| Field       | Value |
|-------------|-------|
| Version     | 20260818 V1 |
| Description | Provide jq nested path mutation and deletion operations. |
| Depends On  | FEATURE-Path-Discovery.md |
| Provides    | setpath, delpaths, del |
| Consumes    | path, paths, getpath, immutable JSON values |

## Purpose

Implement immutable updates and deletion for nested objects, arrays, slices, and generated paths.

## Behavior

- `setpath` creates or replaces nested containers as required by the target path.
- Array paths support valid indices, growth with null padding, and jq-compatible negative-index behavior.
- `delpaths` removes multiple paths while preserving unrelated values.
- `del` converts a path expression into deletion operations.
- Missing deletion targets are harmless where jq specifies no-op behavior.
- Invalid path types, excessive paths, and invalid container/index combinations raise runtime errors.
- Every operation returns a new JSON value and leaves the original evaluation value unchanged.

## Programmatic Acceptance

=== AC path-mutation-suite ===
Intent: The implementation passes the authoritative conformance cases for setpath, delpaths, and del.
Suite: scoped

import os
import subprocess
import sys

selector = r"^(setpath\(|delpaths\(|del\()|(^|[^A-Za-z])(setpath|delpaths|del)\b"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC path-mutation-suite ===

=== AC path-mutation-errors ===
Intent: The implementation passes authoritative invalid-path mutation cases with the required runtime outcomes.
Suite: scoped

import os
import subprocess
import sys

selector = r"(Cannot update|Cannot set|Out of bounds|Path too deep|delpaths|setpath)"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--list", "--select", selector],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC path-mutation-errors ===

## User Acceptance

- None.

## Guardrails

- Apply mutations immutably.
- Do not broaden deletion or replacement beyond the paths selected by the expression.
- Preserve jq runtime error status and partial output behavior.
