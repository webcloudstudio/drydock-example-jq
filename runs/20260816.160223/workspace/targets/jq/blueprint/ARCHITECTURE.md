# ARCHITECTURE: jq Interpreter

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Architecture for a self-contained Python standard-library implementation of jq 1.8.2 semantics. |
| Depends On  | COMPASS.md, TECHNOLOGY_STACK.md |
| Provides    | interpreter module boundaries, executable architecture |
| Consumes    | — |

## Intent

The project delivers a root-level executable named `jq`. It accepts the exercised `./jq -c '<program>'` interface, reads JSON values from standard input, evaluates jq filters as ordered streams, and writes compact JSON values one per line.

## Architecture

The executable wrapper delegates to adjacent Python modules with these boundaries:

| Module area | Responsibility |
|---|---|
| CLI | Argument validation, JSON input loop, compact output, exit-code mapping |
| Lexer | jq tokens, strings, interpolation, comments, literals, operators, and delimiters |
| Parser | Precedence-aware AST construction and compile-time validation |
| Values | JSON values, numeric literal preservation, comparison, serialization |
| Evaluator | Ordered generator streams, backtracking, pipelines, commas, and cartesian evaluation |
| Control | Errors, catches, reductions, recursion, labels, and bounded generators |
| Paths | Path discovery, lookup, immutable mutation, deletion, and assignments |
| Builtins | jq standard functions, formats, regex, dates, traversal, and streaming |

The evaluator is stream-valued: every filter consumes one input and may produce zero, one, or many outputs. Downstream filters execute once for each upstream output, preserving generator ordering and outputs produced before runtime errors.

## Error Model

Compilation and static validation failures terminate with exit code `3`. Runtime failures terminate with exit code `5`; values already emitted remain on stdout. Diagnostics are written to stderr and are not part of the output contract.

## Technology Stack

- Python 3.11 or newer, using only the standard library.
- POSIX `sh` for the supplied verification entry point.
- No package installation, network access, third-party jq implementation, jq binding, or system jq subprocess.

## Source and Harness Boundary

The supplied assets under `sources/` are read-only conformance inputs. The implementation may consult the manual, lexer, parser grammar, builtin definitions, corpus, exclusions, and harness, but must not modify them. Module-loader cases remain excluded only where declared by `sources/exclusions.txt`.

## Programmatic Acceptance

=== AC architecture-runtime ===
Intent: The implementation architecture exposes a runnable root-level jq executable using the declared Python standard-library boundary.

from pathlib import Path
import subprocess
import sys

executable = Path("jq")
assert executable.is_file()
assert executable.stat().st_mode & 0o111
result = subprocess.run(
    [sys.executable, str(executable), "-c", "."],
    input="null\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
=== END AC architecture-runtime ===

=== AC architecture-stream ===
Intent: The architecture preserves the ordered multi-output generator contract.

import json
import subprocess
import sys

source = "[.[]]"
input_value = [1, 2, 3]
result = subprocess.run(
    [sys.executable, "jq", "-c", source],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [input_value]
=== END AC architecture-stream ===

=== AC architecture-dependencies ===
Intent: The executable runs without requiring third-party runtime packages or network access.

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "jq", "-c", "."],
    input="{}\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
=== END AC architecture-dependencies ===

## User Acceptance

- None.

## Guardrails

- The interpreter must never shell out to a system jq binary.
- Runtime behavior must use only Python standard-library facilities.
- Generator ordering, backtracking, compile/runtime exit distinctions, and prior outputs must be preserved.
- Supplied corpus, exclusions, scoring script, and conformance runner remain unchanged.
