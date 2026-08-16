# FEATURE: SQL-Style and Introspection Builtins

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Provide SQL-style joins, membership queries, builtin introspection, and module grammar validation. |
| Depends On  | FEATURE-Structural-Builtins.md, FEATURE-Functions-Bindings.md |
| Provides    | INDEX, JOIN, IN, builtins, module grammar validation |
| Consumes    | structural builtins, function registry, declared module exclusions |

## Purpose

Implement `INDEX`, `JOIN`, `IN`, and `builtins`, plus compile-time validation for supported module syntax. Preserve the declared loader exclusions: excluded fixture modules remain skipped, while invalid module grammar is rejected without filesystem access.

## Behavior

- `INDEX` builds an object keyed by the requested index expression.
- `JOIN` combines stream rows with indexed values.
- `IN` tests membership across generated streams.
- `builtins` exposes registered builtin names and arities.
- Invalid module metadata, dynamic import paths, and unsupported module tokens produce compile status 3.
- No excluded fixture module is loaded.

## Programmatic Acceptance

=== AC index-build ===
Intent: INDEX creates lookup entries for every supplied row.

import json
import subprocess

rows = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
result = subprocess.run(["./jq", "-c", "INDEX(.[]; .id)"], input=json.dumps(rows) + "\n", capture_output=True, text=True)
assert result.returncode == 0
actual = json.loads(result.stdout)
assert actual["1"] == rows[0]
assert actual["2"] == rows[1]
=== END AC index-build ===

=== AC membership-stream ===
Intent: IN returns membership results for supplied generated values.

import json
import subprocess

values = [0, 2, 4]
result = subprocess.run(["./jq", "-c", "range(5) | IN(0,2,4)"], input="null\n", capture_output=True, text=True)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [index in values for index in range(5)]
=== END AC membership-stream ===

=== AC module-compile-rejection ===
Intent: Invalid module metadata is rejected with the compile-error status.

import subprocess

program = "module [];"
result = subprocess.run(["./jq", "-c", program], input="null\n", capture_output=True, text=True)
assert result.returncode == 3
=== END AC module-compile-rejection ===

## User Acceptance

- None.

## Guardrails

- Do not load excluded module fixtures.
- Do not alter `sources/exclusions.txt` or the conformance corpus.
- Keep introspection results derived from the actual registered builtin table.
