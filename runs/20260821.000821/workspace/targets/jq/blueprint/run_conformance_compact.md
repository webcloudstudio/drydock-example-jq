<!-- Compacted from run_conformance.py sha256=c1b5be717d542f2d2dc4f4a694dd02ae8c8f84b25f15c6224fbb6a784abe7492 on 2026-08-20 by drydock build agent -->

Requires `JQ` candidate command. Parses 550 corpus cases and 13 exclusions, runs each with `-c`, accepts compile exit `3` and runtime exit `5`, compares JSON structurally, and returns `0` only with zero failures/errors.
