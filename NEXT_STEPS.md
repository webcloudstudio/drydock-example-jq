# jq Kit — Authoring Notes

What this file is: the author's record of why this kit is shaped the way it is, and what is
still open. It is not a governed input — `uat.json` does not declare it, and no Drydock
command reads it. The rules it refers to (`R1`–`R9`, §-numbers) live in the Drydock
repository at `docs/UAT.md`; they are stated there once and are not repeated here.

Last reviewed: 2026-08-16.

## Status

The kit is authored and calibrated. One unattended run has been recorded.

| Run | Verdict | Where it stopped |
|---|---|---|
| `runs/20260816.134843` | ERROR (expected PASSED) | `plan` exited 1 — a malformed acceptance block in the model's plan output, not a kit fault |

That failure is a Drydock plan-validation failure, not a defect in this kit: no build ran,
so the scoring instrument was never exercised. The kit needs no change on account of it.
Re-run when the plan stage is known good.

## Calibration

| Candidate | Result |
|---|---|
| jq 1.8.2 (the pinned version) | 537 passed, 0 failed, 0 errored, 13 skipped — exit 0, ~1.1 s |
| jq 1.6 (older, negative control) | 397 passed, 136 failed, 4 errored — exit 1 |
| bogus exclusion line, or unset `JQ` | exit 2 — kit fault, never charged to the build |

Reproduce the first row. `curl` is required for the download step and is not otherwise used
by this kit; any HTTP client will do, and the run itself needs no network.

```bash
curl -sL https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-linux-amd64 -o /tmp/jq182
chmod +x /tmp/jq182
cd uat/jq && JQ=/tmp/jq182 python3 sources/run_conformance.py
```

Anything other than `0 failed, 0 errored` on jq 1.8.2 is a defect in `run_conformance.py`,
never in jq.

## Decisions specific to this kit

### The manual ships as `sources/jq-manual.txt`, not as Markdown

Required by R2: a `.md` source reaches `analyze` and `plan` and stops, so a Markdown manual
would survive into the build only as whatever `analyze` paraphrased. `tools/render_manual.py`
renders upstream `tools/manual.yml` to `sources/jq-manual.txt`, which is both injected as
prose at analysis time and staged onto disk for a build story to open. The same applies to
`sources/jq.test`, `sources/parser.y`, `sources/lexer.l`, and `sources/builtin.jq`: none is
Markdown, so all five are staged. `sources/INSTRUCTIONS.md` is the one deliberate `.md` —
author intent, read at analysis, never re-read during the build.

### The Source Roles table in `sources/INSTRUCTIONS.md` is load-bearing

Staging is opt-in and the table is authored by the model during `analyze` (R3). Without the
table in the brief, `analyze` stages nothing and the builder has a manual it cannot open. Do
not delete the table while editing that file down.

### Exit codes are the grading contract

The kit adopts jq's own: `0` ran, `3` did not compile, `5` compiled then raised.

- A `%%FAIL` case passes on exit `3` **specifically**, not on any nonzero exit. All 19
  `%%FAIL` cases were verified to exit 3 under real jq.
- An ordinary case *tolerates* exit `5`. Five cases — the `?//` destructuring alternatives
  and one `try`/`error` case — emit their values and then raise; upstream judges them on the
  values produced. Treating exit 5 as failure was the first calibration defect found.
- The harness reserves exit `2` for its own faults (R4).

### `run_conformance.py` splits lines on `\n` only

Python's `str.splitlines()` is Unicode-aware and breaks on U+000B, U+000C, U+0085, U+2028,
and U+2029. The `trim, ltrim, rtrim` case embeds exactly those inside JSON string literals,
so one expected value was being shredded into five and a correct implementation failed. The
runner uses a newline-only `split_lines()` for corpus parsing, exclusions parsing, and
stdout splitting. Do not "simplify" it back.

### 13 exclusions, all module-loader cases

The excluded cases resolve `import`/`include` against a search path of fixture files across
nested directories, which a flattened source bundle cannot carry (R1). The module *grammar*
cases stay in the scored set — `module (.+1); 0`, `module []; 0`, `include "a" (.+1); 0`,
`include "a" []; 0`, `include "\ "; 0`, `include "\(a)"; 0`, `%::wat` — because they are
`%%FAIL` parse errors a correct front end rejects without touching the filesystem. A stale
exclusion is exit 2, so the list cannot rot silently against the pin.

### No stage gates

Measured, `jq.test`'s comment banners are not a usable partition: `Conditionals` owns 194
cases and `toliteral` 91, so two banners are 52% of 550. There is no decomposition to hide
behind, which is the point — the build loop has to face "this story is too large, split it"
for real. Hence `acceptance.full` alone, per §16.

## Open items

1. **`sources/builtin.jq` is a judgement call.** It is jq's own jq-language implementation of
   roughly 100 builtins — a materially larger giveaway than the CommonMark kit's `cmark.py`,
   which is only a ctypes wrapper. Keeping it makes the builtin layer transcription rather
   than derivation. To drop it: delete the file and its one entry in `uat.json`, and remove
   its row from the Source Roles table and its bullet in `sources/INSTRUCTIONS.md`.
2. **Bundle cost.** The declared sources are roughly 230 KB, about 55k tokens, re-injected at
   `analyze` and at each `plan` batch; `sources/jq-manual.txt` is 131 KB of that. The
   `Invoking jq` and `Colors` sections are already dropped by `tools/render_manual.py`. There
   is no per-story source selection (R6), so the manual ships whole or not at all.
3. **Repository.** `uat/` is gitignored in the Drydock repository; this kit is its own git
   repository, and its `runs/` are committed here as the published proof. Whether it is
   pushed anywhere is the author's call.
