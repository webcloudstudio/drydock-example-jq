# FEATURE: Destructuring Patterns

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Defines array and object destructuring bindings and alternative matching. |
| Depends On  | FEATURE-Variable-Bindings.md, FEATURE-Conditionals-And-Exception-Flow.md, FEATURE-Declarations-And-Control-Syntax.md |
| Provides    | Array patterns, object patterns, missing bindings, ?// alternatives |
| Consumes    | Lexical bindings, generator errors, function scope |

## Purpose

Support jq destructuring patterns in `as` bindings and the `?//` destructuring alternative operator.

Array patterns bind positional elements, using `null` for missing positions. Object patterns bind named fields, including nested patterns and renamed fields. Alternative patterns retry when matching or downstream evaluation fails, exposing unmatched variables as `null`.

## Implementation Requirements

- Parse array and object patterns with nested patterns.
- Bind variables lexically for the remainder of the query.
- Preserve generator ordering and backtracking.
- Implement `?//` alternatives, including retry after downstream errors.
- Reject malformed patterns and undefined bindings at compile time.
- Preserve `null` bindings for variables absent from the successful alternative.

## Programmatic Acceptance

=== AC destructuring-conformance ===
Intent: The authoritative corpus slice covering destructuring syntax and alternatives executes and passes.
Suite: scoped
Requires: executable=python3; scope=test

import json
import os
import subprocess
import sys

select = r"\?//| as \{"
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
=== END AC destructuring-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not treat destructuring bindings as mutable variables.
- Do not retry an alternative after a successful alternative completes without error.
- Do not load module fixtures while parsing or evaluating destructuring syntax.
