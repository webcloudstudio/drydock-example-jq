# jq

A self-contained Python standard-library interpreter for jq filters.

Run the executable from the project root:

```sh
./jq -c '<program>'
```

The filter reads newline-delimited JSON values from standard input and writes each result as
one compact JSON value per line to standard output. Diagnostics are written to standard error.
Values already written remain available if a later input or filter evaluation raises an error.

Exit statuses:

- `0` — the filter compiled and completed successfully.
- `3` — the filter could not compile, including syntax or static errors.
- `5` — the filter compiled but raised a runtime error.

The complete verification command is:

```sh
sh sources/full_test.sh
```

The implementation uses only Python's standard library; it does not require package
installation, network access, or a system `jq` executable.
