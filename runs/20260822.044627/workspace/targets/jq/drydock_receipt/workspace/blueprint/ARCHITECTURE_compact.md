<!-- Compacted from ARCHITECTURE.md sha256=f0e07d8104b7c23be2772201e83dfaf382f4c295492da7b8ec72b2a914af633b on 2026-08-22 by drydock build agent -->

- Executable: `./jq -c '<program>'`; compact JSON lines on stdout.
- Exit codes: `0` success, `3` compile failure, `5` runtime failure; diagnostics on stderr.
- Standard-library Python only; no external jq, dependencies, networking, or persistence.
- Modules: CLI, lexer, parser/AST, evaluator streams, runtime values, builtins, paths/assignment, diagnostics.
- Preserve generator ordering, multiplicity, backtracking, immutable transformations, and partial output.
