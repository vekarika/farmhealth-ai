#!/usr/bin/env python3
"""
mcq_batch1.jsonl — 20 MCQs derived from FarmHealth AI gold examples, to MCQ_SCHEMA.md v1.
5 categories x 4 = 20. Difficulty 10/7/3 (50/35/15). Mostly English + a few Hausa.
Correct-answer positions are shuffled deterministically (even A/B/C/D).

Run: python dataset/mcq/build_mcq_batch1.py  ->  dataset/mcq/mcq_batch1.jsonl

DRAFTS: facts to verify against source_reference; Hausa needs fluent review. No dosages.
"""
import json
import random
from pathlib import Path

LBL = ["A", "B", "C", "D"]

# (id, category, subject, language, difficulty, source_ref, question,
#  [correct, distractor, distractor, distractor], explanation)
M = [
 # ── CROPS ───────────────────────────────────────────────────────────────────
 ("mcq_crp_0001","crops","maize / nutrient","en","basic","verify: IITA maize agronomy guide",
  "A maize farmer's lower leaves are yellowing from the tip inward in a V-shape after heavy rain on sandy soil. What is the most likely cause?",
  ["Nitrogen deficiency","Phosphorus deficiency","Too much sunlight","A virus spread by insects"],
  "Yellowing from the tip of the oldest lower leaves in a V is classic nitrogen deficiency, worsened by leaching on sandy soil after rain. Phosphorus shows as purpling; the others don't give this pattern."),
 ("mcq_crp_0002","crops","maize / pest","en","basic","verify: FAO fall armyworm IPM guide",
  "Young maize shows 'windowpane' patches on new leaves and moist sawdust-like frass in the whorl. Which pest is most likely?",
  ["Fall armyworm","Stem borer","Grasshoppers","Termites"],
  "Windowpane feeding plus wet frass in the whorl is the signature of fall armyworm. Stem borers tunnel stems, grasshoppers chew edges, termites attack near soil."),
 ("mcq_crp_0003","crops","sorghum / striga","ha","intermediate","verify: ICRISAT striga guide",
  "Wata ciyawa mai launin shunayya tana fitowa kusa da dawa da ta yi rauni duk da kasa tana da kyau. Mene ne mafi yiwuwa?",
  ["Striga (witchweed) tana cin saiwar dawa","Ciyawa talakawa tana gasa kawai","Furen dawa na yau da kullum","Ruwa ya yi yawa a gona"],
  "Striga is a purple-flowered parasitic weed that attaches to sorghum roots and stunts the crop even on good soil — the purple weed plus stunting is the giveaway."),
 ("mcq_crp_0004","crops","maize / variety","en","advanced","verify: IITA variety guide + ADP advisory",
  "In Kaduna the rains started two weeks late but are expected to be adequate. What is the soundest maize choice?",
  ["Plant an early-maturing variety to fit the shortened season","Plant a long full-season variety as usual","Abandon maize for the whole year","Plant immediately on the first light shower"],
  "A late-but-adequate season is best matched by an early-maturing variety so it matures in time. Full-season risks not finishing; abandoning or planting on one shower are poor calls."),
 # ── LIVESTOCK ───────────────────────────────────────────────────────────────
 ("mcq_lvk_0001","livestock","poultry / brooding","en","basic","verify: poultry husbandry manual",
  "What is the recommended brooder temperature near day-old chicks during the first week?",
  ["About 32-35 C","About 20-22 C","About 40-42 C","About 26-28 C"],
  "Week-one brooding temperature at chick level is about 32-35 C, reduced ~3 C per week. Lower is too cold; 40-42 C is too hot."),
 ("mcq_lvk_0002","livestock","poultry / brooding","en","basic","verify: poultry husbandry manual",
  "Chicks are huddling tightly directly under the heat source. What does this most likely mean?",
  ["They are too cold","They are too hot","The temperature is correct","They are moulting"],
  "Huddling under the heat means too cold; scattering to edges/panting means too hot; even spreading means correct."),
 ("mcq_lvk_0003","livestock","poultry / feeding","en","intermediate","verify: broiler feeding guide",
  "What is the correct broiler feed sequence from day-old to market?",
  ["Starter, then grower, then finisher","Finisher, then grower, then starter","Layer mash throughout","Grower only, start to finish"],
  "Broilers go starter (high protein, early) -> grower -> finisher (weight gain before market). The others mis-stage or use the wrong feed."),
 ("mcq_lvk_0004","livestock","poultry / biosecurity","ha","intermediate","verify: poultry biosecurity guide",
  "Yaya ya kamata ka yi da sabbin kaji da ka saya kafin ka hada su da garken?",
  ["Ka raba su (quarantine) na akalla mako biyu kafin ka hada","Ka hada su nan da nan da sauran kajin","Ka hada su daren farko kawai","Babu bukatar wani kariya"],
  "New birds should be quarantined ~2 weeks before mixing, to avoid importing disease into the flock. Immediate mixing defeats the purpose."),
 # ── LIVESTOCK HEALTH ────────────────────────────────────────────────────────
 ("mcq_lvh_0001","livestock_health","poultry / Newcastle","en","basic","verify: veterinary poultry-disease manual",
  "Several chickens die suddenly; others show greenish diarrhoea and a twisted neck. Which disease is most likely?",
  ["Newcastle disease","Coccidiosis","Gumboro (IBD)","Fowl pox"],
  "Sudden death + greenish diarrhoea + nervous signs (twisted neck) is classic Newcastle. Coccidiosis = bloody droppings; Gumboro = whitish diarrhoea; fowl pox = skin lesions."),
 ("mcq_lvh_0002","livestock_health","poultry / coccidiosis","en","intermediate","verify: veterinary poultry-disease manual",
  "Young birds on damp litter are droopy with ruffled feathers and bloody droppings. What is the most likely cause?",
  ["Coccidiosis","Newcastle disease","Gumboro (IBD)","Normal moulting"],
  "Bloody droppings in young birds on wet litter point to coccidiosis (an Eimeria parasite). Newcastle/Gumboro have different signs; moulting is not a disease."),
 ("mcq_lvh_0003","livestock_health","poultry / Gumboro","en","intermediate","verify: veterinary poultry-disease manual",
  "Birds around 4 weeks old show whitish watery diarrhoea, vent pecking and trembling, and the disease attacks their immune organ. Which is it?",
  ["Gumboro (infectious bursal disease)","Coccidiosis","Newcastle disease","Fowl cholera"],
  "Whitish watery diarrhoea, vent pecking, trembling in ~3-6 week birds attacking the bursa (immune organ) is Gumboro/IBD."),
 ("mcq_lvh_0004","livestock_health","poultry / Newcastle","ha","basic","verify: veterinary poultry-disease manual",
  "Mene ne kariya mafi muhimmanci daga cutar Newcastle a kaji?",
  ["Allurar rigakafi tare da biosecurity","Maganin antibiotic yana warkar da ita","Ware kaji kawai ba tare da rigakafi ba","Babu abin da za a iya yi"],
  "Newcastle has no cure once it strikes; prevention is vaccination plus biosecurity. Antibiotics don't cure a virus; isolation alone is insufficient."),
 # ── WEATHER & CLIMATE ───────────────────────────────────────────────────────
 ("mcq_wea_0001","weather","planting / timing","en","basic","verify: NAERLS planting calendar",
  "When is it safest to plant maize at the start of the rainy season?",
  ["After two or three steady rains, once the soil holds moisture","On the very first single rain of the season","During the dry season before any rain","Only after the rains have ended"],
  "Waiting for a stable onset (2-3 good rains) avoids seedlings dying in an early dry spell. The others are mistimed or out of season."),
 ("mcq_wea_0002","weather","flooding / management","en","basic","verify: extension water-management note",
  "A field is prone to waterlogging during heavy rains. Which practice best protects the crop?",
  ["Make ridges and provide good drainage channels","Add more water to balance the soil","Compact the soil so water sits on top","Remove all the topsoil"],
  "Ridging and drainage move excess water away from roots. Adding water, compacting, or stripping topsoil all worsen waterlogging."),
 ("mcq_wea_0003","weather","heat stress / poultry","en","intermediate","verify: poultry husbandry manual",
  "During intense heat, chickens are panting with open beaks. What is the best immediate action?",
  ["Provide shade, ventilation and cool clean water","Add more heat to the poultry house","Reduce their drinking water","Close all the air vents"],
  "Open-beak panting is heat stress; provide shade, ventilation and cool water. Adding heat, cutting water, or blocking airflow make it worse."),
 ("mcq_wea_0004","weather","drought / adaptation","en","advanced","verify: IITA variety guide",
  "Rains have started late and are expected to be short this season. Which maize strategy best secures a harvest?",
  ["Choose an early or extra-early maturing variety","Plant a long full-season variety as usual","Plant the seed much deeper than normal","Delay planting several more weeks"],
  "An early-maturing variety (~90 days) finishes before the rains cut off. Full-season may not mature; deeper planting and further delay don't fix a short season."),
 # ── FARM OPERATIONS ─────────────────────────────────────────────────────────
 ("mcq_fop_0001","farm_operations","storage / grain","en","basic","verify: extension PICS storage guide",
  "What is the most reliable low-cost way to protect stored maize grain from weevils?",
  ["Dry it well and seal it in triple-layer hermetic (PICS) bags","Store it loosely in an open basket for airflow","Sprinkle water on it to keep it cool","Keep it in a loosely tied ordinary sack"],
  "Drying to ~12-13% moisture then hermetic (PICS) storage starves weevils of oxygen, no chemicals needed. Airflow, moisture and loose sacks all let weevils thrive."),
 ("mcq_fop_0002","farm_operations","harvest / rice","ha","basic","verify: Africa Rice post-harvest guide",
  "Yaushe ne lokaci mafi kyau na girbin shinkafa?",
  ["Lokacin da kusan kashi 80 na hatsi suka zama rawaya kuma sun yi tauri","Lokacin da ganye har yanzu suke kore sosai","Nan da nan bayan fure","Lokacin da dukkan hatsi suke da madara"],
  "Rice is ready when ~80% of grains are golden and hard. Green leaves, just-after-flowering, and milky grains all mean it is immature."),
 ("mcq_fop_0003","farm_operations","seed / germination test","en","intermediate","verify: extension seed-testing guidance",
  "Before planting a whole field, a farmer tests 100 saved maize seeds and 75 sprout. What is the best action?",
  ["Plant a bit more thickly to compensate for the lower rate","Plant at the normal rate without changes","Discard all the seed as useless","Soak the seed in fertilizer to fix it"],
  "A ~75% germination rate is usable but reduced, so plant slightly thicker to compensate; below ~70% you'd replace the seed. Normal rate risks a thin stand."),
 ("mcq_fop_0004","farm_operations","feed / dry-season ration","en","advanced","verify: dry-season feeding guide",
  "To feed ruminants through the dry season when grass is scarce, which conserved residue gives the most protein?",
  ["Groundnut and cowpea haulms","Maize cobs","Rice straw","Cereal chaff"],
  "Legume haulms (groundnut, cowpea) are protein-rich and the best dry-season residue. Maize cobs, rice straw and chaff are bulky but low in protein."),
]

