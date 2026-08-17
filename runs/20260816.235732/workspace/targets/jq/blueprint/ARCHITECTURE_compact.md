<!-- Compacted from ARCHITECTURE.md sha256=a21f86f8f48cdfff12804f01b38bccf42e3925539683235d250e8f998e435bd7 on 2026-08-16 by drydock build agent -->

Standalone Python 3.11+ standard-library jq CLI. Root `./jq` accepts `-c '<program>'`, reads JSON stdin, emits compact JSON lines stdout, diagnostics stderr, and uses exit codes 0 success, 3 compile/static failure, 5 runtime failure. Modules: executable boundary, Lexer, Parser/AST, generator-based Runtime, Values, Paths/assignments, and Builtins. Preserve generator order/multiplicity and never invoke external jq or modify `sources/`.
