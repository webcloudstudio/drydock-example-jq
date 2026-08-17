# jq Interpreter

A standalone Python interpreter for the jq language that reads JSON from stdin and emits filtered JSON values.

## Intent

Run a jq filter in compact-output mode:

```sh
./jq -c '<program>' < input.json
```

The program reads JSON values from standard input and writes each generated result as one compact JSON value per line to standard output. Diagnostics are written to standard error.

Exit codes:

- `0` — compilation and execution completed successfully.
- `3` — the jq program could not be compiled.
- `5` — the compiled program raised a runtime error.

The implementation uses only the Python standard library and does not depend on a system jq executable or third-party package.

Run the supplied verification command from the application root:

```sh
sh sources/full_test.sh
```
