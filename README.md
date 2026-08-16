# jq

This build provides a self-contained Python standard-library jq interpreter. It
accepts `./jq -c '<program>'`, reads newline-delimited JSON from standard input,
and writes one compact JSON result per line. Exit code `3` denotes compilation
or argument errors; exit code `5` denotes runtime errors after compilation.

Run the supplied conformance harness with:

```sh
sh sources/full_test.sh
```
