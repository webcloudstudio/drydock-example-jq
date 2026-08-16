# jq

A self-contained Python interpreter for the jq language and its supplied conformance corpus.

## Intent

`jq` evaluates jq filters against JSON values read from standard input and emits compact JSON results, one value per line.

Run it as:

```sh
./jq -c '<program>'
```

The program reads newline-delimited JSON from stdin. The exercised exit codes are:

- `0`: compilation and evaluation completed.
- `3`: the jq program failed to compile.
- `5`: evaluation raised a runtime error.

Diagnostics are written to stderr. Values emitted before a runtime error remain on stdout.

The complete verification command is:

```sh
sh sources/full_test.sh
```

The implementation uses only Python's standard library and does not invoke a system jq executable or require package installation or network access.

## Programmatic Acceptance

=== AC readme-interface ===
Intent: The documented executable invocation is runnable from the project root.

import json
import subprocess

program = "."
input_value = {"ok": True}
result = subprocess.run(
    ["./jq", "-c", program],
    input=json.dumps(input_value) + "\n",
    capture_output=True,
    text=True,
)
assert result.returncode == 0
actual = [json.loads(line) for line in result.stdout.splitlines()]
assert actual == [input_value]
=== END AC readme-interface ===

=== AC readme-verification ===
Intent: The documented complete verification command is available and has a successful process contract.

from pathlib import Path

verification = Path("sources/full_test.sh")
assert verification.is_file()
assert verification.stat().st_mode & 0o111
=== END AC readme-verification ===

## User Acceptance

- None.

## Guardrails

- README must identify `./jq -c '<program>'`, stdin/stdout behavior, exit codes, and `sh sources/full_test.sh`.
- README must not claim dependencies or command-line options outside the product contract.
