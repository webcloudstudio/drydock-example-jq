<!-- Compacted from run_conformance.py sha256=c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492 on 2026-08-16 by drydock build agent -->

Parses `sources/jq.test`, applies exact exclusions, runs each case via `JQ`, compares structural JSON output and exit codes. Exit 0 means no failures/errors; 1 means candidate failure; 2 means harness fault. Compile errors must exit 3; runtime errors may exit 5.
