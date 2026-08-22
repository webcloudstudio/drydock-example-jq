<!-- Compacted from ARCHITECTURE.md sha256=4f66ab67409074d13b7837b0c8eefec7ec2ab64ffdf9e91b66dc67b5df6d4247 on 2026-08-22 by drydock build agent -->

Standalone Python 3.11+ jq interpreter using standard library only. Executable `jq` accepts `-c '<program>'`, reads JSON lines from stdin, evaluates ordered generator streams, and emits compact JSON lines.

Boundaries: lexer/source locations; parser/AST; evaluator/generator control flow; paths/updates; builtins; CLI and exit handling. Preserve ordering, multiplicity, cartesian pipelines, backtracking, and partial output before runtime errors.

Exit codes: 0 success, 3 compile failure, 5 runtime failure. No system jq, third-party runtime, network, or source-asset modifications. Required source assets remain read-only.
