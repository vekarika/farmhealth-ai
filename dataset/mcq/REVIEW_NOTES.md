# MCQ Batch 1 — Review Notes

Review of `mcq_batch1.jsonl` (20 items) across: factual accuracy, Hausa quality, encoding,
distractor quality/balance, and MCQ_SCHEMA compliance. Output: `mcq_batch1_reviewed.jsonl`.

## 1. Factual agricultural accuracy
- **No incorrect answers found.** All 20 keyed answers are agronomically/veterinarily sound
  (N-deficiency pattern, fall armyworm signs, striga, brooding temps, feed sequence, Newcastle/
  coccidiosis/Gumboro differentials, planting timing, PICS storage, germination test, legume haulms).
- Caveat: these remain **drafts** — every item keeps `needs_source_check: true` until the
  specific figures (32-35 C, ~12-13% moisture, ~75% germination, "80% golden") are confirmed
  against the cited source. No drug/agrochemical dosages are asserted.

## 2. Hausa language quality
- The 4 Hausa items are comprehensible and roughly correct.
- **Fix applied:** `kasa` -> `ƙasa` (soil) in `mcq_crp_0003` (correct Boko orthography).
- **Still required (kept `hausa_reviewed: false`):** a fluent-speaker pass for full Boko
  orthography (hooked consonants ɓ/ɗ/ƙ, ƴ) and naturalness. ASCII spellings elsewhere are
  understandable but not standardized. Do not treat Hausa items as final until reviewed.

## 3. Character encoding
- **Clean.** No mojibake (no `â€”`, `Â`, `ï¿½`); file is valid UTF-8. Temperatures use "C"
  rather than the ° symbol to avoid any downstream encoding risk.

## 4. Distractor quality & MCQ balance
- **Answer position rebalanced:** was A6/B2/C5/D7 -> now **A5/B5/C5/D5**.
- **Length tells fixed:** 9 items had the correct option markedly longer than its distractors
  (a tell, and an `acc_norm` bias). Trimmed to length-matched options; 1 unavoidable remainder
  (disease names in `mcq_lvh_0001`).
- **Weak/off-type distractors replaced:**
  - `mcq_crp_0001`: "Too much sunlight" / "virus" -> "Potassium deficiency" / "Waterlogging" (all same-type causes).
  - `mcq_lvk_0002`: "They are moulting" -> "They are hungry".
  - `mcq_lvh_0002`: "Normal moulting" -> "Intestinal worm infestation" (same-type illness).

## 5. MCQ_SCHEMA compliance
- All 20 compliant: exactly 4 unique options A-D, single valid `correct_answer`, required fields present.
- **Added** `needs_source_check` and `hausa_reviewed` to every record (present in the spec's intent
  but missing from the original batch1 file).

---

## Recommendations before scaling to 100+

1. **De-duplicate reasoning.** `mcq_crp_0004` and `mcq_wea_0004` are both "late rains -> early-maturing
   variety." Keep one; rewrite the other to a distinct concept (e.g., intercropping, fertilizer timing).
2. **Re-tag or relocate `mcq_wea_0003`** (poultry heat stress under `weather`). Defensible as
   climate-driven, but confirm against the official validation samples' category convention.
3. **Soften self-answering hints.** `mcq_lvh_0003` names the "bursal organ," which points straight to
   Gumboro. Fine occasionally, but don't let every disease item state the pathognomonic clue.
4. **Enforce as authoring rules at scale:** length-matched options · cycle answer positions evenly ·
   same-type distractors · verify every quantitative fact against `source_reference` · native Hausa
   review with proper orthography.
5. **Do not scale until the official ADTC agriculture validation samples are reviewed** — they may
   change option count, phrasing, or category conventions.
