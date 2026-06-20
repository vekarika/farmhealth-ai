#!/usr/bin/env python3
"""
mcq_batch1_reviewed.jsonl — QA-corrected version of mcq_batch1.jsonl.

Corrections applied (see REVIEW_NOTES.md):
  - answer positions balanced to exactly A/B/C/D = 5/5/5/5
  - over-long correct options trimmed so distractors are length-matched (acc_norm fairness)
  - weak/off-type distractors replaced (sunlight->nutrient; moulting->worms; moulting->hungry)
  - Hausa orthography fix: kasa -> kasa (soil) noted; minimal change, full native review still pending
  - hausa_reviewed stays false; needs_source_check stays true (facts still to verify)

Run: python dataset/mcq/build_mcq_batch1_reviewed.py
"""
import json
from pathlib import Path

LBL = ["A", "B", "C", "D"]

# (id, category, subject, language, difficulty, source_ref, question,
#  [correct, d1, d2, d3], explanation)
M = [
 ("mcq_crp_0001","crops","maize / nutrient","en","basic","verify: IITA maize agronomy guide",
  "A maize farmer's lower leaves are yellowing from the tip inward in a V-shape after heavy rain on sandy soil. What is the most likely cause?",
  ["Nitrogen deficiency","Phosphorus deficiency","Potassium deficiency","Waterlogging of the roots"],
  "Nitrogen deficiency yellows the OLDEST lower leaves in a V from the tip, worsened by leaching on sandy soil after rain. Phosphorus shows purpling; potassium scorches leaf margins; waterlogging affects the whole plant."),
 ("mcq_crp_0002","crops","maize / pest","en","basic","verify: FAO fall armyworm IPM guide",
  "Young maize shows 'windowpane' patches on new leaves and moist sawdust-like frass in the whorl. Which pest is most likely?",
  ["Fall armyworm","Stem borer","Grasshoppers","Termites"],
  "Windowpane feeding plus wet frass in the whorl is the signature of fall armyworm. Stem borers tunnel stems, grasshoppers chew edges, termites attack near soil."),
 ("mcq_crp_0003","crops","sorghum / striga","ha","intermediate","verify: ICRISAT striga guide",
  "Wata ciyawa mai launin shunayya tana fitowa kusa da dawa wadda ta yi rauni duk da \u0199asa tana da kyau. Mene ne mafi yiwuwa?",
  ["Striga (witchweed) tana cin saiwar dawa","Ciyawa talakawa tana gasa kawai","Ruwa ya yi yawa a gona","Furen dawa na yau da kullum"],
  "Striga is a purple-flowered parasitic weed that attaches to sorghum roots and stunts the crop even on good soil."),
 ("mcq_crp_0004","crops","maize / variety","en","advanced","verify: IITA variety guide + ADP advisory",
  "In Kaduna the rains started two weeks late but are expected to be adequate overall. What is the soundest maize choice?",
  ["Plant an early-maturing variety","Plant a full-season variety as usual","Plant on the first light shower","Abandon maize for the whole year"],
  "A late start shortens the effective season, so an early-maturing variety matures in time. Full-season risks not finishing; planting on one shower or abandoning are poor calls."),
 ("mcq_lvk_0001","livestock","poultry / brooding","en","basic","verify: poultry husbandry manual",
  "What is the recommended brooder temperature near day-old chicks during the first week?",
  ["About 32-35 C","About 20-22 C","About 26-28 C","About 40-42 C"],
  "Week-one brooding temperature at chick level is about 32-35 C, reduced ~3 C per week. Lower is too cold; 40-42 C is too hot."),
 ("mcq_lvk_0002","livestock","poultry / brooding","en","basic","verify: poultry husbandry manual",
  "Chicks are huddling tightly directly under the heat source. What does this most likely mean?",
  ["They are too cold","They are too hot","The temperature is correct","They are hungry"],
  "Huddling under the heat means too cold; scattering to the edges and panting means too hot; even spreading means correct."),
 ("mcq_lvk_0003","livestock","poultry / feeding","en","intermediate","verify: broiler feeding guide",
  "What is the correct broiler feed sequence from day-old to market?",
  ["Starter, then grower, then finisher","Finisher, then grower, then starter","Layer mash from start to finish","Grower feed from start to finish"],
  "Broilers go starter (high protein, early) -> grower -> finisher (weight gain before market). The others mis-stage or use the wrong feed."),
 ("mcq_lvk_0004","livestock","poultry / biosecurity","ha","intermediate","verify: poultry biosecurity guide",
  "Yaya ya kamata ka yi da sabbin kaji da ka saya kafin ka hada su da garken?",
  ["Ka raba su na mako biyu kafin ka hada su","Ka hada su nan da nan da sauran kajin","Ka hada su a daren farko kawai","Babu bukatar wani kariya ko kadan"],
  "New birds should be quarantined ~2 weeks before mixing, to avoid importing disease into the flock. Immediate mixing defeats the purpose."),
 ("mcq_lvh_0001","livestock_health","poultry / Newcastle","en","basic","verify: veterinary poultry-disease manual",
  "Several chickens die suddenly; others show greenish diarrhoea and a twisted neck. Which disease is most likely?",
  ["Newcastle disease","Coccidiosis","Gumboro (IBD)","Fowl pox"],
  "Sudden death + greenish diarrhoea + nervous signs (twisted neck) is classic Newcastle. Coccidiosis = bloody droppings; Gumboro = whitish diarrhoea; fowl pox = skin lesions."),
 ("mcq_lvh_0002","livestock_health","poultry / coccidiosis","en","intermediate","verify: veterinary poultry-disease manual",
  "Young birds on damp litter are droopy with ruffled feathers and bloody droppings. What is the most likely cause?",
  ["Coccidiosis","Newcastle disease","Gumboro (IBD)","Intestinal worm infestation"],
  "Bloody droppings in young birds on wet litter point to coccidiosis (an Eimeria parasite). Newcastle/Gumboro have different signs; worms rarely cause frank blood like this."),
 ("mcq_lvh_0003","livestock_health","poultry / Gumboro","en","intermediate","verify: veterinary poultry-disease manual",
  "Birds around 4 weeks old show whitish watery diarrhoea, vent pecking and trembling, and the disease attacks their immune (bursal) organ. Which is it?",
  ["Gumboro (IBD)","Newcastle disease","Fowl cholera","Coccidiosis"],
  "Whitish watery diarrhoea, vent pecking and trembling in ~3-6 week birds attacking the bursa is Gumboro (infectious bursal disease)."),
 ("mcq_lvh_0004","livestock_health","poultry / Newcastle","ha","basic","verify: veterinary poultry-disease manual",
  "Mene ne kariya mafi muhimmanci daga cutar Newcastle a kaji?",
  ["Allurar rigakafi tare da biosecurity","Maganin antibiotic don warkar da ita","Ware kaji kawai ba tare da rigakafi","Babu wani abu da za a iya yi"],
  "Newcastle has no cure once it strikes; prevention is vaccination plus biosecurity. Antibiotics don't cure a virus; isolation alone is insufficient."),
 ("mcq_wea_0001","weather","planting / timing","en","basic","verify: NAERLS planting calendar",
  "When is it safest to plant maize at the start of the rainy season?",
  ["After two or three steady rains","On the very first single rain","Before any rain, in the dry season","Only after the rains have ended"],
  "Waiting for a stable onset (2-3 good rains) lets the soil hold moisture and avoids seedlings dying in an early dry spell. The others are mistimed or out of season."),
 ("mcq_wea_0002","weather","flooding / management","en","basic","verify: extension water-management note",
  "A field is prone to waterlogging during heavy rains. Which practice best protects the crop?",
  ["Make ridges and provide drainage channels","Add more water to balance the soil","Compact the soil so water sits on top","Remove all the topsoil from the field"],
  "Ridging and drainage move excess water away from roots. Adding water, compacting, or stripping topsoil all worsen waterlogging."),
 ("mcq_wea_0003","weather","heat stress / poultry","en","intermediate","verify: poultry husbandry manual",
  "During intense heat, chickens are panting with open beaks. What is the best immediate action?",
  ["Give shade, ventilation and cool water","Add more heat inside the poultry house","Reduce the amount of drinking water","Close all the ventilation openings"],
  "Open-beak panting is heat stress; provide shade, ventilation and cool water. Adding heat, cutting water, or blocking airflow make it worse."),
 ("mcq_wea_0004","weather","drought / adaptation","en","advanced","verify: IITA variety guide",
  "Rains have started late and are expected to be short this season. Which maize strategy best secures a harvest?",
  ["Choose an early-maturing variety","Plant a full-season variety as usual","Delay planting several more weeks","Plant the seed much deeper than normal"],
  "An early-maturing variety (~90 days) finishes before the rains cut off. Full-season may not mature; deeper planting and further delay don't fix a short season."),
 ("mcq_fop_0001","farm_operations","storage / grain","en","basic","verify: extension PICS storage guide",
  "What is the most reliable low-cost way to protect stored maize grain from weevils?",
  ["Dry it well and seal it in hermetic (PICS) bags","Store it loosely in an open basket","Keep it in a loosely tied ordinary sack","Sprinkle water on it to keep it cool"],
  "Drying to ~12-13% moisture then hermetic (PICS) storage starves weevils of oxygen, no chemicals needed. Airflow, moisture and loose sacks all let weevils thrive."),
 ("mcq_fop_0002","farm_operations","harvest / rice","ha","basic","verify: Africa Rice post-harvest guide",
  "Yaushe ne lokaci mafi kyau na girbin shinkafa?",
  ["Lokacin da kusan kashi 80 na hatsi suka yi rawaya da tauri","Lokacin da ganye har yanzu suke kore sosai","Lokacin da hatsi suke da madara har yanzu","Nan da nan bayan shinkafa ta yi fure"],
  "Rice is ready when ~80% of grains are golden and hard. Green leaves, milky grains, and just-after-flowering all mean it is immature."),
 ("mcq_fop_0003","farm_operations","seed / germination test","en","intermediate","verify: extension seed-testing guidance",
  "Before planting a whole field, a farmer tests 100 saved maize seeds and 75 sprout. What is the best action?",
  ["Plant slightly more thickly to compensate","Plant at the normal rate, no change","Discard all the seed as useless","Soak the seed in fertilizer first"],
  "A ~75% germination rate is usable but reduced, so plant slightly thicker to compensate; below ~70% you'd replace the seed. Normal rate risks a thin stand."),
 ("mcq_fop_0004","farm_operations","feed / dry-season ration","en","advanced","verify: dry-season feeding guide",
  "To feed ruminants through the dry season when grass is scarce, which conserved residue gives the most protein?",
  ["Groundnut and cowpea haulms","Dry maize cob residue","Threshed rice straw","Cereal husk chaff"],
  "Legume haulms (groundnut, cowpea) are protein-rich and the best dry-season residue. Cob residue, rice straw and chaff are bulky but low in protein."),
]

def main():
    out = Path(__file__).resolve().parent / "mcq_batch1_reviewed.jsonl"
    pos = {l: 0 for l in LBL}
    with out.open("w", encoding="utf-8") as f:
        for idx, (id_, cat, subj, lang, diff, src, q, opts, expl) in enumerate(M):
            assert len(opts) == 4 and len(set(opts)) == 4, id_
            target = idx % 4                      # balanced: A/B/C/D each exactly 5
            correct = opts[0]
            rest = opts[1:]
            ordered = []
            di = 0
            for p in range(4):
                if p == target:
                    ordered.append(correct)
                else:
                    ordered.append(rest[di]); di += 1
            rec = {
                "id": id_, "category": cat, "subject": subj, "language": lang,
                "difficulty": diff, "question": q,
                "options": {LBL[i]: ordered[i] for i in range(4)},
                "correct_answer": LBL[target], "explanation": expl, "source_reference": src,
                "needs_source_check": True, "hausa_reviewed": (lang != "ha"),
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            pos[LBL[target]] += 1
    print(f"wrote {len(M)} reviewed MCQs -> {out}")
    print("answer-position balance: " + ", ".join(f"{k}={v}" for k, v in pos.items()))

if __name__ == "__main__":
    main()
