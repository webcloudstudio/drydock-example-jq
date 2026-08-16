# COMPASS: jq

## Compass
Build a standalone jq-language interpreter for developers and automation users. It reads jq filter programs and JSON values from standard input, evaluates generator-valued filters, and emits compact JSON result streams through an executable named `jq`. Correctness is defined by the supplied jq 1.8.2 conformance corpus and scoring harness.

## Constraints
- Implement in Python using only the standard library.
- Provide an executable `./jq` with the exercised `-c '<program>'` interface.
- Read JSON from stdin and emit one compact JSON value per output line.
- Use exit 3 for compile errors and exit 5 for runtime errors.
- Do not require network access, package installation, third-party jq implementations, or a system jq binary.
- Preserve supplied scoring assets and declared module-loader exclusions.

## Guardrails
- Never edit, filter, skip, or reinterpret the supplied scoring harness or corpus.
- Preserve ordered generator semantics, including zero and multiple outputs and partial output before runtime failure.
- Keep diagnostics on stderr and result values on stdout.
- Do not shell out to another jq implementation.

<!-- drydock:build-write-guardrail:start -->
## Build Write Guardrail

- Authorized build directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/build/jq`
- Authorized Target directory: `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq`
- Build agents have permission to create, modify, and remove files required by the active build block inside these authorized directories.
- No path outside these authorized directories may be modified.
- Protected Drydock artifacts:
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq/blueprint/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq/MANIFEST.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq/COMPASS.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq/QuarterDeck/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/jq/runs/20260816.202001/workspace/targets/jq/evidence/`
<!-- drydock:build-write-guardrail:end -->

<!-- Drydock author intent sha256=a2d2f2fb97c42dc444f8c616af6ed4cdc095855838f14d18051e2db386505997 source=INSTRUCTIONS.md -->

# Build Instructions: A jq Interpreter

## Objective

Build an interpreter for the jq language as described in `sources/jq-manual.txt`.
Correctness is measured by the upstream jq conformance corpus, `sources/jq.test`, taken
verbatim from jq 1.8.2. The goal is to pass every case the corpus supplies, with none
failed and none errored. The suite's size is a property of the pinned corpus; never
assert a case count.

The implementation language is Python, fixed by this Target's `TECHNOLOGY_STACK.md` and
governed by `stack/python.md`.

jq is a small language with a large semantic core. Almost every filter is a **generator**:
it takes one input and produces a stream of zero, one, or many outputs, and downstream
filters run once per upstream output. Backtracking through that stream is not an
optimisation, it is the evaluation model, and `reduce`, `foreach`, `limit`, `first`,
`label`/`break`, and the `?//` destructuring alternative are all defined in terms of it. An
implementation that treats a filter as a function returning one value will pass the early
cases and then stall permanently. Decide the evaluation model before writing builtins.

## Run Harness

`sources/full_test.sh` is the single scoring entry point. It is supplied, not authored: it
is staged verbatim into the build directory alongside the other imported assets, and
`drydock uat` runs `sh sources/full_test.sh` from the completed application root and takes
its exit code and output as the score. It reads:

```sh
#!/bin/sh
# full_test.sh — scoring entry point. Do not filter, skip, or reinterpret.
set -eu
if [ ! -x ./jq ]; then
    echo "error: no executable ./jq at the application root." >&2
    echo "The deliverable is an executable named jq that reads JSON on stdin." >&2
    exit 1
fi
JQ="$PWD/jq" exec python3 sources/run_conformance.py
```

Before relying on any path above, run `ls sources/` in the application directory and
correct the paths in the harness against what is actually on disk. Correcting a path is
the only edit permitted to this script. Do not add flags, filters, skips, or a redirection
of the exit code.

The interface check is deliberately separate from the conformance run so that a missing
program and a genuine conformance failure are distinguishable in the evidence. `JQ` is the
harness's only knowledge of the implementation language; the harness itself is
language-neutral.

## Read-only scoring assets

These four files are the exam. They are hash-verified against the import and restored
before grading, so a modification is reported as tampering rather than honoured:

- `sources/full_test.sh` — the scoring entry point
- `sources/run_conformance.py` — the scoring instrument
- `sources/exclusions.txt` — the declared skips
- `sources/jq.test` — the conformance corpus

Do not write to them. Build `./jq` so that the supplied entry point succeeds; changing the
entry point is not a repair, and a repair pass spent editing one of these files is wasted.

## Interface contract

The program is a filter: an executable file named `jq` at the application root, invoked as

