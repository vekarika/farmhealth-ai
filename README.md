# FarmHealth AI — ADTC 2026 Laptop LLM Submission (Agriculture)

**Offline agricultural & livestock-health advisor for farmers and extension officers in
northern Nigeria** (Nasarawa, Kaduna, Adamawa, Kwali) — runs entirely on an 8 GB laptop with
zero connectivity, in **English and Hausa**, through llama.cpp on a quantized GGUF model.

Built to the official ADTC 2026 submission template, and organised around how the challenge
**actually scores** submissions.

---

## How scoring drives the design

The profiler runs the **bare GGUF model** (no app/RAG in the scored loop):

```
S_total = 0.50·S_acc + 0.30·S_perf + 0.20·S_eff − P_thermal   (+ up to 10 African-use-case points)
          (lm-eval MCQ) (llama-bench)  (peak RSS)   (>85°C)
```

- **Accuracy (50%)** = multiple-choice (lm-eval `acc_norm`) on the bare model → won by a
  **fine-tuned small model** + a strong domain dataset. RAG is *not* in this loop.
- **Speed (30%) + Efficiency (20%)** → reward a **small, lean** model (target ≥15 t/s, low RAM, <7 GB hard ceiling).
- **Cross-disciplinary integration** = location-aware **offline RAG** (information retrieval) →
  the qualitative score, the demo, and the live defense.
- **African use-case bonus** (≤10 pts) → English-primary model with **Hausa** support + genuine local grounding.

Architecture principle: **the model reasons; retrieval supplies what changes by place and week.**

---

## Repo map

```
.
├── metadata.json            # ADTC submission metadata (schema-valid; fill team_id + github_handle)
├── download_model.sh        # pulls the public GGUF into model/ (edit URL after hosting weights)
├── REPORT.md                # technical writeup (problem, design, constraints, benchmarks)
├── model/                   # GGUF lands here at eval time (gitignored — never commit weights)
│
├── ADTC_MASTER_SPEC.md      # authoritative rules/timeline/scoring (single source of truth)
├── DOMAIN_MAP.md            # knowledge coverage map (stable→fine-tune vs volatile→RAG)
├── DATASET_SPEC.md          # dataset manufacturing blueprint (schema, archetypes, quotas)
│
├── dataset/mcq/             # multiple-choice track (the format accuracy is scored in)
│   ├── MCQ_SCHEMA.md        #   canonical MCQ format + authoring/distractor rules
│   ├── mcq_batch1.jsonl     #   20 review-grade MCQs across 5 categories
│   └── build_mcq_batch1.py
│
├── training/                # free-text gold data + fine-tune + quantize pipeline
│   ├── data/TAXONOMY.md
│   ├── data/gold_batch1.jsonl        # 34 bilingual gold examples
│   ├── data/gold_eval_holdout.jsonl  # reserved eval set (never trained)
│   ├── data/seed_examples_v2.jsonl
│   ├── data/build_gold_batch1.py · build_seed.py · expand_dataset_v2.py
│   ├── finetune_qlora.py    # QLoRA fine-tune (Qwen2.5-1.5B primary)
│   └── to_gguf.sh           # convert + quantize to Q4_K_M
│
├── benchmarks/              # pick the model with data, not assumptions
│   ├── README.md
│   ├── run_benchmark.sh     # TPS + peak RAM per candidate
│   ├── quality_eval.py      # dev-time quality proxy vs the holdout
│   └── compute_composite.py # numbers → estimated ADTC S_total
│
├── profiling/run_profiler.sh   # official ADTC profiler wrapper
└── docs/
    ├── MODEL_COMPARISON.md      # Qwen2.5-1.5B vs 3B vs Tiny Aya Earth (design alternatives)
    └── reference/UPSTREAM_NOTES.md
```

---

## Status

Planning + dataset/format + benchmarking scaffold complete. Next: register (done), fetch the
agriculture validation samples, fine-tune + quantize the candidate models, profile on
target-class hardware, fill real benchmarks into REPORT.md, host the GGUF, submit.

## Data status (honest)

All dataset content is **competition-grade draft**: every quantitative fact carries
`needs_source_check` until verified against the cited source, and every Hausa item carries
`hausa_reviewed: false` until reviewed by a fluent speaker. No drug/agrochemical dosages are
asserted — those are deferred to the product label / vet / extension officer.

## License
Model weights and tools used are cited in REPORT.md with their respective licenses.
