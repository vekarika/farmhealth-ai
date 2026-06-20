# FarmHealth AI — DATASET_SPEC.md (v0.1)

The manufacturing blueprint for the 285-example gold dataset. Every example is authored
against this spec so the set is auditable against the quota grid and consistent in structure.

Architecture principle (state this in the defense verbatim):
**"Stable agricultural reasoning is embedded in the model through fine-tuning. Dynamic,
location-specific information — prices, planting calendars, advisories — is retrieved offline
from local knowledge stores."** → *Model reasons; retrieval localizes.*

---

## 1. Updated category quota grid (~285, Decision Support added)

| Category | EN | HA | Total | Integration tag |
|---|---:|---:|---:|---|
| Crops | 37 | 18 | 55 | Agronomy |
| Livestock | 30 | 15 | 45 | Animal husbandry |
| **Livestock Health** | 50 | 25 | 75 | **Health Sciences** |
| Weather & Climate | 20 | 10 | 30 | Climate Science |
| Farm Operations | 27 | 13 | 40 | Agronomy / Husbandry |
| Markets | 17 | 8 | 25 | Agricultural Economics |
| **Decision Support** | 10 | 5 | 15 | Reasoning (cross-cutting) |
| **Total** | **191** | **94** | **285** | — |

EN:HA ≈ 2:1 in every row, not just overall. Hold out ~28 EN examples (10%) as a never-trained eval set.

---

## 2. Authoring record schema (one row per example)

Maintain the dataset as JSONL where each line carries `messages` **plus** a `meta` block.
The `meta` block is for authoring/audit only — it is **stripped** before training (§6).

```json
{
  "messages": [
    {"role": "system",    "content": "<system persona>"},
    {"role": "user",      "content": "<farmer/officer question>"},
    {"role": "assistant", "content": "<structured answer>"}
  ],
  "meta": {
    "id": "lvh_pol_0007",
    "category": "livestock_health",
    "subject": "poultry / Newcastle",
    "lang": "en",
    "archetype": "diagnostic",
    "reasoning_pattern": "observe_diagnose_explain_act",
    "sv": "S",
    "difficulty": "basic",
    "location": null,
    "source_reference": "verify: veterinary/extension poultry-health guide",
    "needs_source_check": true,
    "hausa_reviewed": false
  }
}
```

> `source_reference` and `needs_source_check` are **authoring-only provenance pointers** — they
> name the source to *verify against*, not a confirmed citation. They are stripped before training
> and feed the data-provenance section of REPORT.md.

### Field reference

| Field | Values | Notes |
|---|---|---|
| `id` | `cat_subj_NNNN` | stable unique id; lets you audit coverage |
| `category` | one of the 7 grid rows | drives quota counting |
| `subject` | crop/livestock + topic | e.g. `maize / nutrient`, `goats / PPR` |
| `lang` | `en` \| `ha` | drives the 2:1 split |
| `archetype` | diagnostic · how_to · timing · quantitative · comparison · market_decision · safety_correction | drives the reasoning template (§3) |
| `reasoning_pattern` | see §3 | matched to archetype |
| `difficulty` | basic · intermediate · advanced | deliberate complexity spread (see below) |
| `sv` | `S` \| `V` | S → fine-tune; V → flag, prefer RAG (see §5) |
| `location` | `{state, lga, season}` or `null` | populate **only** when load-bearing (§4) |
| `source_reference` | string (authoring-only) | source to verify against (FAO/IITA/ICRISAT/extension/vet) — not a confirmed citation |
| `needs_source_check` | bool | true until a human verifies any quantitative claim |
| `hausa_reviewed` | bool | HA rows are not "done" until true |

