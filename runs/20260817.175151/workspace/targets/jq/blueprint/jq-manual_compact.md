<!-- Compacted from jq-manual.txt sha256=92fc1c179ee6e33d75ffc1f24dd1f0b8ddf5ea666a51224be5088d9431cd8ab3 on 2026-08-17 by drydock build agent -->

jq filters are generator pipelines over JSON values. Lexical requirements include comments, JSON strings and escapes, interpolation via `\(expr)`, identifiers, bindings, operators, literals, and delimiters. Compilation errors use exit 3; runtime errors use exit 5.
