# FEATURE: Executable jq Entry Point

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides the executable jq command and exercised compact-filter interface. |
| Depends On  | ARCHITECTURE.md |
| Provides    | ./jq -c '<program>' |
| Consumes    | executable boundary |

## Intent

Provide an executable named `jq` at the application root. The command accepts the exercised `-c` option and a jq filter program, then evaluates that program against JSON supplied on standard input.

## Interface

```text
./jq -c '<program>'
stdin: JSON value(s)
stdout: one compact JSON value per generated output line
```

The executable must be runnable directly and must not require package installation or external runtime dependencies.

## Programmatic Acceptance

=== AC exec-entry-conformance ===
Intent: The executable entry point passes the corpus slice containing the primitive interface programs.

import json
import os
import subprocess
import sys

select = r"^(true|false|null|1)$"
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
=== END AC exec-entry-conformance ===

=== AC exec-is-runnable ===
Intent: The deliverable is directly executable at the application root.

import os
import stat

mode = os.stat("jq").st_mode
assert stat.S_ISREG(mode)
assert mode & stat.S_IXUSR
=== END AC exec-is-runnable ===

## User Acceptance

- None.

## Guardrails

- The executable is named exactly `jq`.
- `-c` is the only required command-line option.
- Do not add a wrapper around another jq executable.
