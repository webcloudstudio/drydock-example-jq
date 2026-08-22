# FEATURE: Object Entries And Containment

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq key, membership, containment, and object-entry conversion builtins. |
| Depends On  | FEATURE-Field-And-Index-Access.md, FEATURE-Truthiness-And-Comparison.md, FEATURE-Collection-Transformations.md |
| Provides    | keys, keys_unsorted, has, in, inside, contains, to_entries, from_entries, with_entries |
| Consumes    | value access, equality, collection transformations |

## Workflow

Implement key enumeration for arrays and objects, membership predicates, recursive containment and inverse containment, and conversion between objects and entry arrays. Support the documented key aliases in `from_entries` and preserve object semantics through `with_entries`.

## Programmatic Acceptance

=== AC data-003-conformance ===
Intent: The authoritative corpus slice covering keys, membership, containment, and entries executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

selector = r"keys|has\(|contains|inside|to_entries|from_entries"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
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

- `keys` sorts object keys by Unicode codepoint; `keys_unsorted` preserves insertion order.
- Containment is recursive and type-sensitive.
- Missing fields and invalid access follow established jq runtime semantics.
