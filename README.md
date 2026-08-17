# jq Interpreter

`./jq -c '<program>'` reads newline-delimited JSON from standard input and emits one compact JSON value per result on each output line.

Exit status `0` indicates success, `3` a compile or static error, and `5` a runtime error. The supplied conformance suite can be run with:

```sh
sh sources/full_test.sh
```
