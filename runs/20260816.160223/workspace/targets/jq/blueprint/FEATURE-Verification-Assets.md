# FEATURE: Verification Assets

| Field       | Value |
|-------------|-------|
| Version     | 20260816 V1 |
| Description | Preserve the supplied jq specifications, corpus, exclusions, and conformance harness under sources. |
| Depends On  | ARCHITECTURE.md |
| Provides    | sources/jq.test, sources/run_conformance.py, sources/full_test.sh, sources/exclusions.txt, sources/jq-manual.txt, sources/parser.y, sources/lexer.l, sources/builtin.jq |
| Consumes    | supplied source assets |

## Scope

Stage each supplied asset byte-for-byte at its documented build-relative path under `sources/`. The corpus, exclusions, scoring script, and conformance runner are read-only grading assets and must remain unchanged.

## Programmatic Acceptance

- None. This is a governed byte-for-byte staging operation; Drydock verifies the declared copies and the terminal conformance story executes the preserved harness.

## User Acceptance

- None.

## Guardrails

- Do not modify `sources/jq.test`, `sources/run_conformance.py`, `sources/full_test.sh`, or `sources/exclusions.txt`.
- Do not filter, skip, reinterpret, or rewrite corpus cases.
- Do not add module-loader exclusions beyond the supplied exclusions file.
