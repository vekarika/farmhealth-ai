# Benchmarking Kit — pick the model with data, not assumptions

The milestone this answers: **can Qwen 0.5B / 1.5B / 3B run within ADTC limits AND answer
agriculture questions well enough?** Run this before authoring more data or fine-tuning.

## Candidate matrix (start here)

| Model | Quant | Why it's in the matrix |
|---|---|---|
| Qwen2.5-0.5B-Instruct | Q4_K_M | speed/efficiency ceiling — the lean bet |
| Qwen2.5-1.5B-Instruct | Q4_K_M | primary candidate — quality/size balance |
| Qwen2.5-3B-Instruct | Q4_K_M | upper bound — must out-accuracy its speed/RAM penalty |
| Qwen3-1.7B (if available) | Q4_K_M | newer architecture at similar size |
| *(optional)* Gemma-2-2B-it, Phi-3.5-mini | Q4_K_M | cross-family sanity checks |

Get GGUFs from the official Qwen GGUF repos on Hugging Face, or `ollama pull qwen2.5:1.5b` etc.

## Workflow

```bash
# 1. Telemetry (TPS + peak RAM) on the 840 G6 — edit model paths in the script first
bash benchmarks/run_benchmark.sh

# 2. Quality proxy: hold out ~28 EN gold examples, serve each model via Ollama, grade
ollama serve &
python benchmarks/quality_eval.py --model qwen2.5:1.5b --eval-file training/data/gold_eval_holdout.jsonl
#   → paste the mean quality into the 'quality' column of results.csv for that model

# 3. Composite: convert numbers into an estimated ADTC score and rank
python benchmarks/compute_composite.py benchmarks/results.csv
```

## Decision rule

1. **Drop anything over 7 GB peak RAM** — automatic disqualification, no exceptions.
2. Rank survivors by `Stot(rel)` (speed scored relative to the fastest candidate).
3. **If the base model's quality proxy is already ~75+**, fine-tuning may only need to be light —
   shift effort to RAG + localization. **If it's mediocre (~50–65)**, fine-tuning is the main lever
   and the dataset is where the score is won.
4. Re-run after fine-tuning to confirm the gain justified the effort.

## Honest caveats

- `quality` here is a **dev-time LLM-judge proxy**, not the official S_acc. Replace it with real
  **validation-set** accuracy the moment you obtain the agriculture validation set.
- `Sperf(ref)` uses the provisional `TPS_max = 15`; the real denominator is the fastest team's
  TPS, unknown until submissions land. Treat ~15 t/s as "good," not "guaranteed full marks."
- Bonuses (budget +10%, African-language +15%) are not applied here — form still unconfirmed.
- Run telemetry on target-class hardware (840 G6), or the numbers won't mean anything.
