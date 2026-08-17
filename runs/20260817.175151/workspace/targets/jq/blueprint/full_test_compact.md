<!-- Compacted from full_test.sh sha256=4df25cda12c2741ee02cb7e22d5e3b62161bd90fde948c88a675cb2a94e70fc5 on 2026-08-17 by drydock build agent -->

Executable scoring entry point. Requires `./jq` executable, sets `JQ="$PWD/jq"`, then runs `python3 sources/run_conformance.py` unfiltered. Propagates the harness verdict.
