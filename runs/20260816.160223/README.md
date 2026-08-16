# jq: DEGRADED

2 of 6 receipt claims proven. Open `index.html` for the linked proof kit; verify it with `sha256sum -c SHA256SUMS`.

## Receipt

| Claim | Verdict | Recorded outcome | Proof |
|---|---|---|---|
| Lifecycle completed | PASS | 15 lifecycle commands executed; the run ended at 15-score-release. Completed with a named shortfall; see the verdict above. | [result.json](result.json) |
| External conformance suite passed | UNPROVEN | No external test command is defined for this project. | — |
| Target completion check passed | UNPROVEN | No completion check was recorded for this run. | — |
| Acceptance score passed | FAIL | drydock score acceptance exited 1. | [evidence/commands/13-score-acceptance.stdout.log](evidence/commands/13-score-acceptance.stdout.log) |
| Release score passed | FAIL | drydock score release exited 1. | [evidence/commands/15-score-release.stdout.log](evidence/commands/15-score-release.stdout.log) |
| Integrity verification passed | PASS | 433 files digested; verify with sha256sum -c SHA256SUMS. | [SHA256SUMS](SHA256SUMS) |

## Run facts

- Drydock: `0.2.0` (commit `0970c48b2a59ed2c0496b0767b4320d3c27e4254`)
- Provider and model: `codex` / `gpt-5.6-luna`
- Platform: `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.35` on Python `3.12.13`
- Target: `jq`
- Run: `20260816.160223`
- Ran: 2026-08-16 12:02:24 EDT — 2026-08-16 12:55:10 EDT
- Elapsed: 3166.0s
- LLM calls: 31
- Tokens: cached 9,762,304; uncached 1,883,650; output 114,368
- LLM elapsed: 2995.6s
- Build passes: 1; repairs: 6 attempts allowed
- Conformance: no external suite defined
- Verdict: expected PASSED, observed ERROR
- Advisory scores: acceptance=exit 1, build-report=exit 1, release=exit 1

## RUN SUMMARY

- Input specification: [`sources/INSTRUCTIONS.md`](sources/INSTRUCTIONS.md)
- Delivered Code: [`build/jq/`](build/jq)
- Test Results: not recorded for this run.

## RUN NOTES:

- One run is evidence of one run. It is not a benchmark.
- It is not a security certification of the delivered code.

## Shortfall

- Degraded: initial-build-1 exited 1; test not run: the build did not complete

## Commands

| # | Command | Exit | Elapsed | Output |
|---|---|---|---|---|
| 01-init | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock init jq` | 0 | 4.2s | [stdout](evidence/commands/01-init.stdout.log) · [stderr](evidence/commands/01-init.stderr.log) |
| 02-import-sources | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock import jq sources --format markdown` | 0 | 4.7s | [stdout](evidence/commands/02-import-sources.stdout.log) · [stderr](evidence/commands/02-import-sources.stderr.log) |
| 03-analyze | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock analyze jq` | 0 | 88.5s | [stdout](evidence/commands/03-analyze.stdout.log) · [stderr](evidence/commands/03-analyze.stderr.log) · [llm](evidence/llm_logs/20260816.160235.081Z_jq_analyze_codex.llm.log) |
| 04-plan | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock plan jq --override` | 0 | 942.9s | [stdout](evidence/commands/04-plan.stdout.log) · [stderr](evidence/commands/04-plan.stderr.log) · [llm](evidence/llm_logs/20260816.160403.811Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.160557.903Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.160703.095Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.160821.112Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.160929.096Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.161037.528Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.161150.106Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.161257.684Z_jq_plan_codex.llm.log) · [llm](evidence/llm_logs/20260816.161406.852Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161451.043Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161605.366Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161633.665Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161654.330Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161727.322Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161804.158Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161823.415Z_jq_lineage_attribute_codex.llm.log) · [llm](evidence/llm_logs/20260816.161907.635Z_jq_lineage_attribute_codex.llm.log) |
| 05-after-plan-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock build status jq` | 0 | 1.0s | [stdout](evidence/commands/05-after-plan-build-status.stdout.log) · [stderr](evidence/commands/05-after-plan-build-status.stderr.log) |
| 06-after-plan-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status jq` | 0 | 0.9s | [stdout](evidence/commands/06-after-plan-target-status.stdout.log) · [stderr](evidence/commands/06-after-plan-target-status.stderr.log) |
| 07-after-plan-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status` | 0 | 0.5s | [stdout](evidence/commands/07-after-plan-workspace-status.stdout.log) · [stderr](evidence/commands/07-after-plan-workspace-status.stderr.log) |
| 08-initial-ready | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status jq --ready` | 0 | 0.4s | [stdout](evidence/commands/08-initial-ready.stdout.log) · [stderr](evidence/commands/08-initial-ready.stderr.log) |
| 09-initial-build-1 | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock build jq --override --repair-attempts 6` | 1 | 2021.4s | [stdout](evidence/commands/09-initial-build-1.stdout.log) · [stderr](evidence/commands/09-initial-build-1.stderr.log) · [llm](evidence/llm_logs/20260816.161950.832Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.162359.423Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.162753.958Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.163007.330Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.163254.663Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.163408.702Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.163902.220Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.164045.261Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.164423.186Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.164656.502Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.165132.725Z_jq_build_codex.llm.log) · [llm](evidence/llm_logs/20260816.165223.003Z_jq_build_codex.llm.log) |
| 10-after-initial-build-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock build status jq` | 0 | 3.0s | [stdout](evidence/commands/10-after-initial-build-build-status.stdout.log) · [stderr](evidence/commands/10-after-initial-build-build-status.stderr.log) |
| 11-after-initial-build-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status jq` | 0 | 2.2s | [stdout](evidence/commands/11-after-initial-build-target-status.stdout.log) · [stderr](evidence/commands/11-after-initial-build-target-status.stderr.log) |
| 12-after-initial-build-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status` | 0 | 0.3s | [stdout](evidence/commands/12-after-initial-build-workspace-status.stdout.log) · [stderr](evidence/commands/12-after-initial-build-workspace-status.stderr.log) |
| 13-score-acceptance | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock score ac jq` | 1 | 15.9s | [stdout](evidence/commands/13-score-acceptance.stdout.log) · [stderr](evidence/commands/13-score-acceptance.stderr.log) |
| 14-score-build-report | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock score build jq` | 1 | 0.5s | [stdout](evidence/commands/14-score-build-report.stdout.log) · [stderr](evidence/commands/14-score-build-report.stderr.log) |
| 15-score-release | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock score release jq` | 1 | 63.6s | [stdout](evidence/commands/15-score-release.stdout.log) · [stderr](evidence/commands/15-score-release.stderr.log) · [llm](evidence/llm_logs/20260816.165447.363Z_jq_score-release_codex.llm.log) |

## Evidence

- [`evidence/commands/`](evidence/commands) — stdout and stderr of every command
- [`evidence/prompts/`](evidence/prompts) — the assembled prompt for every LLM call
- [`evidence/provider_raw/`](evidence/provider_raw) — unmodified provider transcripts
- [`evidence/llm_logs/`](evidence/llm_logs) — call banners and token accounting
- [`result.json`](result.json) — the machine-readable record of this run
