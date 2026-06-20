# FarmHealth AI — Domain Ownership Map (v0.1)

The foundational artifact. Everything downstream is built from this:
**dataset blueprint · fine-tuning blueprint · RAG corpus blueprint · benchmark coverage
checklist · REPORT.md outline · live-defense narrative.**

---

## Positioning (locked)

| Field | Value |
|---|---|
| Primary domain | Agriculture |
| Product identity | **FarmHealth AI** — offline agricultural & livestock-health advisor for African farmers and extension officers |
| Technical cross-disciplinary integration | **Offline RAG** (Information Retrieval × Agriculture) — the *load-bearing* component |
| Secondary domain expertise | Health Sciences (livestock health, disease prevention, biosecurity) |
| Region of depth | Northern Nigerian belt — Nasarawa, Kaduna, Adamawa, Kwali |
| Languages | English (primary) + Hausa |

Identity = livestock-health advisor. Declared technical integration = retrieval. Both true,
both pulling different scoring lines. Don't let one replace the other in the defense.

---

## The organizing principle: STABLE vs VOLATILE

Every leaf is tagged **[S]** or **[V]**. This is what makes the map serve two artifacts at once.

- **[S] Stable knowledge** → goes into the **fine-tuning dataset** (lives in model weights).
  Diagnoses, husbandry, prevention, agronomic reasoning. Doesn't change by week or village.
- **[V] Volatile / local knowledge** → goes into the **RAG corpus** (retrieved at runtime).
  Market prices, per-LGA planting calendars, current outbreak advisories, input costs.

Deletion test for the defense: remove retrieval → every **[V]** fact vanishes, leaving only
generic advice. That is what makes the RAG load-bearing, not cosmetic.

---

## Taxonomy (expanded for real northern-belt coverage)

### Level 1 — Crops  · integration: Agronomy
Core staples (build depth here):
- **Maize** [S], **Sorghum (guinea corn)** [S], **Millet** [S], **Rice (lowland/upland)** [S]
- **Cowpea (beans)** [S], **Groundnut** [S], **Soybean** [S]
- **Cassava** [S], **Yam** [S]
- *(secondary, lighter coverage):* sesame, tomato, pepper, onion
- Per crop, cover: variety/planting window [S][V-calendar], spacing & seed rate [S],
  nutrient management [S], weed/pest/disease [S], harvest & storage [S]

### Level 2 — Livestock  · integration: Animal husbandry
- **Poultry** (broilers, layers, local/noiler) [S]
- **Goats** (Red Sokoto, WAD) [S]
- **Sheep** (Balami, Uda) [S]
- **Cattle** (smallholder dairy/beef) [S]
- Per animal, cover: housing [S], feeding/rations [S], breeding [S], routine care [S]

### Level 3 — Livestock Health  · integration: **Health Sciences** (heaviest weight)
This is the FarmHealth identity — depth here is the differentiator.
- **Poultry:** Newcastle disease [S], coccidiosis [S], Gumboro/IBD [S], fowl pox [S],
  fowl typhoid [S]
- **Small ruminants:** PPR (peste des petits ruminants) [S], mange/mites [S], pneumonia [S]
- **Cattle:** mastitis [S], foot-and-mouth disease [S], tick-borne diseases [S]
- **Cross-cutting:** symptom-based triage [S], **biosecurity & isolation** [S],
  vaccination scheduling [S][V-local outbreak alerts], deworming [S]
- **Safety rule:** educational + prevention + biosecurity focus. Name the disease, the signs,
  prevention, and *when to call a vet*. **No specific drug names or dosages** — defer to the
  vet / product label, exactly as agrochemical rates are deferred.

### Level 4 — Weather & Climate  · integration: Climate Science
- Drought response & drought-tolerant choices [S]
- Flooding / waterlogging management [S]
- **Rainfall onset & cessation timing** [S][V-seasonal forecast]
- Heat stress (crops & livestock) [S]
- Activity prioritisation by weather ("what to do during heavy rain") [S]

### Level 5 — Farm Operations  · integration: Agronomy / Animal husbandry
- Storage (hermetic/PICS, drying to safe moisture) [S]
- Harvest timing & maturity signs [S]
- Fertilizer use & deficiency diagnosis [S]
- Feed & ration management [S]
- **Biosecurity** (ties into Level 3) [S]

