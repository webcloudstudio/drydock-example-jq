<!-- Compacted from ARCHITECTURE.md sha256=03fbda0643fbd44af66e0fb45cec64fb2847a84746eee35aa27e1a288c4a0070 on 2026-08-16 by drydock build agent -->

Root executable `jq` delegates to Python standard-library CLI, lexer, parser, values, evaluator, control, paths, and builtins boundaries. Evaluation is generator-based and preserves ordered streams/backtracking. Compile errors exit 3; runtime errors exit 5; prior outputs remain emitted. No third-party dependencies, jq subprocesses, or network access.
