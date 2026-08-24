# FEATURE: Scoped Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides executable, machine-readable scoped conformance verification. |
| Depends On  | ARCHITECTURE.md, FEATURE-CONF-001.md |
| Provides    | scoped conformance execution with JQ candidate binding |
| Consumes    | ./jq, sources/run_conformance.py |

## Workflow

Scoped verification invokes the supplied runner against a construct selector, extends the inherited environment with the candidate executable through `JQ`, parses the runner's JSON report, and requires every selected case to pass without errors.

## Programmatic Acceptance

=== AC conf-002-scoped-run ===
Intent: The scoped verification assets expose the candidate binding and machine-readable selector contracts.
Suite: scoped

from pathlib import Path

runner = Path("sources/run_conformance.py")
assert runner.is_file()
source = runner.read_text(encoding="utf-8")
assert "JQ" in source and "--select" in source and "--json" in source
=== END AC conf-002-scoped-run ===

## User Acceptance

- None.

## Guardrails

- Scoped verification must execute selected cases and must never use enumeration, dry-run, or unscoped execution as its product verdict.