def main():
    out = Path(__file__).resolve().parent / "mcq_batch1.jsonl"
    pos = {l: 0 for l in LBL}
    cov = {}
    with out.open("w", encoding="utf-8") as f:
        for (id_, cat, subj, lang, diff, src, q, opts, expl) in M:
            assert len(opts) == 4, id_
            correct_text = opts[0]
            shuffled = opts[:]
            random.Random(id_).shuffle(shuffled)
            ci = shuffled.index(correct_text)
            rec = {
                "id": id_, "category": cat, "subject": subj, "language": lang,
                "difficulty": diff, "question": q,
                "options": {LBL[i]: shuffled[i] for i in range(4)},
                "correct_answer": LBL[ci], "explanation": expl, "source_reference": src,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            pos[LBL[ci]] += 1
            cov.setdefault(cat, {"n": 0, "en": 0, "ha": 0, "basic": 0, "intermediate": 0, "advanced": 0})
            cov[cat]["n"] += 1; cov[cat][lang] += 1; cov[cat][diff] += 1
    print(f"wrote {len(M)} MCQs -> {out}\n")
    print(f"{'category':<17}{'n':>3}{'EN':>4}{'HA':>4}{'bas':>5}{'int':>5}{'adv':>5}")
    for c, d in cov.items():
        print(f"{c:<17}{d['n']:>3}{d['en']:>4}{d['ha']:>4}{d['basic']:>5}{d['intermediate']:>5}{d['advanced']:>5}")
    tot = {k: sum(d[k] for d in cov.values()) for k in ('n', 'en', 'ha', 'basic', 'intermediate', 'advanced')}
    print(f"{'TOTAL':<17}{tot['n']:>3}{tot['en']:>4}{tot['ha']:>4}{tot['basic']:>5}{tot['intermediate']:>5}{tot['advanced']:>5}")
    print("\nanswer-position spread: " + ", ".join(f"{k}={v}" for k, v in pos.items()))

if __name__ == "__main__":
    main()
