<!-- Compacted from run_conformance.py sha256=c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492 on 2026-08-17 by drydock build agent -->

Language-neutral jq corpus runner. Requires `JQ`; supports `--list`, `--select`, `--json`, and verbose mode. List mode parses and enumerates cases without execution. Exit 0 means all run cases pass, 1 means failures/errors, and 2 means harness fault. Candidate compile errors must exit 3; runtime errors must exit 5.
