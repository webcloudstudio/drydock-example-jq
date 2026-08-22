# COMPASS: jq

Build a standalone interpreter for the jq language. The executable reads JSON from
standard input, evaluates a jq filter as an ordered generator, and writes produced
values to standard output.

Compile failures return exit `3`. Runtime failures return exit `5`. Successful
completion returns exit `0`.
