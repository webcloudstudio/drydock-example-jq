# FEATURE: Project Interface Documentation

| Field       | Value |
|-------------|-------|
| Version     | 20260821 V1 |
| Description | Documents the jq executable interface, exit statuses, and conformance verification command. |
| Depends On  | FEATURE-FOUNDATION-002.md |
| Provides    | README.md project interface documentation |
| Consumes    | executable jq, sources/full_test.sh |

## Scope

The project README documents the supported `./jq -c '<program>'` invocation, JSON stdin/stdout behavior, compile and runtime exit statuses, standard-library-only implementation constraint, and the supplied verification command `sh sources/full_test.sh`.

## Programmatic Acceptance

=== AC readme-interface ===
Intent: README.md records the complete executable interface contract.

from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
required_tokens = [
    "./jq -c",
    "stdin",
    "stdout",
    "exit",
    "3",
    "5",
    "sh sources/full_test.sh",
]
assert all(token in readme for token in required_tokens)
=== END AC readme-interface ===

=== AC readme-verification-command ===
Intent: README.md identifies the supplied conformance command as the project verification entry point.

from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
verification_command = "sh sources/full_test.sh"
assert verification_command in readme
assert Path("sources/full_test.sh").is_file()
=== END AC readme-verification-command ===

## User Acceptance

- The README is concise and sufficient for a developer to invoke and verify the executable.

## Guardrails

- Documentation must not claim support for command-line options beyond the exercised `-c` contract.
- The README must not instruct users to modify supplied scoring assets.
