# Upstream reference notes (from ADTC official repos)

Key facts extracted from the official profiler + template. The full GPL-3.0 source lives in
the official repos (github.com/Africa-Deep-Tech-Foundation/adtc-profiler); these are the
decision-relevant takeaways, not a copy of their code.

## Accuracy (accuracy.py)
- Runs `lm-eval --model gguf --model_args base_url=local,pretrained=<model_path>` → **bare GGUF, no RAG**.
- Metric: **acc_norm** (length-normalized multiple-choice accuracy), fallback acc.
  → MCQ scored by option *likelihood*, not generation. Keep distractors similar length.
- Default smoke test: `arc_easy`, 50 questions. **Real audit: full hidden 30% validation subset.**
- Has a `language` param (default "en") → per-language accuracy possible; English is default.
- Fixed `--seed 42`.

## Profiler telemetry + audit variance (profiler README)
- S_perf = min(TPS/15, 1.0)*100  ·  S_eff = max(0,(7-peak_rss_gb)/7)*100  ·  P_thermal = -10.
- Self-check vs audit tolerances: memory ±15%, throughput/latency ±25%
  (flag beyond; **FAIL if >50% off**). → benchmark on near-target hardware (840 G6).
- Audit runs in Docker capped at **--memory=7.5g**. Stay under 7 GB.

## Submission template
- metadata.json must have NO placeholder values; exactly 2 test prompts.
- Public repo, no weights in git, download_model.sh idempotent + credential-free, 100% offline at eval.
