<!-- Compacted from jq-manual.txt sha256=92fc1c179ee6e33d75ffc1f24dd1f0b8ddf5ea666a51224be5088d9431cd8ab3 on 2026-08-16 by drydock build agent -->

jq filters are ordered generators. Functions, filter/value arguments, lexical bindings, closures, recursion, destructuring, and `?//` must preserve stream multiplicity, scope, backtracking, and jq truthiness. JSON values are immutable; runtime errors are catchable.
