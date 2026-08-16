<!-- Compacted from ARCHITECTURE.md sha256=63147cdb463cbfc1d03a584c4c0dcb7119daf45ece3136570ec4f327657ab631 on 2026-08-16 by drydock build agent -->

- Python standard-library jq architecture with boundaries: `jq_lexer.tokenize`, `jq_parser.parse`, generator-based `jq_runtime.evaluate`, builtin registry, CLI, and executable `jq`.
- `./jq -c '<program>'` reads newline-delimited JSON and emits compact result streams.
- Exit codes: 0 success, 3 compile failure, 5 runtime failure; diagnostics stderr only.
- Preserve ordered generator semantics and partial output; prohibit third-party dependencies, network, subprocesses, and system jq.
