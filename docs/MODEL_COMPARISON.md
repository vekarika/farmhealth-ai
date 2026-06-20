# Model Comparison — FarmHealth AI (ADTC 2026, Agriculture)

Candidate base models evaluated for an offline, fine-tuned, GGUF/llama.cpp agriculture
advisor on the ADTC Standard Laptop (4 vCPU, 8 GB RAM, integrated graphics, **7 GB peak
ceiling**). Accuracy (50%) is graded as multiple-choice on the **bare model**; speed (30%)
and efficiency (20%) reward small, lean models. English is the primary evaluation language;
Hausa earns the African-use-case bonus (up to 10 points).

> **Status of figures:** Q4_K_M sizes and Hausa coverage are taken from published model cards
> (verified). RAM and TPS are **development estimates** pending measurement with the ADTC
> profiler on the target-class machine (HP EliteBook 840 G6). Final benchmarks replace these.

---

## 1. Qwen2.5-1.5B-Instruct

| Attribute | Value |
|---|---|
| Parameters | 1.5B |
| Est. Q4_K_M size | ~1.0–1.1 GB |
| Est. peak RAM | ~1.3–1.8 GB |
| Est. TPS (i5 CPU) | ~15–25 t/s — clears the TPS_REFERENCE of 15 |
| Hausa support | Weak natively (Hausa not in Qwen2.5's supported set); acquired via fine-tuning |
| Fine-tuning difficulty | **Low** — standard architecture, mature ecosystem (TRL/PEFT/Unsloth/Axolotl), trains fast under QLoRA |
| License | **Apache-2.0** (commercial use permitted) |

**Pros**
- Best speed + efficiency profile of the three → maximises the combined 50% (S_perf + S_eff).
- Apache-2.0 — no commercialization constraint, important for the ADTC scale-up/residency prize.
- Easiest and fastest to fine-tune; quick benchmark/iterate loop on a 10-week timeline.
- Strong reasoning-per-parameter; clears the English MCQ bar well after domain fine-tuning.

**Cons**
- Lowest raw knowledge ceiling of the three; relies on a strong domain dataset for accuracy.
- No meaningful native Hausa — bilingual capability must be built through fine-tuning data.

---

## 2. Qwen2.5-3B-Instruct

| Attribute | Value |
|---|---|
| Parameters | 3B |
| Est. Q4_K_M size | ~1.9 GB |
| Est. peak RAM | ~2.5–3.0 GB |
| Est. TPS (i5 CPU) | ~7–11 t/s — likely below the 15 reference |
| Hausa support | Weak natively; acquired via fine-tuning |
| Fine-tuning difficulty | **Low–moderate** — same ecosystem as 1.5B, more compute per step |
| License | **Qwen Research License** (non-commercial; commercial use needs a separate licence) — verify on the model card |

**Pros**
- Higher base English reasoning/knowledge than the 1.5B → strongest accuracy *ceiling* among the Qwen options.
- Same easy fine-tuning tooling as the 1.5B.
- Still well under the 7 GB memory wall.

**Cons**
- Slower; likely forfeits points on the 30% speed score versus a 1.5B.
- Heavier RAM → lower S_eff than the 1.5B.
- Non-commercial research licence complicates the commercialization/residency prize.
- No native Hausa.

---

## 3. Tiny Aya Earth (3.35B)

| Attribute | Value |
|---|---|
| Parameters | 3.35B (Africa/West-Asia specialised variant of Tiny Aya; `cohere2` architecture) |
| Est. Q4_K_M size | **2.14 GB** (verified, Cohere GGUF model card) |
| Est. peak RAM | ~2.8–3.4 GB (262k-token vocab adds embedding/output overhead) |
| Est. TPS (i5 CPU) | ~6–10 t/s — likely below the 15 reference |
| Hausa support | **Strong natively** — Hausa is an explicitly covered language; Africa-specialised; ~39% African-language reasoning vs ~6% for a same-class Qwen3-4B |
| Fine-tuning difficulty | **Higher** — newer `cohere2` architecture, fewer community recipes, more integration friction |
| License | Open weights, **non-commercial terms (CC-BY-NC-style)** — verify exact licence on the model card |

**Pros**
- Best native Hausa of the three by a wide margin → strongest African-use-case bonus and localisation story.
- Official Q4_K_M GGUF exists and runs through llama.cpp; fits the memory budget.
- Large multilingual vocab tokenises Hausa efficiently (fewer tokens per word).

**Cons**
- Slowest and heaviest of the three → weakest combined S_perf + S_eff.
- Multilingual breadth can trade off English depth → risk on the English MCQ that drives the 50%.
- Hardest to fine-tune (architecture maturity); higher schedule risk.
- Non-commercial licence complicates the commercialization prize.

---

## Recommendation

| Role | Model | Rationale |
|---|---|---|
| **Primary Candidate** | **Qwen2.5-1.5B** | Best speed + efficiency (half the score), Apache-2.0, fastest to fine-tune, clears the English MCQ bar with a strong domain dataset. The default submission model. |
| **Secondary Candidate** | **Qwen2.5-3B** | Accuracy upper bound; deploy only if the 1.5B's accuracy proves insufficient *and* it still clears the 7 GB / thermal limits with acceptable TPS. Mind the research licence. |
| **Experimental Candidate** | **Tiny Aya Earth** | Native-Hausa differentiator for the African-use-case bonus and localisation award; also usable as a Hausa data generator/translator for the dataset even if not submitted. Higher fine-tuning and licence risk. |

**Decision rule:** fine-tune and profile all three on the 840 G6, compute the composite
(`benchmarks/compute_composite.py`), and submit the highest scorer — expected to be the 1.5B
on the speed/efficiency-weighted formula. Keep Tiny Aya Earth in play as the localisation
engine regardless of the final model choice.

---

### Sources
- Q4_K_M sizes, `cohere2` architecture, and Hausa coverage for Tiny Aya: Cohere Labs Hugging Face model cards (`tiny-aya-earth-GGUF`, `tiny-aya-global`).
- Qwen2.5 licence terms (Apache-2.0 for 0.5B/1.5B; Qwen Research License for 3B): Qwen2.5 model cards — verify before submission.
- RAM/TPS values are development estimates to be replaced by ADTC-profiler measurements on the target-class laptop.
