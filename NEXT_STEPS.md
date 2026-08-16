# jq Kit — State, Design Points, and Open Items

Written 2026-08-14. This file exists so the reasoning behind the kit survives a context clear.
It is authoring notes, not a governed input; `uat.json` does not declare it.

## Status

The kit is complete and calibrated. Nothing is pending before a run.

| Candidate | Result |
|---|---|
| jq 1.8.2 (the pinned version) | 537 passed, 0 failed, 0 errored, 13 skipped — exit 0, ~1.1 s |
| jq 1.6 (older, negative control) | 397 passed, 136 failed, 4 errored — exit 1 |
| bogus exclusion, or unset `JQ` | exit 2 — kit fault, never charged to the build |

Reproduce the first row:

```bash
curl -sL https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-linux-amd64 -o /tmp/jq182
chmod +x /tmp/jq182
cd uat/jq && JQ=/tmp/jq182 python3 sources/run_conformance.py
```

Anything other than `0 failed, 0 errored` on jq 1.8.2 is a defect in `run_conformance.py`.

## Design points

### The manual ships as `.txt`, not `.md`, and that is load-bearing

Build-story prompts receive **no imported source content**. `source_roles.py` skips Markdown when
promoting sources into the Blueprint, and `build.py` gives the builder only the *names* of staged
non-Markdown assets. The full bundle reaches `analyze` and `plan` and stops there.

So an imported `.md` manual would survive into the build only as whatever `analyze` paraphrased
into the Blueprint. As `.txt` it is both injectable as prose at analysis time and staged onto disk
for the builder to open. CommonMark's `spec.txt` works the same way.

### The Source Roles table in INSTRUCTIONS.md is not decoration

Staging is opt-in and the `## Source Roles` table is authored by the LLM during `analyze`. An
unsteered `analyze` stages nothing, and the builder then has a manual it cannot read. The table in
`sources/INSTRUCTIONS.md` exists to force `stage` on all eight non-INSTRUCTIONS sources. Do not
delete it while editing that file down.

### Exit codes are the grading contract

jq's own: `0` ran, `3` did not compile, `5` compiled then raised. The runner adopts them.

- A `%%FAIL` case passes on exit `3` **specifically**, not on any non-zero exit. All 19 `%%FAIL`
  cases were verified to exit 3 under real jq. This is stricter than the original plan.
- An ordinary case *tolerates* exit `5`. Five cases — the `?//` destructuring alternatives and one
  `try`/`error` case — emit their values and then raise; upstream judges them on the values
  produced. Treating exit 5 as failure was the first calibration defect found.
- The harness reserves exit `2` for its own faults, matching `GATE_USAGE_EXIT`.

### `str.splitlines()` cannot be used on this corpus

It is Unicode-aware and breaks on U+000B, U+000C, U+0085, U+2028, and U+2029. The
`trim, ltrim, rtrim` case's expected output embeds exactly those inside JSON strings, so one value
was being shredded into five and a correct implementation failed. `run_conformance.py` uses a
newline-only `split_lines()` throughout — corpus parsing, exclusions parsing, and stdout splitting.
Do not "simplify" it back.

### 13 exclusions — loader cases only

Only the module-*loader* cases are excluded: they resolve `import`/`include` against a search path
of fixture files across nested directories, and Drydock copies a kit's sources **flattened by
basename**, so that tree physically cannot be carried.

The module-*grammar* cases stay in the scored set — `module (.+1); 0`, `module []; 0`,
`include "a" (.+1); 0`, `include "a" []; 0`, `include "\ "; 0`, `include "\(a)"; 0`, `%::wat`.
They are `%%FAIL` parse errors a correct front end rejects without touching the filesystem.

An exclusion matching zero cases is exit 2, so the list cannot rot silently against the pin.

### Why this target at all

`jq.test`'s comment banners are **not** a usable partition — measured, `Conditionals` owns 194
cases and `toliteral` 91, so two banners are 52% of 550. There is no decomposition to hide behind,
which is the whole point: the build loop has to face "this story is too hard, split it" for real.
Hence `acceptance.full` only, with no `stages` block.

## Open items for your hand-edit

1. **`sources/builtin.jq`.** In per `ideas/UAT.md`'s bundle, but it is jq's own jq-language
   implementation of ~100 builtins — a materially larger giveaway than the CommonMark kit shipped
   (`cmark.py` there is a ctypes wrapper, not a reference implementation). To drop it: delete the
   file and its one entry in `uat.json`.
2. **Bundle cost.** ~230 KB ≈ 55k tokens at `analyze` and at each `plan` batch. `jq-manual.txt` is
   131 KB of that. The `Invoking jq` and `Colors` sections are already dropped by
   `tools/render_manual.py`. There is no per-story source selection in Drydock — `build.py`
   resolves a story's `context:` against the Blueprint, never against `sources/` — so slicing the
   manual per story is not available; it ships whole or not at all.
3. **Repository.** `uat/` is gitignored at `.gitignore:46` (commit 9771073, one repo per kit).
   Nothing here is tracked. Whether `uat/jq` becomes its own repository is your call.

## Unrelated red test, not from this kit

`tests/test_gate_policy_replay.py::test_frozen_corpus_matches_the_live_corpus` fails with
`ValueError: unrecognized recorded verdict 'MET'`. `tests/uat_corpus.py:32` maps only
`{PASS, FAIL, INCONCLUSIVE}`, but recent runs under `uat/ReadingList/` and `uat/Toml/` record
`MET`. The grader's verdict vocabulary changed and the replay helper's map did not follow. This
kit has produced no runs. Rest of the suite: 2608 passed.
