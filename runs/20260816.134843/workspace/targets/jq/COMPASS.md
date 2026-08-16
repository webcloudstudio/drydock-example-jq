# COMPASS: jq

## Compass

Build a standalone jq-language interpreter for developers and automation that reads JSON from stdin, evaluates jq filters, and emits compact JSON values. The supplied jq 1.8.2 corpus and runner define correctness; the implementation must be usable through the fixed executable contract and complete the language semantics needed by the corpus.

## Constraints

- Implement in Python using only the standard library.
- Provide an executable named `jq` at the application root.
- Support the exercised `-c '<program>'` interface.
- Preserve the supplied source assets and run without installation or network access.
- Respect jq exit codes: 0 for success, 3 for compile failure, and 5 for runtime failure.
- Keep module-loader exclusions represented by the supplied exclusions file.

## Guardrails

- Never shell out to a system jq executable.
- Never use a third-party jq implementation or binding.
- Never modify the supplied corpus, harness, exclusions, or scoring script.
- Preserve generator ordering, multiplicity, and backtracking semantics.
- Write diagnostics to stderr and produced JSON values to stdout.

<!-- drydock:build-write-guardrail:start -->
## Build Write Guardrail

- Authorized build directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/build/jq`
- Authorized Target directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/workspace/targets/jq`
- Build agents have permission to create, modify, and remove files required by the active build block inside these authorized directories.
- No path outside these authorized directories may be modified.
- Protected Drydock artifacts:
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/workspace/targets/jq/blueprint/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/workspace/targets/jq/MANIFEST.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/workspace/targets/jq/COMPASS.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/workspace/targets/jq/QuarterDeck/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.134843/workspace/targets/jq/evidence/`
<!-- drydock:build-write-guardrail:end -->
