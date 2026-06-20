# FarmHealth AI — MCQ_SCHEMA.md (v1)

Canonical **multiple-choice** format for FarmHealth AI — the format ADTC scores accuracy in.
The profiler runs lm-evaluation-harness (`--model gguf`) against the **bare GGUF**, reads
`acc_norm` (length-normalized MCQ accuracy), so the model must make the **correct option the
most probable completion**. RAG is not in this loop.

> Provisional until the official agriculture validation samples are reviewed; ARC-compatible.

---

## Canonical record (exact fields)

```json
{
  "id": "mcq_crp_0001",
  "category": "crops",
  "subject": "maize / nutrient",
  "language": "en",
  "difficulty": "basic",
  "question": "A maize farmer's lower leaves are yellowing from the tip inward in a V-shape after heavy rain on sandy soil. What is the most likely cause?",
  "options": {
    "A": "Too much sunlight",
    "B": "Nitrogen deficiency",
    "C": "Phosphorus deficiency",
    "D": "A virus spread by insects"
  },
  "correct_answer": "B",
  "explanation": "Yellowing from the tip of the oldest lower leaves in a V is classic nitrogen deficiency, worsened by leaching on sandy soil after rain. Phosphorus shows as purpling; the others don't give this pattern.",
  "source_reference": "verify: IITA maize agronomy guide"
}
```

## Field definitions

| Field | Description |
|---|---|
| `id` | `mcq_<cat3>_NNNN`, unique |
| `category` | crops · livestock · livestock_health · weather · farm_operations |
| `subject` | crop/animal + topic, e.g. `poultry / Newcastle` |
| `language` | `en` (benchmark-primary) or `ha` |
| `difficulty` | basic · intermediate · advanced |
| `question` | standalone stem; answerable without external context |
| `options` | object with exactly 4 keys `A`–`D`; plausible, mutually exclusive, similar length |
| `correct_answer` | the single correct option key (`A`–`D`) |
| `explanation` | why the answer is right and distractors wrong (authoring/review; strip before eval) |
| `source_reference` | source to verify against — not a confirmed citation |

## Difficulty

| Level | Tests | Target |
|---|---|---|
| basic | single-fact recall; symptom → cause | 50% |
| intermediate | distinguish similar options; apply a rule | 35% |
| advanced | multi-step reasoning; conditional decision | 15% |

## Authoring & distractor rules (for lm-eval scoring)

1. **Exactly one defensibly-correct answer** — an agronomist/vet agrees without argument.
2. **4 options, same type** — if the answer is a disease, all options are diseases; if a nutrient, all nutrients.
3. **Plausible distractors** from real misconceptions / look-alike conditions, **similar in length**
   to the correct option (`acc_norm` normalizes by length — a longer correct answer is a tell and a bias).
4. **No "all/none of the above"**, no synonyms, no joke options, no grammatical clue to the answer.
5. **Vary `correct_answer` position** across the file (roughly even A/B/C/D).
6. **No drug/agrochemical dosages** as the correct answer; region-appropriate (northern Nigeria).
7. Design so the **correct option is the most probable continuation** of the question stem.

## Validation checklist

- [ ] 4 options A–D, unique, similar length; `correct_answer` valid and singular
- [ ] standalone stem; no giveaway
- [ ] category/subject/language/difficulty tagged
- [ ] no dosages; region-appropriate; fact verified against `source_reference` before training
- [ ] Hausa items reviewed by a fluent speaker
- [ ] answer positions varied across the file

## lm-eval / ARC export

Map to ARC: `{question, choices:{text:[...A,B,C,D], label:["A","B","C","D"]}, answerKey: correct_answer}`.
Strip `explanation` and `source_reference` before eval export.
