# FarmHealth AI — ADTC 2026 Laptop LLM Submission (Agriculture)

Offline agricultural & livestock-health advisor for farmers and extension officers in northern Nigeria (Nasarawa, Kaduna, Adamawa, Kwali) — runs entirely on an 8 GB laptop with zero connectivity, in English and Hausa, through llama.cpp on a quantized GGUF model.

## How scoring drives the design

- Accuracy (50%) = MCQ evaluation on the bare GGUF model
- Speed (30%) + Efficiency (20%) reward small models
- Cross-disciplinary integration = offline location-aware RAG
- African use-case bonus = English + Hausa + local agricultural grounding

## Repository Structure

- metadata.json
- REPORT.md
- ADTC_MASTER_SPEC.md
- DATASET_SPEC.md
- DOMAIN_MAP.md
- dataset/mcq/
- training/
- benchmarks/
- profiling/

## Status

Planning, dataset design, benchmarking scaffold, and initial datasets complete. Next steps: dataset expansion, fine-tuning, quantization, profiling, and submission.

## License

See LICENSE and REPORT.md for model and tooling licenses.
