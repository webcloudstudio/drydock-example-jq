# jq Interpreter

This standalone Python implementation reads JSON texts from standard input and evaluates a jq filter supplied with `-c`:

```sh
./jq -c '.' < input.json
```

Each generated value is written as one compact JSON line. Compilation failures exit `3`; runtime failures exit `5`; successful evaluation exits `0`. The supplied verification command is:

```sh
sh sources/full_test.sh
```
