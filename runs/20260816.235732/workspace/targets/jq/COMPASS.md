# COMPASS: jq

## Compass
Build a standalone jq-language interpreter for developers and automation that need to transform JSON through jq filters. The executable reads JSON from stdin, evaluates filters with jq's generator semantics, and emits compact JSON values to stdout.

## Constraints

- Implement in Python using only the standard library.
- Provide an executable named `jq` at the application root.
- Support the exercised `./jq -c '<program>'` interface.
- Use no network access, package installation, third-party jq implementation, jq binding, or system jq binary.
- Preserve exit code 3 for compile errors and 5 for runtime errors.
- Keep supplied scoring assets unchanged.
- Acceptance runs from the completed application root.

## Guardrails

- Do not shell out to or wrap another jq implementation.
- Do not modify, filter, skip, or reinterpret the supplied conformance corpus or harness.
- Preserve generator backtracking, output order, and multiplicity.
- Emit diagnostics to stderr and JSON results to stdout.
- Run the complete suite only through the terminal acceptance story.

<!-- drydock:build-write-guardrail:start -->
## Build Write Guardrail

- Authorized build directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/build/jq`
- Authorized Target directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/workspace/targets/jq`
- Build agents have permission to create, modify, and remove files required by the active build block inside these authorized directories.
- No path outside these authorized directories may be modified.
- Protected Drydock artifacts:
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/workspace/targets/jq/blueprint/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/workspace/targets/jq/MANIFEST.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/workspace/targets/jq/COMPASS.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/workspace/targets/jq/QuarterDeck/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.235732/workspace/targets/jq/evidence/`
<!-- drydock:build-write-guardrail:end -->
