# jq

A standalone Python jq-language interpreter that reads JSON streams, evaluates jq filters, and emits compact JSON results.

## Intent

Run jq programs with:

```bash
./jq -c '<program>'
```

The program reads JSON values from standard input and writes each generated result as one compact JSON value per line.

Exit statuses are:

- `0` when compilation and evaluation complete successfully
- `3` when the jq program fails to compile
- `5` when evaluation raises a runtime error

The implementation uses only the Python standard library. Run the supplied conformance verification with:

```bash
sh sources/full_test.sh
```

## Programmatic Acceptance

=== AC readme-content ===
Intent: The README documents the executable invocation, stream behavior, exit statuses, and scoring command.

from pathlib import Path

text = Path("README.md").read_text(encoding="utf-8")
required = [
    "./jq -c",
    "standard input",
    "compact JSON",
    "Exit statuses",
    "sources/full_test.sh",
]
for phrase in required:
    assert phrase in text
=== END AC readme-content ===

## User Acceptance

- None.

## Guardrails

- Keep documentation concise and aligned with the executable contract.
- Do not claim command-line options beyond the exercised `-c` interface.
