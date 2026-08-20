# jq

## Intent

jq is a standalone Python standard-library interpreter for the jq language. It reads JSON values from standard input, evaluates a jq filter, and writes compact JSON results one per line.

Invoke it from the application root:

```bash
./jq -c '<program>'
```

The executable uses these exit statuses:

- `0` when compilation and evaluation complete successfully.
- `3` when the jq program cannot be compiled.
- `5` when evaluation raises a runtime error.

Runtime output produced before an error is preserved. Diagnostics are written to standard error.

The supplied conformance suite can be run with:

```bash
sh sources/full_test.sh
```

The project requires no network access, package installation, or third-party runtime dependency.

## Programmatic Acceptance

- None. This specification documents operation; executable behavior is verified by the delivery and terminal conformance stories.

## User Acceptance

- The documented invocation, input/output behavior, exit statuses, and verification command are clear and accurate.

## Guardrails

- Keep this document concise and consistent with the executable contract.
