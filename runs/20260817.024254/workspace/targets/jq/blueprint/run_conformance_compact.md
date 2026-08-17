<!-- Compacted from run_conformance.py sha256=c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492 on 2026-08-16 by drydock build agent -->

Conformance runner for `sources/jq.test`; invokes `$JQ -c <program>` per case, compares JSON outputs structurally, requires compile errors as exit 3 and runtime errors as exit 5, skips declared exclusions, and returns 0 only when no cases fail or error.