**Difficulty distribution** (deliberate — hidden prompts won't all be beginner-level):

| Level | Share | Example |
|---|---:|---|
| basic | 50% | "What causes yellowing in lower maize leaves?" |
| intermediate | 35% | "How do I tell nitrogen deficiency from drought stress in maize?" |
| advanced | 15% | "Rains started two weeks late in Kaduna — should I switch maize to sorghum, and why?" |

---

## 3. Reasoning templates by archetype (NOT one universal template)

Each archetype has its own answer skeleton. This teaches reasoning that generalizes to hidden
prompts without forcing rigid five-paragraph answers onto simple questions.

| Archetype | `reasoning_pattern` | Answer skeleton |
|---|---|---|
| diagnostic | `observe_diagnose_explain_act` | Observation restated → likely cause(s) → why → immediate action → prevention/biosecurity → when to escalate (vet/extension) |
| how_to | `goal_steps_caution_check` | Goal → ordered steps → key cautions → how to know it worked |
| timing | `condition_window_caveat` | Trigger condition → recommended window → what to avoid → fallback if late/early |
| quantitative | `figure_apply_caveat` | Conservative figure/rate → how to apply → verify-with-label/local caveat → why timing/splitting matters |
| comparison | `options_tradeoffs_reco` | Options → trade-offs of each → recommendation tied to the stated condition |
| market_decision | `situation_factors_rule_reco` | Current situation → key factors (incl. [V] price/seasonality) → decision rule → recommendation + caveat |
| safety_correction | `acknowledge_risk_correct_safe` | Acknowledge intent → why the proposed action is risky → correct approach → safe practice/PPE |

> ⚠️ Benchmark-format dependency: if the organizers confirm the accuracy eval is
> **multiple-choice**, tighten all answers and add a parallel MCQ-formatted track. If it is
> **free-text panel-graded**, these structured answers are ideal. Lock answer length after their reply.

---

## 4. Location-awareness rules (conditional)

Populate `location` **only when the answer changes by place or season**:

- **Populate** for: timing/planting windows, weather/climate, market prices, input costs,
  outbreak advisories, region-specific variety choice.
- **Leave `null`** for: universal agronomy/husbandry (how Newcastle spreads, what nitrogen
  deficiency looks like, how to set up a brooder). Don't bolt "in Kaduna" onto universal facts.

When populated, prefer the target belt: Nasarawa, Kaduna, Adamawa, Kwali. Season values:
`early_rains` · `peak_rains` · `late_rains` · `harvest` · `dry_season`.

---

## 5. Stable vs Volatile in practice

- `sv: "S"` → the answer is durable knowledge → **goes into fine-tuning**. Most of the 285.
- `sv: "V"` → the answer depends on dated/local data (today's price, this LGA's calendar) →
  the gold example should **teach the model to defer to / use retrieved data**, e.g. "current
  prices vary by market — check your local price sheet; the decision rule is…". The actual
  numbers live in the RAG corpus, not the training answer. This keeps the model from memorising
  stale prices and makes retrieval load-bearing.

---

## 6. Training export (messages-only)

The fine-tune script consumes only `messages`. Strip `meta` on export:

```bash
# authoring file (with meta)  ->  training file (messages only)
jq -c '{messages: .messages}' training/data/gold_authoring.jsonl > training/data/agri_train.jsonl
```

Audit coverage from the authoring file before exporting:

```bash
jq -r '.meta | [.category, .lang] | @tsv' training/data/gold_authoring.jsonl \
  | sort | uniq -c        # compare counts against the quota grid in §1
```

---

## 7. Worked examples (the bar to match)

### 7a — EN · livestock_health · diagnostic · [S] · location null

```json
{"messages":[
 {"role":"system","content":"You are FarmHealth AI, an offline agricultural and livestock-health advisor for farmers and extension officers in northern Nigeria. Give practical, region-appropriate advice. Answer in the language the user used."},
 {"role":"user","content":"My layers are eating less, coughing, and egg production has dropped sharply over three days. What is happening and what should I do?"},
 {"role":"assistant","content":"Reduced feed intake, coughing, and a sudden drop in egg production together point to a respiratory disease — Newcastle disease is the most likely and most dangerous candidate in our area, though infectious bronchitis can look similar. Because Newcastle spreads fast and kills, act now rather than wait: isolate the affected birds from the rest of the flock immediately and restrict all movement of people and equipment between pens. Give clean water and easily eaten feed to keep weaker birds going, and disinfect feeders, drinkers and footwear. Do not introduce any new birds. The real protection is prevention through vaccination and biosecurity, so going forward keep a strict Newcastle vaccination schedule. If mortality is rising or you are unsure of the cause, contact an animal-health officer or veterinarian quickly — early confirmation changes how much of the flock you can save."}],
 "meta":{"id":"lvh_pol_0007","category":"livestock_health","subject":"poultry / Newcastle","lang":"en","archetype":"diagnostic","reasoning_pattern":"observe_diagnose_explain_act","sv":"S","location":null,"needs_source_check":true,"hausa_reviewed":false}}
```

### 7b — HA · markets / decision_support · market_decision · [V] · location populated

```json
{"messages":[
 {"role":"system","content":"You are FarmHealth AI, an offline agricultural and livestock-health advisor for farmers and extension officers in northern Nigeria. Give practical, region-appropriate advice. Answer in the language the user used."},
 {"role":"user","content":"Na girbe masara a Kaduna. In sayar yanzu ko in adana don in jira farashi ya hau?"},
 {"role":"assistant","content":"Wannan ya dogara da ko za ka iya adana masara cikin aminci. Farashin masara yana da tsari da ake iya hasashe: yana da rahusa lokacin girbi saboda kowa na sayarwa, kuma yana hauhawa zuwa lokacin damina mai zuwa da lokacin karanci. Doka mai sauki: idan kana da wuri mai kyau na adanawa, ka bushe masara sosai ka sa a cikin jakar hermetic (PICS) don kare ta daga kwari da fumfuna, sannan ka jira ka sayar lokacin karanci inda farashi ke kan gaba. Amma idan adanar ka ba ta da tabbas ko kana bukatar kudi yanzu, ka sayar da rabi yanzu ka adana rabi. Ka duba farashin kasuwarka ta yanzu (ka kalli jadawalin farashi na cikin gida) kafin ka yanke shawara, domin farashi yana sauyawa daga kasuwa zuwa kasuwa."}],
 "meta":{"id":"mkt_dec_0003","category":"decision_support","subject":"maize / sell-vs-store","lang":"ha","archetype":"market_decision","reasoning_pattern":"situation_factors_rule_reco","sv":"V","location":{"state":"Kaduna","lga":null,"season":"harvest"},"needs_source_check":true,"hausa_reviewed":false}}
```

Note how 7b is `sv:"V"`: it teaches the *decision rule* and tells the user to consult the local
price sheet — it does **not** bake in a specific price. The price lives in the RAG corpus.

---

## 8. Authoring quality gates (every example must pass)

1. Real farmer/officer voice; specific (state, stage, symptom, season where relevant).
2. Answer follows its archetype skeleton (§3); 3–7 sentences unless format dictates otherwise.
3. **No drug or agrochemical dosages** — name the IPM/biosecurity approach; defer exact rates
   to the label / vet / extension officer.
4. Every quantitative claim verified against a real source → flip `needs_source_check` to false.
5. HA rows fluent-reviewed → flip `hausa_reviewed` to true. Unreviewed HA does not ship.
6. `sv:"V"` answers teach deferral to retrieved data, never memorised prices/dates.
7. Teach the reasoning pattern, not a memorised pair — the real hidden-prompt defense.
