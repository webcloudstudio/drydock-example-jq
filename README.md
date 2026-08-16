# Drydock UAT Kit: jq

A **kit** is one known project that Drydock rebuilds unattended, end to end, against a real model:
`init` → `import` → `analyze` → `plan` → `build`, then scored and sealed into a self-verifying
proof kit. This kit directory is self-contained and self-runnable; nothing outside it is needed to
reproduce a run.

## What this kit builds

An interpreter for the **jq** language, in Python, from the jq 1.8.2 manual. Correctness is
decided by upstream's own conformance corpus, `tests/jq.test`, taken byte-for-byte from the jq
repository at tag `jq-1.8.2`.

## Why this target

The other kits grade a parser against a suite that arrives pre-carved. `toml-test` scopes by
feature directory; CommonMark's `spec.txt` is flat but shallow. jq is neither. Its 550 cases sit
in one file with no partition worth using — measured, two comment banners own 52% of them — and
its difficulty is concentrated in a single place rather than spread across features:

**Almost every jq filter is a generator.** It takes one input and yields a stream, and downstream
filters run once per upstream value. `reduce`, `foreach`, `limit`, `label`/`break`, path
expressions, and the `?//` destructuring alternative are all defined in terms of backtracking
through that stream. An implementation that treats a filter as a function returning one value
passes the early cases and then stops improving.

That is the property under test. There is no suite partition to hide behind and no way to reach a
high score by breadth, so a story that is too large has to be split rather than retried. The
score is fractional, so the failure shows up as a number instead of a judgement call.

## Prerequisites

None beyond Python 3. Unlike the Toml kit there is no toolchain to install, no harness to build,
and no network access at any point after the kit is fetched.

## Running

```bash
drydock uat jq                   # this kit
drydock uat                      # every kit under uat/
drydock uat --report jq          # rebuild proof kits from completed runs
```

| Flag | Effect |
|---|---|
| `--uat-root <path>` | Directory holding the kits (default `<workspace>/uat`) |
| `--max-build-passes <n>` | Repair passes allowed per build before the kit fails |
| `--llm-provider`, `--model`, `--effort` | Provider and model selection for the whole run |

A run is long and consumes subscription quota.

## Scoring

`sources/full_test.sh` is the sole acceptance verdict, declared as this kit's governed full gate
in `uat.json`. It checks that an executable `./jq` exists, then runs the corpus:

```bash
JQ=/path/to/jq python3 sources/run_conformance.py            # the scored run
JQ=/path/to/jq python3 sources/run_conformance.py -v         # list passing cases too
JQ=/path/to/jq python3 sources/run_conformance.py --json     # machine-readable
python3 sources/run_conformance.py --list                    # print cases, run nothing
```

The runner is external to the implementation on purpose. Upstream jq grades itself through its own
`--run-tests` flag, and a self-graded suite proves nothing here, so `run_conformance.py`
re-implements the corpus protocol and drives the candidate as a subprocess, one process per case.

There are no stage gates. The corpus is not decomposed, and inventing a decomposition would remove
the property this kit exists to measure.

### Calibration

The runner is calibrated against real jq before any model runs:

| Candidate | Result |
|---|---|
| jq 1.8.2 (the pinned version) | 537 passed, 0 failed, 0 errored, 13 skipped — exit 0 |
| jq 1.6 (older, for a gradient) | 397 passed, 136 failed, 4 errored — exit 1 |

Reproduce the first row with the official static release binary:

```bash
curl -sL https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-linux-amd64 -o /tmp/jq182
chmod +x /tmp/jq182
JQ=/tmp/jq182 python3 sources/run_conformance.py
```

A full run takes about one second. Anything other than `0 failed, 0 errored` on jq 1.8.2 is a
defect in the runner, never in jq.

### Declared exclusions

The corpus is never edited. Where a case cannot run under this harness it is named in
`sources/exclusions.txt` with its reason, reported as `skipped`, and left out of the score. Only
the module-loader cases are excluded: they resolve `import` and `include` against a search path of
fixture files spread over nested directories, and Drydock imports a kit's sources flattened by
basename. An exclusion that matches no case is a hard error, so the list cannot go stale silently.

The module *grammar* cases stay in the scored set — they are parse errors a correct front end
rejects without touching the filesystem.

## Layout

```text
uat/jq/
  README.md              this file
  PROVENANCE.md          upstream tag and a SHA-256 for every verbatim file
  uat.json               source bundle, test command, and the governed full gate
  inputs/                lifecycle decisions seeded before analysis
    SEA_TRIALS.md
    TECHNOLOGY_STACK.md
  sources/               Blueprint inputs and supplied build assets
    INSTRUCTIONS.md      the build brief; specification prose, not staged
    jq-manual.txt        the jq 1.8.2 manual, rendered from upstream manual.yml
    jq.test              the conformance corpus, verbatim
    exclusions.txt       cases this kit cannot run, with reasons
    parser.y  lexer.l    upstream grammar and lexer, verbatim
    builtin.jq           builtins upstream defines in jq itself, verbatim
    run_conformance.py   the scoring instrument
    full_test.sh         the scoring entry point
  tools/                 kit authoring tools; not declared in uat.json, never imported
    fetch_upstream.sh    re-fetch the pinned upstream files and rewrite PROVENANCE.md
    render_manual.py     manual.yml -> sources/jq-manual.txt
  runs/<run-id>/         one complete unattended run (generated)
```

The manual ships as `.txt` rather than `.md` deliberately. Drydock stages only non-Markdown
imports onto disk in the build directory; an imported `.md` reaches `analyze` and `plan` and then
survives only as whatever those commands rewrote into the Blueprint. The manual is the normative
semantics of every builtin, and a build story that cannot re-read it is working from a paraphrase.

## Reading a run

```text
runs/<run-id>/
  README.md             run verdict, elapsed time, token and cost accounting
  index.html            linked proof kit
  result.json           every child command, argv, exit code, elapsed time
  SHA256SUMS            integrity manifest
  inputs/               exact declared lifecycle inputs for this run
  sources/              the exact bundle imported for this run
  workspace/            the isolated Drydock workspace, including targets/jq/
  build/jq/             the delivered application
  evidence/
    commands/           stdout and stderr of every child command
    prompts/            the assembled prompt for every LLM call
    prompt_outputs/     the parsed model output
    provider_raw/       the unmodified provider transcript
    llm.jsonl           one record per call: tokens, elapsed time, execution id
    manifest.json       evidence index
```

When a build fails, the authoritative diagnosis is
`workspace/targets/jq/evidence/<block-id>.md`: the pre-build acceptance observation, the stacked
context, the build-directory changes, and the post-build result for every criterion.

Verify a run with:

```bash
cd runs/<run-id> && sha256sum -c SHA256SUMS
```

## Provenance and licensing

`sources/jq.test`, `sources/parser.y`, `sources/lexer.l`, and `sources/builtin.jq` are
unmodified files from https://github.com/jqlang/jq at tag `jq-1.8.2`, under the MIT licence
reproduced in `LICENSE`. `sources/jq-manual.txt` is a deterministic rendering of the same tag's
manual. `PROVENANCE.md` records a SHA-256 for each; `tools/fetch_upstream.sh --verify` re-checks
them.
