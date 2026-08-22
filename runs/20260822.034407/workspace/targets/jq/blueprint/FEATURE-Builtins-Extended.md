# FEATURE: Builtins Extended

| Field       | Value |
|-------------|-------|
| Version     | 20260822 V1 |
| Description | Provides jq serialization, formats, dates, mathematics, SQL-style, environment, and streaming builtins. |
| Depends On  | FEATURE-Builtins-Regex.md, FEATURE-Builtins-Core.md |
| Provides    | JSON conversion, @ formats, dates, math, SQL-style operators, streaming utilities |
| Consumes    | regex builtins, collection builtins, generator evaluator |

## Intent

Implement the remaining standard-library jq builtins required by the manual and corpus: JSON serialization and parsing, format encoders, date and time functions, mathematical functions, SQL-style operators, environment access, debugging-compatible I/O, and stream conversion utilities.

## Programmatic Acceptance

=== AC builtins-extended-serialization-formats ===
Intent: The authoritative corpus slice covering JSON conversion, format encoders, and related serialization behavior passes.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"tojson|fromjson|@text|@json|@html|@uri|@urid|@csv|@tsv|@sh|@base64|@base64d"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0

=== END AC builtins-extended-serialization-formats ===

=== AC builtins-extended-time-math-streaming ===
Intent: The authoritative corpus slice covering dates, mathematics, SQL-style operators, and streaming utilities passes.
Suite: scoped

import json
import os
import subprocess
import sys
from pathlib import Path

assert Path("jq").is_file()

selector = r"fromdate|todate|strptime|strftime|mktime|gmtime|floor|sqrt|atan|cos|sin|pow|log|INDEX|JOIN|IN\(|tostream|fromstream|truncate_stream|env|debug"
result = subprocess.run(
    [sys.executable, "sources/run_conformance.py", "--select", selector, "--json"],
    capture_output=True,
    text=True,
    env={**os.environ, "JQ": f"{os.getcwd()}/jq"},
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
report = json.loads(result.stdout)
summary = report["summary"]
assert sum(summary.values()) > 0
assert summary["fail"] == 0 and summary["error"] == 0
assert result.returncode == 0

=== END AC builtins-extended-time-math-streaming ===

## User Acceptance

- None.

## Guardrails

- Keep runtime dependencies limited to Python's standard library.
- Date behavior is UTC-based where jq specifies UTC; nondeterministic clock output is not used as an acceptance oracle.
- Preserve compact JSON semantics, format escaping, stream ordering, and partial runtime output.
