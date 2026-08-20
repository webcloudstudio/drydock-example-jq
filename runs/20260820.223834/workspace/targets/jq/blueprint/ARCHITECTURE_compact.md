<!-- Compacted from ARCHITECTURE.md sha256=7c98155c5d01d5c7a9f433ec157833451b61cf24d3d02aefbf97974b87bfda67 on 2026-08-20 by drydock build agent -->

Defines lexer, parser, evaluator, path/assignment, control/binding, builtin, and executable boundaries. Requires lazy generator streams, immutable values, standard-library-only Python 3.11+, POSIX sh, and exit codes 3/5 for compile/runtime failures.
