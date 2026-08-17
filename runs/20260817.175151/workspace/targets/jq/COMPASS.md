# COMPASS: jq

## Compass

Build a standalone interpreter for the jq language as described in `sources/jq-manual.txt`. The
product is an executable file named `jq` at the application root. It reads JSON from standard
input, evaluates a jq filter as an ordered generator, and writes each value the filter produces to
standard output as one compact JSON value per line.

Correctness is measured by the upstream jq conformance corpus `sources/jq.test`, taken verbatim
from jq 1.8.2, minus the cases named in `sources/exclusions.txt`. The goal is every case passing,
none failed and none errored.

## Constraints

- Implement in Python using only the standard library.
- Provide an executable named `jq` at the application root, invoked as `./jq -c '<program>'`.
- `-c` is the only option exercised. No other command-line option is required.
- Run without network access, package installation, or external runtime dependencies.
- Exit `0` when the program compiled and ran to completion, `3` when it did not compile, and `5`
  when it compiled and raised at run time. The harness grades on this distinction.
- Diagnostics go to standard error and are never compared.

## Guardrails

- Do not shell out to a system `jq` executable.
- Do not use a third-party jq implementation or binding.
- Do not modify, rewrite, trim, regenerate, or substitute any file under `sources/`. Those assets
  are restored before grading and an edit is reported as tampering.
- Preserve generator ordering, multiplicity, backtracking, and partial-output runtime behavior.
- Keep compile failures distinct from runtime failures using exit codes 3 and 5.

## Verification Protocol

This section is normative. It governs which story may invoke the supplied harness, and how.

### Invoking the harness

`sources/run_conformance.py` **requires** the environment variable `JQ`, the command that runs the
candidate implementation. Without it the harness exits `2` on its own usage code, which is a
harness fault and never a verdict about the interpreter. Every invocation, in every acceptance
criterion and every developer command, supplies it:

```bash
JQ="$PWD/jq" python3 sources/run_conformance.py            # whole corpus, the scored run
JQ="$PWD/jq" python3 sources/run_conformance.py --list     # print case names, run nothing
JQ="$PWD/jq" python3 sources/run_conformance.py --select 'reduce'   # one construct, development only
```

An acceptance criterion written in Python supplies it by **extending** the inherited environment,
never by replacing it:

```python
env={**os.environ, "JQ": str(build_dir / "jq")}
```

`env={"JQ": ...}` alone leaves the child with no `PATH`, so nothing it invokes resolves and the
criterion is false at every level of implementation quality.

`sources/full_test.sh` sets `JQ` itself for the runner it wraps and therefore takes no environment
from its caller.

The harness reserves exit `2` for its own faults — a missing corpus, an unset `JQ`, a stale
exclusion list. Exit `2` never means the interpreter is wrong.

The summary line is:

```
jq conformance: NNN passed, N failed, N errored, N skipped (corpus jq.test @ jq-1.8.2)
```

### The terminal story

The **terminal story** is the last story in the build order: the one on which every other story is
a transitive dependency, and after which no further story runs. It is a verification story. Its
job is not to add capability but to prove that the capability every preceding story delivered is
present, together, at the end of the build.

The terminal story of this project runs `sh sources/full_test.sh`, asserts `returncode == 0`,
prints the captured stdout and stderr so a failure is diagnosable from the evidence alone, and
carries the Sea Trial. It is the only story permitted to run the whole corpus.

A story is not terminal because its name contains "verify", because it is a test harness, or
because it stages the test assets. Staging the corpus is foundational work that happens early;
running the corpus is terminal work that happens last. Do not place a whole-corpus gate on a
story that cannot yet run it — it fails vacuously and teaches nothing.

### Scope of every other story

Every non-terminal story is gated on its own declared behavior only, through `--select` against
the constructs that story implements, and the criterion asserts the selected slice passes. A
non-terminal story never invokes `sources/full_test.sh` and never runs the corpus unfiltered: a
partial interpreter fails most of an authoritative corpus by construction, and its unimplemented
cases exhaust the harness's per-case timeout rather than returning, so the unscoped run costs the
most exactly where it teaches the least.

Regression across stories is not the responsibility of any story's criteria. Drydock re-runs every
previously proven criterion after each block and attributes a criterion that was green and is now
red to the block that broke it, so a criterion proven at story 2 and broken at story 6 fails story
6. Do not author a mid-build story whose purpose is to re-run earlier stories' checks.

### The staging story

The story that stages the conformance assets is gated on the assets being present, complete, and
runnable — not on a bare file-existence assertion, and not on the corpus running. Its criterion
invokes the harness in list mode:

```bash
JQ="$PWD/jq" python3 sources/run_conformance.py --list
```

and asserts the harness exits `0` and reports the expected number of cases. List mode enumerates
the corpus without executing a single case, so it proves the corpus parses, the exclusion list
applies, and the harness runs — while requiring nothing of the interpreter. This is the one
permitted non-terminal use of `run_conformance.py`, and it still supplies `JQ`.

## The corpus

`sources/jq.test` documents its own format in its header. Cases are separated by blank lines;
blank lines and `#` lines are ignored. A case is a program line, an input line, and then the
expected output values, one per line. A case preceded by `%%FAIL` is a program that must be
rejected at compile time; the following lines are upstream jq's diagnostic, which the harness
records but never compares. Reproducing jq's exact error text is reverse-engineering a C
implementation rather than conforming to a specification, so a `%%FAIL` case passes on exit `3`
alone.

Values are compared structurally, not textually. `1` and `1.0` are the same jq value, and so are
two objects whose keys print in a different order. Output formatting is therefore not under test,
but the number and order of values is.

`sources/exclusions.txt` names the corpus cases this kit cannot run, with the reason. They are the
module-loader cases, whose `import` and `include` resolve against a search path of fixture files a
flat source import cannot carry. They are reported as `skipped` and are not part of the score.

The module *grammar* cases are not excluded and must pass. `module (.+1); 0`, `module []; 0`,
`include "a" (.+1); 0`, `include "a" []; 0`, `include "\ "; 0`, `include "\(a)"; 0`, and `%::wat`
are all `%%FAIL` cases: the front end parses the module syntax far enough to reject them, without
ever touching the filesystem.

<!-- drydock:build-write-guardrail:start -->
## Build Write Guardrail

- Authorized build directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/build/jq`
- Authorized Target directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq`
- Build agents have permission to create, modify, and remove files required by the active build block inside these authorized directories.
- No path outside these authorized directories may be modified.
- Protected Drydock artifacts:
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq/blueprint/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq/MANIFEST.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq/COMPASS.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq/QuarterDeck/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260817.175151/workspace/targets/jq/evidence/`
<!-- drydock:build-write-guardrail:end -->
