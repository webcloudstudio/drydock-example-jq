# FEATURE: Scoped Conformance Verification

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide construct-scoped execution of the supplied jq conformance harness. |
| Depends On  | FEATURE-Executable-Entry-Point.md, FEATURE-Process-Contract.md, FEATURE-Conformance-Asset-Staging.md |
| Provides    | scoped conformance execution contract |
| Consumes    | executable jq, staged conformance assets |

## Purpose

Ensure implementation stories can execute only the corpus slice corresponding to the capability under construction, using the supplied runner and its machine-readable report.

## Behavior

- Each scoped invocation supplies `JQ` while preserving the inherited environment.
- Selectors match actual jq program syntax and execute selected cases.
- Acceptance reads the parsed JSON summary rather than scraping human-readable output.
- A valid scoped run requires a nonzero selected case count, zero failures, zero errors, and exit status zero.
- The unfiltered corpus remains reserved for the terminal verification story.

## Programmatic Acceptance

=== AC scoped-runner-contract ===
Intent: The supplied runner executes a nonempty scoped slice and reports a clean result.
import json
import os
import subprocess
import sys

select = r"reduce"
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
=== END AC scoped-runner-contract ===

=== AC scoped-selector-executes ===
Intent: A syntax selector identifies executable corpus cases rather than merely enumerating them.
import json
import os
import subprocess
import sys

select = r"try |error|\?"
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
=== END AC scoped-selector-executes ===

=== AC scoped-environment-preserved ===
Intent: A scoped invocation supplies JQ without discarding the inherited execution environment.
import json
import os
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", r"^(true|false|null|1)$", "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0
assert summary["error"] == 0
assert result.returncode == 0
=== END AC scoped-environment-preserved ===

## User Acceptance

- None.

## Guardrails

- Never use enumeration or dry-run mode as a behavioral acceptance gate.
- Never invoke the unfiltered corpus from this story.
- Never assert against printed summary text; parse the JSON report.
- Never replace the inherited environment when setting `JQ`.
- Do not modify supplied harness assets.
