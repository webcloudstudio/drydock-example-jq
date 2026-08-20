# jq

A standalone Python implementation of the jq language.

| Field       | Value |
|-------------|-------|
| Name        | jq |
| Display Name | jq Interpreter |
| Description | A standalone jq interpreter with a root-level executable interface. |
| Status      | planned |
| Stack       | Python 3.11+ standard library; POSIX sh |
| Code Root   | application root |
| Executable  | ./jq |

## Intent

The application reads newline-delimited JSON from standard input, evaluates a jq filter supplied with `-c`, and writes compact JSON values to standard output, one per line. It must pass the supplied jq 1.8.2 conformance corpus without third-party dependencies or network access.

## Programmatic Acceptance

=== AC metadata-contract ===
Intent: Project metadata declares the executable interface and approved runtime stack.

from pathlib import Path

text = Path("METADATA.md").read_text(encoding="utf-8")
assert "./jq" in text
assert "Python" in text
assert "standard library" in text
=== END AC metadata-contract ===

=== AC metadata-interface ===
Intent: Project metadata records the required compact-filter command shape.

from pathlib import Path

text = Path("METADATA.md").read_text(encoding="utf-8")
assert "-c" in text
assert "standard input" in text
assert "standard output" in text
=== END AC metadata-interface ===

## User Acceptance

- None.

## Guardrails

- No third-party runtime dependency or network access.
- The deliverable executable is named `jq` and resides at the application root.