```
./jq -c '<program>'
```

with JSON on **stdin**. It writes each value the program produces to **stdout** as one
compact JSON value per line, and exits `0`.

`-c` is the only option exercised. The program need not implement any other jq
command-line option, and the manual's "Invoking jq" section is omitted from
`sources/jq-manual.txt` for that reason.

Exit codes follow jq's own, and the distinction is load-bearing because the harness grades
on it:

| Exit | Meaning |
|---|---|
| `0` | the program compiled and ran to completion |
| `3` | the program did not compile — a syntax or static error |
| `5` | the program compiled but raised at run time |

A case may legitimately emit several values and then raise; the harness compares the values
produced before the raise, so exit `5` is not by itself a failure. Exit `3` on a valid
program is always a failure. Diagnostics go to **stderr** and are never compared.

Any implementation shape that satisfies this contract is acceptable. A
`#!/usr/bin/env python3` script named `jq` that imports the real work from a package
alongside it is the obvious one; `main` should parse arguments and delegate.

## Test / verification process

The imported source files are placed in a `sources/` subdirectory of the application
directory. The only tools required are `python3` and a POSIX `sh`, both already present.
No installation step, no package download, and no network access are required at any
point.

```bash
JQ="$PWD/jq" python3 sources/run_conformance.py                     # the scored run
JQ="$PWD/jq" python3 sources/run_conformance.py -v                  # list passing cases too
JQ="$PWD/jq" python3 sources/run_conformance.py --json              # machine-readable
JQ="$PWD/jq" python3 sources/run_conformance.py --list              # print cases, run nothing
JQ="$PWD/jq" python3 sources/run_conformance.py --select 'reduce'   # one construct at a time
```

During development, `sh sources/full_test.sh` does the interface check and the conformance
run together, and is the same command the score is taken from.

`--select` takes a regular expression matched against the case's program text and exists
for development only. The acceptance gate always runs the whole corpus; there is no scoped
gate and none may be created.

**Exactly one acceptance check runs the suite.** One terminal story — the last one — runs
`sh sources/full_test.sh`, asserts only `result.returncode == 0`, prints the captured
stdout and stderr so a failure can be diagnosed from the evidence, and carries the Sea
Trial. No other acceptance check may invoke `full_test.sh` or `run_conformance.py`, and no
acceptance check may assert that an imported or staged file merely exists — a file-presence
check is not acceptance.

The summary line is:

```
jq conformance: NNN passed, N failed, N errored, N skipped (corpus jq.test @ jq-1.8.2)
```

The harness reserves exit `2` for its own faults — a missing corpus, an unset `JQ`, a
stale exclusion. Exit `2` never means the interpreter is wrong.

## The corpus format

`sources/jq.test` documents its own format in its header. Cases are separated by blank
lines; blank lines and `#` lines are ignored. A case is a program line, an input line, and
then the expected output values, one per line. A case preceded by `%%FAIL` is a program
that must be **rejected at compile time**: the following lines are upstream jq's
diagnostic, which this harness records but never compares. Reproducing jq's exact error
text is reverse-engineering a C implementation, not conforming to a specification, so a
`%%FAIL` case passes on exit `3` alone.

Values are compared structurally, not textually. `1` and `1.0` are the same jq value; so
are two objects whose keys are printed in a different order. Formatting of output is
therefore not under test, but the **number and order** of values is.

## Declared exclusions

`sources/exclusions.txt` names the corpus cases this kit cannot run, with the reason. They
are the module-loader cases: `import` and `include` resolved against a search path of
fixture files that this kit's flat source import cannot carry. They are reported as
`skipped` and are not part of the score.

The module *grammar* cases are **not** excluded and must pass. `module (.+1); 0`,
`module []; 0`, `include "a" (.+1); 0`, `include "a" []; 0`, `include "\ "; 0`,
`include "\(a)"; 0`, and `%::wat` are all `%%FAIL` cases: the front end must parse the
module syntax far enough to reject them, without ever touching the filesystem.

## Source Roles

Record this table in the Analysis so every asset is staged onto disk in the build
directory. `sources/jq-manual.txt`, `sources/jq.test`, `sources/parser.y`, and
`sources/lexer.l` are large and must be readable from disk during implementation rather
than carried in prompt text.

| Source | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `jq-manual.txt` | normative specification | context | stage |
| `jq.test` | conformance test suite | context | stage |
| `parser.y` | normative specification | context | stage |
| `lexer.l` | normative specification | context | stage |
| `builtin.jq` | reference implementation | context | stage |
| `run_conformance.py` | conformance harness | context | stage |
| `full_test.sh` | conformance harness | context | stage |
| `exclusions.txt` | conformance harness | context | stage |
| `INSTRUCTIONS.md` | author intent | context | prompt-only |