### Level 6 — Markets  · integration: Agricultural Economics
- Sell-vs-store decisions & price seasonality [S]
- **Current local prices** [V] · **input costs** [V]
- Post-harvest losses & grading [S]
- Aggregation / cooperatives, simple margin math [S]

---

## Dataset quota grid — v0.1 gold set (~285 examples)

Fill this grid; don't free-style. A *defined* 285 beats a sprawling 2,000.

| Category | EN | Hausa | Total | Integration tag |
|---|---:|---:|---:|---|
| Crops | 40 | 20 | 60 | Agronomy |
| Livestock | 30 | 15 | 45 | Animal husbandry |
| **Livestock Health** | 50 | 25 | 75 | **Health Sciences** |
| Weather & Climate | 20 | 10 | 30 | Climate Science |
| Farm Operations | 30 | 15 | 45 | Agronomy / Husbandry |
| Markets | 20 | 10 | 30 | Agricultural Economics |
| **Total** | **190** | **95** | **285** | — |

Within each cell, vary the **question archetype**: diagnostic, how-to, timing, quantitative
(conservative), comparison/choice, market, safety/correction. Hold out ~10% (≈28 examples,
English) as an eval set you never train on, to detect Hausa-vs-English accuracy trade-offs.

---

## RAG corpus blueprint (the [V] tags, gathered)

These are the documents the retrieval layer owns — the volatile/local data the model can't
hold. Keyed by location (state/LGA) where relevant.

| Corpus document | Source to gather from | Keyed by |
|---|---|---|
| Per-LGA planting calendars / windows | NAERLS/ABU, state ADP bulletins | LGA |
| Local market price sheets (staples) | local market surveys, commodity boards | market/town + date |
| Input cost sheets (seed, fertilizer, feed) | agro-dealer surveys | town + date |
| Pest/disease outbreak advisories | NAERLS, vet services, ADP alerts | region + date |
| Crop & livestock factsheets (canonical) | IITA, ICRISAT, FAO, extension manuals | crop/animal |

The [S] dataset teaches reasoning and language; this corpus supplies the dated, placed facts.

---

## Benchmark coverage checklist (does the gold set cover the map?)

Before fine-tuning, confirm every Level has ≥ its quota AND spans archetypes:
- [ ] Each core crop has ≥1 diagnostic + ≥1 timing + ≥1 nutrient/storage example
- [ ] Each livestock species has husbandry + ≥1 named disease
- [ ] Every Level-3 disease appears with signs + prevention + biosecurity
- [ ] Weather has activity-prioritisation + drought + flood
- [ ] Markets has ≥1 sell-vs-store + ≥1 quantitative margin example
- [ ] EN:HA ratio ≈ 2:1 in every category, not just overall
- [ ] ≥10% quantitative items; numbers verified against a real source
- [ ] Hausa reviewed by a fluent speaker

---

## How this map feeds each deliverable

| Artifact | What it pulls from the map |
|---|---|
| Fine-tuning dataset | all [S] leaves × quota grid × archetypes |
| RAG corpus | all [V] leaves → corpus blueprint table |
| `metadata.json` test prompts | 1 crop diagnostic (EN) + 1 livestock-health (HA) — both load-bearing |
| `REPORT.md` | Levels 1–6 → problem scope; STABLE/VOLATILE split → design-decisions section |
| Live defense | "Model reasons (fine-tuned [S]); retrieval supplies dated/local facts ([V]). Remove retrieval and the prices, calendars, and outbreak alerts disappear." |
| Cross-disciplinary justification | Integration tags column → one named discipline per Level |

---

## Authoring rules for the gold set (the quality bar)

1. Real farmer/officer voice in the question; specific (state, growth stage, symptom, season).
2. Answer: practical, 3–7 sentences, region-appropriate, no markdown.
3. **No drug/agrochemical dosages** — name the IPM/biosecurity approach, defer exact rates to
   label/vet/extension officer.
4. Verify every number against a real source before it enters training.
5. Hausa must be fluent-reviewed — it is the difference between earning the bonus and a liability.
6. Teach *reasoning patterns*, not memorised Q&A pairs — this is the real defense against
   overfitting on the hidden prompts.
