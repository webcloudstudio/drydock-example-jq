# FEATURE: jq Parser

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Grammar, precedence, and AST construction for jq programs. |
| Depends On  | FEATURE-Frontend-Lexer.md, ARCHITECTURE.md |
| Provides    | jq parser, jq AST |
| Consumes    | jq lexer |

## Capability

The parser implements jq expressions, filters, function and module declarations, bindings, patterns, indexing, construction, operators, conditionals, error forms, and generator syntax. It applies the precedence and associativity defined by `sources/parser.y`, constructs an AST, and rejects syntactically invalid programs with compile exit status `3`.

## Programmatic Acceptance

=== AC parser-invalid-programs ===
Intent: The parser rejects malformed object and expression syntax with compile exit status 3.

import os
import subprocess

programs = ["{", "}", "break $out"]
for program in programs:
    result = subprocess.run(
        ["./jq", "-c", program],
        input="null\n",
        capture_output=True,
        text=True,
        env={**os.environ},
    )
    assert result.returncode == 3
=== END AC parser-invalid-programs ===

=== AC parser-precedence ===
Intent: The parser accepts operator precedence and grouping syntax.

import os
import subprocess

program = "1 + 2 * 2 + 10 / 2"
result = subprocess.run(
    ["./jq", "-c", program],
    input="null\n",
    capture_output=True,
    text=True,
    env={**os.environ},
)
assert result.returncode == 0
=== END AC parser-precedence ===

=== AC parser-conformance ===
Intent: Executed conformance cases exercising parser constructs pass without failures or errors.

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"^(module |include |def |if |try |reduce |foreach |.*\?//)"
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
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0
=== END AC parser-conformance ===

## User Acceptance

- None.

## Guardrails

- Follow `sources/parser.y` for precedence, associativity, and syntax.
- Keep compile errors distinct from runtime errors.
- Do not access module files for grammar-only rejection cases.
