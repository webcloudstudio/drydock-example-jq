# FEATURE: Source Staging

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Preserves the supplied jq specifications, corpus, exclusions, and scoring harness under sources/. |
| Depends On  | ARCHITECTURE.md |
| Provides    | staged jq source and scoring assets |
| Consumes    | supplied source inventory |

## Purpose

Make every imported source available beneath `sources/` in the application root without altering its contents. These files are read-only reference and scoring assets during implementation.

## Staged Assets

The following files must be present verbatim:

- `sources/INSTRUCTIONS.md`
- `sources/builtin.jq`
- `sources/exclusions.txt`
- `sources/full_test.sh`
- `sources/jq-manual.txt`
- `sources/jq.test`
- `sources/lexer.l`
- `sources/parser.y`
- `sources/run_conformance.py`

The corpus, exclusions, runner, and full-test script are protected scoring assets. They must not be filtered, shortened, rewritten, or replaced.

## Programmatic Acceptance

=== AC staging-complete ===
Intent: Every declared source asset is staged at its required build-relative path.
from pathlib import Path

paths = [
    "sources/INSTRUCTIONS.md",
    "sources/builtin.jq",
    "sources/exclusions.txt",
    "sources/full_test.sh",
    "sources/jq-manual.txt",
    "sources/jq.test",
    "sources/lexer.l",
    "sources/parser.y",
    "sources/run_conformance.py",
]
assert all(Path(path).is_file() for path in paths)
=== END AC staging-complete ===

=== AC staging-nonempty ===
Intent: Every staged source asset contains imported content.
from pathlib import Path

paths = [
    "sources/INSTRUCTIONS.md",
    "sources/builtin.jq",
    "sources/exclusions.txt",
    "sources/full_test.sh",
    "sources/jq-manual.txt",
    "sources/jq.test",
    "sources/lexer.l",
    "sources/parser.y",
    "sources/run_conformance.py",
]
assert all(Path(path).stat().st_size > 0 for path in paths)
=== END AC staging-nonempty ===

=== AC staging-harness-executable ===
Intent: The supplied scoring entry point is executable by POSIX sh.
import subprocess

result = subprocess.run(
    ["sh", "sources/full_test.sh", "--help"],
    capture_output=True,
    text=True,
)
assert result.returncode != 127
=== END AC staging-harness-executable ===

## User Acceptance

- None.

## Guardrails

- Preserve all listed assets byte-for-byte.
- Do not alter exclusions or reinterpret corpus cases.
- Do not add filters, skips, redirects, or alternate scoring commands.
