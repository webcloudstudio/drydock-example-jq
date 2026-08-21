# jq

This project provides a standalone jq interpreter implemented with only the Python standard
library. Invoke it from the project root as `./jq -c '<program>'`.

The command reads JSON values from stdin, evaluates the filter for each value, and writes each
result as one compact JSON value per line to stdout. Diagnostics go to stderr. The exit status `0` means
success, `3` means compile failure, and `5` means runtime failure; values emitted before a runtime
failure are retained.

Run the supplied verification with `sh sources/full_test.sh`.
