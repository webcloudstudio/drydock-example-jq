# drydock jq Uat Kit

Flagship drydock UAT kit. ~620 conformance test conditions from the upstream jq test suite (46 excluded, reasons in exclusions.txt). Provenance: byte-for-byte upstream files from github.com/jqlang/jq at tag jq-1.8.2, SHA-256 verified in PROVENANCE.md.

## Intent

Build a standalone interpreter for the jq language as described in `sources/jq-manual.txt`. The
product is an executable file named `jq` at the application root. It reads JSON from standard
input, evaluates a jq filter as an ordered generator, and writes each value the filter produces to
standard output as one compact JSON value per line.

Correctness is measured by the upstream jq conformance corpus `sources/jq.test`, taken verbatim
from jq 1.8.2, minus the cases named in `sources/exclusions.txt`. The goal is every case passing,
none failed and none errored.

## What It Does

Support array and object destructuring in `as` bindings, bind absent members as `null`, and backtrack through `?//` alternatives when a pattern or subsequent expression fails.

Implement filters that discover paths through JSON values and construct projections from selected paths.

Implement immutable access and mutation of nested arrays and objects through explicit path arrays.

Implement jq's immutable deletion, plain assignment, update assignment, and arithmetic assignment semantics.

Handle complex assignment cases involving iterated paths, empty updates, array expansion, invalid indices, NaN indices, string slices, and depth limits.

## Next Steps

- Complete the first-run checks above.