What each staged file is for:

- `sources/jq-manual.txt` — the jq language manual at 1.8.2, rendered to plain text. The
  primary specification, and the normative description of every builtin.
- `sources/jq.test` — the conformance corpus. Also the most precise available statement of
  the semantics, especially for generators and backtracking.
- `sources/parser.y` — upstream's yacc grammar. The authority on operator precedence,
  associativity, and the shape of every syntactic form.
- `sources/lexer.l` — upstream's lexer. The authority on tokens, string interpolation, and
  escape handling.
- `sources/builtin.jq` — the subset of jq's builtins that upstream defines in jq itself.
  Read it as a specification of those builtins' semantics.
- `sources/run_conformance.py`, `sources/full_test.sh`, `sources/exclusions.txt` — the
  scoring instruments, read-only as stated above.

## Suggested implementation order

The difficulty is concentrated in one place — the evaluation model — and not spread evenly
across the corpus. Build the core correctly before reaching for coverage.

1. **Lexer and parser.** Follow `sources/lexer.l` and `sources/parser.y` directly. Produce
   an AST. Precedence, `?` suffixes, string interpolation, and the `def` forms are all
   settled there. Reject invalid programs with exit `3`.
2. **The generator core.** Evaluate a filter as something that yields a stream of values:
   `.`, literals, `|`, `,`, field access, iteration, arithmetic, comparison, and
   `empty`. Every later feature is expressed in terms of this. Get `[.[] | f]`,
   cartesian products over multi-output arguments, and short-circuiting right.
3. **Paths and assignment.** `path(f)`, `getpath`, `setpath`, `delpaths`, `del`, and then
   `=`, `|=`, `+=`, and friends. Assignment is defined over path expressions, so this
   cannot precede step 2.
4. **Control flow.** `if`/`then`/`elif`/`else`/`end`, `try`/`catch` and `?`, `//`,
   `reduce`, `foreach`, `label`/`break`, `limit`, `first`, `last`, `until`, `while`,
   `recurse`. This is where backtracking is tested hardest.
5. **Functions, variables, and destructuring.** `def` with arity and closures, `as`
   bindings, object and array patterns, and the `?//` alternative operator.
6. **Builtins.** Work outward from `sources/builtin.jq` and the manual: strings, arrays,
   objects, `sort_by`/`group_by`/`unique_by`, `@base64`/`@uri`/`@csv`/`@tsv`/`@sh`
   formats, the date functions, `tostream`, `input`/`inputs`, `$__loc__`, `debug`.
7. **Numbers and edge cases.** `nan`, `infinite`, integer/float equality, large literals,
   and the `have_decnum` builtin — return `false` from it and the corpus takes its
   non-decNumber branch, which native floats satisfy.

The manual is normative and the corpus is precise. Follow both directly rather than
inferring behaviour from jq's printed output.

## Definition of Done

- `sh sources/full_test.sh` runs cleanly with zero errors and exits zero.
- The program satisfies the `./jq -c` → stdin → one-JSON-value-per-line → exit-code
  contract.
- Every corpus case that runs passes: the failed and errored counts are both zero, and the
  skipped count matches the declared exclusions. The harness exit status is the verdict and
  the whole verdict — assert `returncode == 0` and stop there. Do not assert on the text of
  the summary line at all: the case totals belong to the pinned corpus, and a check that
  reads a runner's printed output is measuring the runner rather than the interpreter.
- Do not create acceptance checks asserting that imported or staged files merely exist.
- The interpreter is written from the specification. **Every third-party jq
  implementation or binding is forbidden** — `jq.py`, `pyjq`, `jqlang`, `gojq`, `jaq`, and
  any other — as is shelling out to a system `jq` binary. A wrapper around real jq scores
  perfectly and makes the exercise meaningless.
- The project declares no third-party runtime dependency. The standard library is
  sufficient: `json`, `decimal`, `math`, `re`, `datetime`, `time`, `base64`, `unicodedata`,
  `itertools`, `functools`, `dataclasses`, `argparse`, `sys`.
- No network access at any point, including at test time. No package is installed, and no
  tool beyond `python3` and POSIX `sh` is invoked.
- Deliver a concise project `README.md` documenting the stdin/stdout interface, the exit
  codes, and the `sh sources/full_test.sh` command.
