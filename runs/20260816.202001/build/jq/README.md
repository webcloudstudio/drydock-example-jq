# jq Interpreter

This project provides a standalone Python implementation boundary for jq. The executable
`./jq -c '<program>'` reads one JSON value per line from standard input and emits each
result as compact JSON on its own output line.

Compile errors exit with status `3`; runtime errors exit with status `5`; successful
evaluation exits with status `0`. The supplied conformance command is:

```sh
sh sources/full_test.sh
```

The implementation uses only Python's standard library and does not invoke another jq.
