# FEATURE: CLI Documentation

| Field       | Value |
|-------------|-------|
| Version     | 20260817 V1 |
| Description | Documents the jq executable interface and verification command. |
| Depends On  | FEATURE-CLI-Entrypoint.md, FEATURE-CLI-Exit-Semantics.md |
| Provides    | README command-line documentation |
| Consumes    | executable jq |

## Intent

The project README concisely documents invocation as `./jq -c '<program>'`, JSON input from standard input, compact JSON outputs on standard output, exit codes `0`, `3`, and `5`, and the supplied verification command `sh sources/full_test.sh`.

## Programmatic Acceptance

=== AC cli-documentation-content ===
Intent: README documents the required command-line contract and verification command.

from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
required_terms = [
    "./jq -c",
    "standard input",
    "standard output",
    "exit",
    "sh sources/full_test.sh",
]
for term in required_terms:
    assert term in readme
=== END AC cli-documentation-content ===

=== AC cli-documentation-statuses ===
Intent: README documents all three required exit statuses.

from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
for status in ("0", "3", "5"):
    assert status in readme
=== END AC cli-documentation-statuses ===

## User Acceptance

- None.

## Guardrails

- Documentation must not claim unsupported command-line options or external dependencies.
