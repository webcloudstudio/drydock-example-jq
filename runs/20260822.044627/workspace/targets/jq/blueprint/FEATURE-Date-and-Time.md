# FEATURE: Date and Time

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provide jq date parsing, formatting, and time conversion filters. |
| Depends On  | FEATURE-Regular-Expressions.md |
| Provides    | fromdateiso8601, todateiso8601, strptime, strftime, gmtime, localtime, mktime |
| Consumes    | jq string and numeric values |

## Intent

Implement UTC ISO-8601 conversion and the required low-level date and time filters using Python standard-library facilities. Support supplied valid and invalid-input behavior and the fixed interface's deterministic timezone expectations.

## Programmatic Acceptance

=== AC text-004-conformance ===
Intent: Date and time filters perform deterministic UTC conversions.
import json
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", "fromdateiso8601"],
    input='"1970-01-01T00:00:00Z"\n',
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == 0

result = subprocess.run(
    ["./jq", "-c", "todateiso8601"],
    input="0\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == "1970-01-01T00:00:00Z"
=== END AC text-004-conformance ===

=== AC text-004-execution ===
Intent: Low-level date and time filters execute a non-empty deterministic case.
import json
import os
import subprocess

env = {**os.environ, "PATH": os.environ.get("PATH", "")}

result = subprocess.run(
    ["./jq", "-c", "strftime(\"%Y-%m-%d\")"],
    input="0\n",
    capture_output=True,
    text=True,
    env=env,
)
assert result.returncode == 0, result.returncode
assert json.loads(result.stdout) == "1970-01-01"
=== END AC text-004-execution ===

## User Acceptance

- None.

## Guardrails

- Use UTC for ISO date behavior and the supplied fixed interface.
- Use only Python standard-library facilities.
- Do not introduce wall-clock-dependent assertions or runtime dependencies.
