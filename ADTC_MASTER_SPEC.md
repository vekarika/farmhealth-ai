# ADTC 2026 — Master Spec & Rules (AUTHORITATIVE, v2)

Updated from the official DevPost Rules, Resources, and submission-template README
(retrieved while logged in). This supersedes the microsite-based v1. Conflicts from v1 are
now resolved and marked ✓.

---

## 1. Snapshot

| Fact | Value |
|---|---|
| Name | Africa Deep Tech Challenge 2026 — "Laptop LLM Challenge" |
| What | On-device LLM app, zero cloud, on the ADTC Standard Laptop; one domain + a load-bearing cross-disciplinary integration |
| Team size | 1–3 |
| Runtime | llama.cpp only, GGUF only |
| **Gate 1 deadline** | **Tuesday, August 25, 2026** ✓ (was wrongly July 24 on the microsite) |
| Total prize | $20,000 ($16,500 cash + $3,500 GPU credits) |
| Our domain | Agriculture (en + ha) — product: **FarmHealth AI** |
| Eligibility | Nigeria ✓ listed · 18+ ✓ · early-stage rules apply (see §11) |

---

## 2. Official timeline

| Date | Stage | Notes |
|---|---|---|
| Jun 16, 2026 | Launch | domains, hardware profile, profiler, **validation-set samples published** |
| **Aug 25, 2026** | **Gate 1 deadline** | **proposals + prototypes. Two-step judging: proposal screen → prototype review of top ~10%** |
| Sep 8, 2026 | Semifinalists (≤20) | Gate 2 narrowing audit begins |
| Sep 29, 2026 | Finalists (≤10) | live-defense prep opens |
| Oct 17, 2026 | Live Defense & Awards | remote pitches, technical Q&A, winners same day |

Implication: documentation/proposal quality is **gating** at Gate 1 (it's screened before deep prototype review).

---

## 3. Domains — pick ONE
math_scientific_reasoning · healthcare_medical · **agriculture** ← ours · creative_writing ·
coding_assistants · corporate_enterprise · autonomous_ai_agents
(Note: profiler JSON-schema enum omits autonomous_ai_agents; irrelevant to us.)

---

## 4. What to submit (Gate 1)
- [ ] Public GitHub repo from the official template (GPL-3.0)
- [ ] `metadata.json` fully filled — **no placeholder values**, exactly 2 test prompts
- [ ] `download_model.sh` pulls a valid public `.gguf` into `model/` (idempotent, no creds)
- [ ] `*.gguf` and `model/` in `.gitignore` (never commit weights)
- [ ] `REPORT.md` — problem · constraints · design alternatives & decisions · tools · benchmarks (1–3 pages)
- [ ] Screenshots / short clips of the build running
- [ ] 2-minute video (solution + journey)
- [ ] Runs 100% offline during evaluation

---

## 5. Hardware standard
4 vCPU · 8 GB DDR4 · integrated graphics only · 256 GB SSD · Ubuntu 22.04 · i5 10–12th gen / Ryzen 5 3000–5000.

---

## 6. Scoring

```
S_total = 0.50·S_acc + 0.30·S_perf + 0.20·S_eff − P_thermal   (+ up to 10 use-case bonus pts)
```

| Component | Weight | Notes |
|---|---|---|
| Accuracy S_acc | 50% | **multiple-choice benchmarks + qualitative** (prompt accuracy, documentation quality). MCQ runs on the model. ✓ |
| Speed S_perf | 30% | `100×(TPS/TPS_max)`; provisional `TPS_REF = 15` |
| Efficiency S_eff | 20% | `100×((7−PeakRAM)/7)`; 7 GB budget |
| Thermal | −10 | if throttled or temp > 85 °C |
| OOM/crash | DQ | S_total = 0 |
| **African Use Case bonus** | **+ up to 10 pts (additive)** ✓ | applicability to a real African use case — broader than language |

Judges download the `.gguf` (locked to submission-time git commit) and run it offline in
LM Studio / Ollama / Open WebUI. Speed/efficiency/thermal automated; accuracy = MCQ + panel.

---

## 7. Prizes (official) ✓

| Award | Cash | Non-cash |
|---|---|---|
| Grand | $8,000 | 6-mo residency, pilot matchmaking, demo day |
| Second | $4,000 | 3-mo residency, pilot, demo day |
| **3rd Place** | $3,000 | 3-mo residency, demo day |
| **Best African Use Case** | $1,500 | 3-mo residency |
| Finalist stipends ×10 | $250 GPU each | network access |
| Semifinalist stipends ×20 | $50 GPU each | prototyping support |

**No "Best Integration Award" exists** (microsite error). Cross-disciplinary RAG feeds S_acc
qualitative only. Total $20,000.

---

## 8. Eligibility (official) — our status

- Residency: **Nigeria listed ✓**; age 18+ ✓.
- **Venture age < 12 months** as of Jun 16, 2026 (incorporations/registrations/organized teams).
- **Product stage**: ideation / conceptual / early PoC; **not commercially launched**, no mature MVP > 6 months, no active MRR.
- **Funding cap**: ≤ $25,000 external dilutive or grant capital.
- Honor system at registration; **finalists background-checked**; misrepresentation → DQ + prize clawback.
- **ACTION:** enter as an individual builder / new ≤12-mo team. Do NOT attach to KGTG/SCL or any
  established company. FarmHealth AI as a fresh PoC complies on all counts. Declare truthfully.

---

## 9. Tools & resources (from official Resources tab)
- **Apply for up to 5 hours of GPU credits (Udutech) to TRAIN** — apply now, covers the fine-tune.
- Stack confirmed: Ollama, llama.cpp (OpenBLAS), llama-bench, ollama-benchmark.
- 8 GB tuning: `vm.swappiness`, `--mlock` to pin model in RAM; GGUF mmap loading.
- Thermal: lm-sensors + thermald + CPU governor to stay < 85 °C (the −10 penalty).
- Quant: Q4_K_M = sanctioned sweet spot.
- **Masakhane** (github.com/masakhane-io) — African NLP datasets incl. Hausa → dataset source.
- **Cohere Aya (3B)** — multilingual offline candidate (African languages) → optional benchmark entry.
- Support: challenge@africadeeptech.org · Discord: bit.ly/ADTC_Discord.

---

## 10. Open items (post-authoritative)

| Item | Status |
|---|---|
| Eligibility (Nigeria/age) | ✓ confirmed |
| Gate-1 deadline | ✓ Aug 25, 2026 |
| Bonus form | ✓ +10 additive use-case points |
| Prize labels | ✓ 3rd place + Best African Use Case |
| MCQ in accuracy | ✓ confirmed present → add MCQ dataset track |
| **Validation-set samples** | ⏳ PUBLISHED — **download from Resources now** (defines MCQ format) |
| Bare-model vs app for accuracy | ⏳ still worth confirming on Discord, but MCQ-on-model strongly indicated |
| GPU credits (Udutech, 5 h) | ⏳ apply now |

---

## 11. How our build maps (current)
- Repo/template, metadata (schema-valid), download_model.sh, .gitignore → done.
- Dataset: DOMAIN_MAP + DATASET_SPEC + 34 gold (free-text) → feeds fine-tune + qualitative.
  **Add: MCQ track mirroring the published validation samples.**
- Benchmark kit (TPS/RAM/quality → composite) → run on the 840 G6.
- RAG (location-aware retrieval) → cross-disciplinary requirement + qualitative (no prize, still required).
- Bonus: African use-case is core to the whole project (≤10 pts); Hausa is one lever.
