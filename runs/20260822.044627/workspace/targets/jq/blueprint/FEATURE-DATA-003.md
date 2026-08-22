# FEATURE: Object Entry and Containment Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq object-key, entry-conversion, and containment builtins. |
| Depends On  | ARCHITECTURE.md, FEATURE-DATA-002.md |
| Provides    | keys, keys_unsorted, has, in, inside, contains, to_entries, from_entries, with_entries |
| Consumes    | jq value model, comparison and ordering |

## Workflow

Implement key enumeration for arrays and objects, membership predicates, recursive containment and inverse containment, object-to-entry and entry-to-object conversion, and `with_entries` transformations. Preserve jq's key ordering and handling of supported key aliases.

## Programmatic Acceptance

=== AC data-003-conformance ===
Intent: The object-entry, key, membership, and containment slice executes matching corpus cases and passes all selected cases.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"keys|has\(|contains|inside|to_entries|from_entries"
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
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC data-003-conformance ===

## User Acceptance

- None.

## Guardrails

- `keys` must use Unicode codepoint ordering; `keys_unsorted` must preserve insertion-oriented ordering.
- Containment must recurse structurally and must not confuse booleans with numbers.
