<!-- Compacted from jq-manual.txt sha256=92fc1c179ee6e33d75ffc1f24dd1f0b8ddf5ea666a51224be5088d9431cd8ab3 on 2026-08-16 by drydock build agent -->

jq filters consume one input and produce ordered zero-or-more outputs. Core frontend semantics include identity, fields, indexing, iteration, arrays, objects, pipes, commas, literals, comments, string interpolation, and generator ordering. Strings use JSON-compatible escapes; interpolation is `\(expression)`. Invalid programs compile-fail; runtime errors are separate.
