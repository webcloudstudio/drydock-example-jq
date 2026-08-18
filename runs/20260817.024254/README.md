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
| Integrity verification passed | PASS | 297 files digested; verify with sha256sum -c SHA256SUMS. | [SHA256SUMS](SHA256SUMS) |

## Run facts

- Drydock: `0.2.0` (commit `22a9ef86e3a9a69f136bca8d60294591b2485b62`)
- Provider and model: `codex` / `gpt-5.6-luna`
- Platform: `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.35` on Python `3.12.13`
- Target: `jq`
- Run: `20260817.024254`
- Ran: 2026-08-16 22:42:54 EDT — 2026-08-17 00:33:32 EDT
- Elapsed: 6637.0s
- LLM calls: 32
- Tokens: cached 36,693,248; uncached 2,174,063; output 185,377
- LLM elapsed: 5851.2s
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
| 01-init | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock init jq` | 0 | 2.5s | [stdout](evidence/commands/01-init.stdout.log) · [stderr](evidence/commands/01-init.stderr.log) |
| 02-import-sources | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock import jq sources --format markdown` | 0 | 2.8s | [stdout](evidence/commands/02-import-sources.stdout.log) · [stderr](evidence/commands/02-import-sources.stderr.log) |
| 03-analyze | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock analyze jq` | 0 | 81.0s | [stdout](evidence/commands/03-analyze.stdout.log) · [stderr](evidence/commands/03-analyze.stderr.log) · [llm](evidence/commands/03-analyze.llm.log) |
| 04-plan | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock plan jq --override` | 0 | 719.0s | [stdout](evidence/commands/04-plan.stdout.log) · [stderr](evidence/commands/04-plan.stderr.log) · [llm](evidence/commands/04-plan.llm.log) |
| 05-after-plan-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock build status jq` | 0 | 1.6s | [stdout](evidence/commands/05-after-plan-build-status.stdout.log) · [stderr](evidence/commands/05-after-plan-build-status.stderr.log) |
| 06-after-plan-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status jq` | 0 | 1.7s | [stdout](evidence/commands/06-after-plan-target-status.stdout.log) · [stderr](evidence/commands/06-after-plan-target-status.stderr.log) |
| 07-after-plan-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status` | 0 | 0.5s | [stdout](evidence/commands/07-after-plan-workspace-status.stdout.log) · [stderr](evidence/commands/07-after-plan-workspace-status.stderr.log) |
| 08-initial-ready | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status jq --ready` | 0 | 0.5s | [stdout](evidence/commands/08-initial-ready.stdout.log) · [stderr](evidence/commands/08-initial-ready.stderr.log) |
| 09-initial-build-1 | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock build jq --override --repair-attempts 6` | 1 | 5539.9s | [stdout](evidence/commands/09-initial-build-1.stdout.log) · [stderr](evidence/commands/09-initial-build-1.stderr.log) · [llm](evidence/commands/09-initial-build-1.llm.log) |
| 10-after-initial-build-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock build status jq` | 0 | 2.7s | [stdout](evidence/commands/10-after-initial-build-build-status.stdout.log) · [stderr](evidence/commands/10-after-initial-build-build-status.stderr.log) |
| 11-after-initial-build-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status jq` | 0 | 1.0s | [stdout](evidence/commands/11-after-initial-build-target-status.stdout.log) · [stderr](evidence/commands/11-after-initial-build-target-status.stderr.log) |
| 12-after-initial-build-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock status` | 0 | 0.4s | [stdout](evidence/commands/12-after-initial-build-workspace-status.stdout.log) · [stderr](evidence/commands/12-after-initial-build-workspace-status.stderr.log) |
| 13-score-acceptance | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock score ac jq` | 1 | 187.5s | [stdout](evidence/commands/13-score-acceptance.stdout.log) · [stderr](evidence/commands/13-score-acceptance.stderr.log) |
| 14-score-build-report | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock score build jq` | 1 | 0.5s | [stdout](evidence/commands/14-score-build-report.stdout.log) · [stderr](evidence/commands/14-score-build-report.stderr.log) |
| 15-score-release | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python3 -m drydock score release jq` | 1 | 83.9s | [stdout](evidence/commands/15-score-release.stdout.log) · [stderr](evidence/commands/15-score-release.stderr.log) · [llm](evidence/commands/15-score-release.llm.log) |

## Evidence

- [`evidence/commands/`](evidence/commands) — stdout and stderr of every command
- [`evidence/prompts/`](evidence/prompts) — the assembled prompt for every LLM call
- [`evidence/provider_raw/`](evidence/provider_raw) — unmodified provider transcripts
- [`evidence/llm_logs/`](evidence/llm_logs) — call banners and token accounting
- [`result.json`](result.json) — the machine-readable record of this run
