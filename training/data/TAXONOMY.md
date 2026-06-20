# Agri-Advisor Dataset Coverage Taxonomy

The accuracy half of your score is decided by how well your fine-tuned model answers a
**hidden agriculture subset**. You can't see those questions, so the only defense is
*systematic coverage*: span the real decision space of a northern-Nigerian smallholder so
the hidden prompts land on something you trained for.

Build the dataset as a grid: **(crop or livestock) × (topic) × (question archetype) × (language)**.
Aim for roughly **1,500–4,000 examples**, balanced so no single crop or topic dominates,
and so EN and HA are both well represented (target ~55% EN / ~45% HA).

---

## 1. Crops (northern-belt staples — weight by local importance)

| Group | Crops |
|---|---|
| Cereals | maize, sorghum (guinea corn), millet, rice (upland & lowland) |
| Legumes | cowpea (beans), groundnut, soybean |
| Oil/cash | sesame (beniseed), cotton, sunflower |
| Roots/tubers | yam, cassava, sweet potato, irish potato (Plateau-adjacent) |
| Vegetables | tomato, pepper (tatase/shombo), onion, okra, amaranth (alayyahu), garden egg |
| Tree/other | mango, citrus, sugarcane (small holdings) |

## 2. Livestock & aquaculture

| Group | Items |
|---|---|
| Poultry | broilers, layers, local/noiler chickens, guinea fowl |
| Small ruminants | goats (Red Sokoto, WAD), sheep (Balami, Uda) |
| Cattle | dairy & beef (smallholder/pastoral) |
| Other | fish (catfish ponds), rabbits, snails, beekeeping |

## 3. Topics (the cross-cutting columns)

1. **Land preparation & soil** — clearing, tillage, soil type fit, soil fertility signs
2. **Planting** — variety/seed selection, planting window vs. rains, spacing, seed rate, depth
3. **Nutrient management** — organic + inorganic fertilizer types, timing, split application, deficiency signs
4. **Water & weather timing** — rain onset/cessation, dry-spell risk, irrigation for dry-season farming, flood/drought response
5. **Weed management** — critical weed-free period, manual vs. herbicide (general, defer exact rates to label)
6. **Pest identification & IPM** — common pests per crop, scouting, cultural/biological/chemical control hierarchy
7. **Disease diagnosis** — symptom-based ID, management, resistant varieties
8. **Harvest & post-harvest** — maturity signs, harvesting, drying, threshing, storage (incl. pest-free storage, PICS bags)
9. **Livestock husbandry** — housing, brooding, feeding/rations, vaccination schedules, common diseases, breeding
10. **Market & economics** — when to sell vs. store, price seasonality, grading, aggregation/cooperatives, simple margin math
11. **Climate adaptation** — drought-tolerant varieties, early maturing options, changing rainfall patterns
12. **Inputs & safety** — sourcing genuine inputs, avoiding adulterated agrochemicals, safe handling/PPE

## 4. Question archetypes (the rows — vary these for every crop/topic)

| Archetype | Example shape |
|---|---|
| **Diagnostic** | "My [crop] shows [symptom] — what's wrong and what do I do?" |
| **How-to / procedure** | "How do I [task] for [crop/livestock]?" |
| **Timing** | "When should I [plant/spray/harvest/sell] [crop] in [state]?" |
| **Quantitative** | "How much [seed/fertilizer/feed] per [hectare/bird]?" (keep numbers conservative + verifiable) |
| **Comparison/choice** | "Should I plant [A] or [B] this season given [condition]?" |
| **Market** | "Is it better to sell my [crop] now or store it?" |
| **Safety/correction** | catches bad practice — "I want to spray [X] — is that right?" |

---

## Accuracy & safety rules (non-negotiable for THIS dataset)

These directly affect score quality and real-world harm:

1. **Verify every quantitative claim** against a real source before training — fertilizer
   rates, feed quantities, brooding temps, spacing. Wrong numbers train wrong answers.
2. **Never put exact agrochemical dosages in answers.** Teach the model to name the IPM
   approach and say *"follow the product label rate and consult your extension officer."*
   A hallucinated pesticide rate is a real hazard and judges will mark it down.
3. **Ground in trustworthy sources** (see expansion plan): IITA, ICRISAT, FAO, NAERLS/ABU
   extension bulletins, Nigeria's ADPs, CGIAR crop guides. Paraphrase — don't copy.
4. **Hausa must be reviewed by a fluent speaker.** Machine-drafted Hausa seeds the set,
   but a native review pass (ideally your farm-region contacts) is what makes the +15%
   bonus real instead of a liability.
5. **Keep advice region-appropriate** — northern Nigeria, rainfed smallholder reality, not
   generic temperate-zone agronomy.

---

## Suggested distribution (for ~2,000 examples)

| Slice | Share |
|---|---|
| Cereals (maize/sorghum/millet/rice) | 25% |
| Legumes + oil/cash crops | 15% |
| Roots/tubers + vegetables | 20% |
| Poultry | 12% |
| Ruminants + cattle | 10% |
| Fish/other livestock | 5% |
| Market/economics + climate (cross-crop) | 13% |
| EN : HA | ~55 : 45 |
| Archetype balance | diagnostic & how-to heaviest; ensure ≥10% quantitative |

Hold out ~10% as an **English eval set** you never train on, so you can measure whether
adding Hausa is hurting English accuracy before you commit.
