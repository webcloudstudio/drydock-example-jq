# jq

This project provides a standalone Python implementation of the jq command-line interface.

Invoke it with a filter program:

```sh
./jq -c '<program>'
```

The executable reads newline-delimited JSON values from standard input and writes each value
produced by the filter as compact JSON on standard output, one value per line.

The exit statuses are:

- `0` — the program compiled and ran to completion.
- `3` — the program could not be compiled.
- `5` — the program compiled but raised during runtime.

Run the supplied verification command with:

```sh
sh sources/full_test.sh
```
