#!/usr/bin/env python3
"""
Batch 1 gold dataset — format-stable categories only (safe to author pre-organizer-reply):
crops (maize/rice/sorghum), poultry husbandry, livestock health (Newcastle/coccidiosis/Gumboro).

All records are sv="S" (stable knowledge -> fine-tuning). Authored to DATASET_SPEC.md v0.1.

Run:  python training/data/build_gold_batch1.py
Out:  training/data/gold_batch1.jsonl   (authoring format, with meta)

STATUS OF THIS DATA:
  - needs_source_check=true on every row  -> verify agronomy/vet facts against the named source
  - hausa_reviewed=false on every HA row   -> a fluent speaker must review before training
  - no drug/agrochemical dosages           -> deferred to label / vet / extension officer
These are competition-grade DRAFTS, not verified ground truth.
"""
import json
from pathlib import Path

SYS = ("You are FarmHealth AI, an offline agricultural and livestock-health advisor for "
       "farmers and extension officers in northern Nigeria. Give practical, region-appropriate "
       "advice. Answer in the language the user used.")

# (id, category, subject, lang, archetype, pattern, difficulty, location, source_ref, user, assistant)
R = [
 # ── MAIZE ───────────────────────────────────────────────────────────────────
 ("crp_mze_0001","crops","maize / nutrient","en","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: IITA maize agronomy guide",
  "The lower leaves of my maize are turning yellow from the tip inward in a V-shape. What is wrong?",
  "Yellowing that starts at the tip of the oldest (lower) leaves and moves inward in a V is the classic sign of nitrogen deficiency. Maize pulls nitrogen from old leaves to feed new growth, so the bottom shows it first. On sandy soil or after heavy rain it is usually leaching — the rain has washed nitrogen below the young roots. Side-dress with a nitrogen fertilizer banded beside the row, not touching the stem, and split the dose if you can so the next rains do not wash it all away. If only scattered plants are affected in a blotchy pattern, check for waterlogging instead."),
 ("crp_mze_0002","crops","maize / planting","ha","how_to","goal_steps_caution_check","basic",None,
  "verify: NAERLS maize extension bulletin",
  "Yaya zan shuka masara da tazara madaidaiciya?",
  "Manufar ita ce a ba kowace tsiro sarari da abinci da ya isa. Yi layuka da tazara kusan santimita 75 tsakaninsu, sannan tazara kusan santimita 25 tsakanin tsiro a cikin layi. Ka sa kwaya daya zuwa biyu a kowace rami, zurfin kusan santimita 3 zuwa 5. Ka tabbatar kasa tana da danshi lokacin shuka. Idan ka shuka kusa-kusa fiye da haka, tsiro za su yi gasa kan abinci da ruwa su yi rauni; idan ka yi nisa sosai kuma za ka rasa yawan amfani."),
 ("crp_mze_0003","crops","maize / diagnosis","en","comparison","options_tradeoffs_reco","intermediate",None,
  "verify: IITA maize agronomy guide",
  "How can I tell the difference between nitrogen deficiency and drought stress in my maize?",
  "They look similar at a glance but differ in pattern. Nitrogen deficiency shows as yellowing on the OLDEST lower leaves first, in a V from the tip, while the plant stays otherwise upright. Drought stress shows as leaf rolling or curling (often worst in the heat of the day), greyish-green colour, and wilting across the WHOLE plant including new growth, not just the bottom. Check the soil: dry and cracked points to drought; moist soil with yellow lower leaves points to nitrogen. If the leaves perk back up in the cool of evening, it is water; if they stay yellow, it is nutrition."),
 ("crp_mze_0004","crops","maize / pest","en","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: FAO fall armyworm IPM guide",
  "My young maize has ragged holes and 'windowpane' patches on new leaves with moist sawdust in the whorl. What is it?",
  "That is fall armyworm — the windowpane feeding and the wet sawdust-like frass packed into the whorl are the giveaways. Scout twice a week and crush egg masses (felt-like patches under leaves) and small larvae by hand. For small plots, dropping a pinch of dry sand or wood ash into the infested whorl is a cheap, effective control. Avoid blanket spraying, which kills the natural enemies that help you. Only if many plants are heavily attacked should you use an insecticide recommended for fall armyworm, applied into the whorl in the evening, strictly at the label rate. Early planting helps the crop escape the worst pressure."),
 ("crp_mze_0005","crops","maize / planting","ha","timing","condition_window_caveat","intermediate",
  {"state":"Kaduna","lga":None,"season":"early_rains"},
  "verify: NAERLS planting calendar (Kaduna)",
  "Yaushe ne lokaci mafi kyau na shuka masara a Kaduna?",
  "Ka shuka lokacin da ruwan sama ya tabbata da kyau — yawanci karshen Mayu zuwa Yuni a Kaduna — bayan ka samu ruwa mai kyau sau biyu ko uku a jere domin kasa ta rike danshi. Ka yi niyyar shuka iri mai cikakken lokaci a cikin makonni biyu na farkon tabbatar ruwan. Kar ka shuka a kan ruwa daya kawai, domin idan rana ta dawo tsiron zai bushe. Idan ruwan ya yi jinkiri ko ya yi karanci, sai ka koma iri mai saurin nuna (kusan kwana 90) don ka tabbatar da girbi."),
 ("crp_mze_0006","crops","maize / variety","en","comparison","situation_factors_rule_reco","advanced",
  {"state":"Kaduna","lga":None,"season":"early_rains"},
  "verify: IITA variety guide + state ADP advisory",
  "Rains started two weeks late in Kaduna this year. Should I switch from maize to sorghum, and why?",
  "Not necessarily switch crops — first switch the maize VARIETY. A two-week-late start mostly shortens your season, so move from a full-season maize to an early or extra-early maize (around 90 days) so it matures before the rains cut off. Sorghum becomes the better choice only if your rains are also likely to be SHORT and unreliable, not just late, because sorghum tolerates dry spells and poorer soils better than maize and doubles as fodder. Decision rule: late-but-adequate rains → early-maturing maize; late AND short/erratic → lean sorghum (or split your land between both to spread the risk). Either way, don't plant on the first single rain — wait for a stable onset so you don't replant."),
 ("crp_mze_0007","crops","maize / storage","en","how_to","goal_steps_caution_check","basic",None,
  "verify: extension post-harvest / PICS guide",
  "How do I store my maize so weevils don't destroy it?",
  "The goal is to dry it hard and cut off the weevils' air. First sun-dry the grain well, to about 12–13% moisture — it should crack rather than dent when bitten. Then store it in triple-layer hermetic (PICS) bags, tying each inner liner and the outer bag tightly so no air gets in; this suffocates any weevils inside within a couple of weeks and keeps the grain for months with no chemicals. Keep the bags off the floor and out of the rain. You'll know it worked when the grain stays clean and hard with no fresh powder or live weevils after a few weeks."),
 ("crp_mze_0008","crops","maize / nutrient","ha","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: IITA maize agronomy guide",
  "Ganyen masara ta na juya launin shunayya (purple). Mene ne dalili?",
  "Launin shunayya a ganyen masara yawanci yana nuna karancin phosphorus, musamman a tsiro masu kankanta. Sau da yawa yana faruwa ne saboda kasa mai sanyi ko danshi sosai a farkon girma, wanda ke hana saiwa daukar phosphorus ko da yana cikin kasa. Idan yanayi ya yi dumi kuma kasa ta sami iska, sau da yawa tsiron yana warkewa da kansa. Idan ya ci gaba, yana nufin kasa na bukatar phosphorus — yi amfani da taki mai dauke da phosphorus lokacin shuka a shekara mai zuwa, kuma ka duba lafiyar kasa."),
 # ── RICE ────────────────────────────────────────────────────────────────────
 ("crp_ric_0001","crops","rice / disease","ha","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: FAO/Africa Rice blast factsheet",
  "Shinkafa ta na da raunuka masu siffar lu'u-lu'u (diamond) a ganye. Mene ne?",
  "Wannan alama ce ta cutar 'rice blast' (kunar shinkafa) — raunin yana da siffar lu'u-lu'u mai tsakiya toka da gefe ruwan kasa. Hanyoyin magancewa: yi amfani da iri masu juriya da iri da aka tabbatar (certified seed); kar ka zuba nitrogen fiye da kima domin yana kara cutar; ka bar sarari tsakanin tsiro don iska ta shiga ta rage danshi a ganye. Idan cutar ta yi yawa, yi amfani da fungicide da aka ba da shawara bisa ka'idar lakabin kawai, kuma ka tuntubi jami'in koyar da noma."),
 ("crp_ric_0002","crops","rice / transplanting","en","how_to","goal_steps_caution_check","intermediate",None,
  "verify: Africa Rice lowland production guide",
  "When and how should I transplant my lowland rice seedlings?",
  "Transplant when the seedlings are about 3 to 4 weeks old with 4 to 5 leaves — young, vigorous seedlings establish faster than old ones. Level your puddled field and keep a thin film of water, not a deep flood, at transplanting. Plant 2 to 3 seedlings per hill in rows (around 20 cm spacing) so you can weed and so air moves through the crop. Transplant in the cooler part of the day to reduce shock. Keep the water shallow for the first week while roots take hold, then manage levels as the crop grows; the field should be settled and weed-free, and seedlings standing upright within a few days."),
 ("crp_ric_0003","crops","rice / harvest","en","timing","condition_window_caveat","basic",None,
  "verify: Africa Rice post-harvest guide",
  "How do I know when my rice is ready to harvest?",
  "Harvest when about 80–85% of the grains in the panicle have turned golden-yellow and the grains in the middle of the panicle are firm and hard, not milky when pressed. The lower leaves yellowing and panicles bending over are good supporting signs. Don't wait until everything is bone-dry on the stalk — over-waiting causes shattering and grain loss to birds. If you harvest too early, you'll get many immature, chalky grains. After cutting, dry the grain properly before storage to avoid moulding."),
 ("crp_ric_0004","crops","rice / nutrient","en","diagnostic","observe_diagnose_explain_act","intermediate",None,
  "verify: Africa Rice nutrient guide",
  "My rice is stunted and the older leaves are yellowing evenly. What might be the cause?",
  "Even yellowing that begins on the older, lower leaves together with stunting most often points to nitrogen deficiency, which is very common in lowland rice on poor soils. Confirm by checking the pattern: nitrogen shows first on old leaves and the whole plant looks pale and small. If instead the YOUNGEST leaves are yellow between the veins, that suggests a different nutrient (such as iron or sulphur) and you should have the soil or water checked. For nitrogen, apply a topdressing in split doses timed to the crop's growth stages rather than all at once, and keep water management even, since flooding swings affect nutrient uptake."),
 # ── SORGHUM ─────────────────────────────────────────────────────────────────
 ("crp_sor_0001","crops","sorghum / striga","ha","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: ICRISAT striga management guide",
  "Akwai ciyawa mai launin shunayya tana fitowa kusa da dawa ta, kuma dawar ta yi rauni. Mene ne?",
  "Wannan tana kama da striga (witchweed) — ciyawa mai launin shunayya da ke hada kanta da saiwar dawa tana shan abincinta, don haka dawar ta yi rauni ko da kasa ba ta da matsala a fili. Magance ta na bukatar hanyoyi da dama tare: cire striga da hannu kafin ta yi fure don kar ta yada iri; yi juyawar shuka da wake ko gyada; yi amfani da iri masu juriya idan akwai; ka kara wa kasa taki da kwayoyin halitta (manure) domin striga tana son talaucin kasa. Babu maganin gaggawa daya — sai dagewa na shekaru."),
 ("crp_sor_0002","crops","sorghum / planting","en","how_to","goal_steps_caution_check","basic",None,
  "verify: ICRISAT sorghum agronomy guide",
  "What spacing and seed rate should I use for sorghum?",
  "Aim to give each plant room without wasting land. Plant in rows about 75 cm apart with plants 20–25 cm apart within the row, dropping 2 to 3 seeds per hole about 3–5 cm deep, then thin to the strongest 1 to 2 plants once they establish. Treat the seed against smut before planting. For dual-purpose (grain plus fodder) you can plant slightly closer in the row. Keep the field weed-free for the first six weeks, which is when sorghum is most vulnerable to weed competition."),
 ("crp_sor_0003","crops","sorghum / disease","en","diagnostic","observe_diagnose_explain_act","intermediate",None,
  "verify: ICRISAT sorghum disease guide",
  "Some of my sorghum heads have grey-black galls instead of grain. What is it and how do I stop it next time?",
  "Those galls replacing grain are sorghum smut — a fungal disease carried mainly on the seed and in the soil. This season, remove and destroy the smutted heads (don't leave them in the field or compost them) so the spores don't spread and build up. For next season, the key prevention is to treat your seed with a recommended seed dressing before planting and to use clean, certified or smut-free seed. Rotating with a non-host crop and avoiding saving seed from an infected field also reduce the carry-over. Follow the seed-treatment product's label for handling and safety."),
 ("crp_sor_0004","crops","sorghum / harvest","en","timing","condition_window_caveat","basic",None,
  "verify: ICRISAT post-harvest guide",
  "When should I harvest my sorghum?",
  "Harvest when the grains are hard and have reached full colour for your variety, and a fingernail pressed into a grain no longer leaves a dent (the 'hard dough' to physiological-maturity stage). The leaves and stalk will be drying and the heads firm. Harvesting at the right time protects against bird damage and mould — sorghum left too long is heavily attacked by birds, while harvesting too early gives soft, immature grain that stores poorly. After cutting, dry the heads well before threshing and store the grain hermetically to keep weevils out."),
 # ── POULTRY HUSBANDRY ───────────────────────────────────────────────────────
 ("lvk_pol_0001","livestock","poultry / brooding","en","how_to","goal_steps_caution_check","basic",None,
  "verify: poultry husbandry / extension manual",
  "What temperature should my brooder be in the first week, and how do I know if it's right?",
  "In the first week the brooder floor area near the chicks should be about 32–35°C, then reduce it by roughly 3°C each week after. The chicks themselves are your best thermometer: if they huddle in a pile under the heat source, they are cold; if they scatter to the edges away from it and pant, they are too hot; if they spread out evenly and move around feeding normally, the temperature is right. Warm the brooder for several hours before the chicks arrive, keep it free of cold drafts, and provide clean warm water immediately. Check the chicks' behaviour through the day and adjust the heat accordingly."),
 ("lvk_pol_0002","livestock","poultry / feeding","ha","how_to","goal_steps_caution_check","basic",None,
  "verify: broiler feeding guide",
  "Wace irin abinci zan ba kajin nama (broilers) a kowane mataki?",
  "Ka ba su abinci a matakai, kuma kar ka canza kwatsam. Yi amfani da abinci na 'starter' (mai yawan furotin, kusan 22-23%) na kwanaki 10 zuwa 14 na farko don gina jiki da gabobi. Sannan ka koma 'grower' a tsakiyar lokaci, sa'an nan 'finisher' a mako daya ko biyu na karshe don kiba kafin kasuwa. Ka tabbatar suna da ruwa mai tsabta koyaushe — kaji na cin abinci kadan kuma su yi rashin girma idan ruwa ya yi karanci ko kazanta. Lokacin canza abinci daga mataki zuwa mataki, ka gauraya tsohon da sabon na kwana biyu zuwa uku don cikinsu ya saba."),
 ("lvk_pol_0003","livestock","poultry / biosecurity","en","how_to","goal_steps_caution_check","intermediate",None,
  "verify: poultry biosecurity guide",
  "What basic biosecurity should I practise on my small poultry farm?",
  "Biosecurity is about keeping disease out and contained, and it is cheaper than treating outbreaks. Limit who enters the pens, and have a dedicated pair of boots or a disinfectant foot-dip at the entrance so people don't carry disease in on their feet. Quarantine any newly bought birds for about two weeks before mixing them with your flock, and never bring in birds of unknown health status. Keep feed and water clean and protected from wild birds and rodents, clean and disinfect equipment regularly, and isolate any sick bird immediately. Dispose of dead birds properly rather than leaving them around. These simple routines block most common diseases."),
 ("lvk_pol_0004","livestock","poultry / vaccination","ha","timing","condition_window_caveat","intermediate",None,
  "verify: local veterinary vaccination schedule",
  "Wane jadawalin allurar rigakafi kajina ke bukata, kuma yaushe?",
  "Ka bi jadawalin da likitan dabbobi na yankinka ya tabbatar, amma yawanci ginshikin shi ne: Marek a ranar farko (yawanci a wurin kyankyashe), Newcastle (kamar Lasota) da infectious bronchitis a mako na farko da maimaitawa, Gumboro a mako na biyu da na uku, fowl pox kusan mako na 6 zuwa 8, sannan a maimaita Newcastle kafin da lokacin kwai. Newcastle ita ce babbar mai kisa, don haka a maimaita ta kowane 'yan watanni. Ka adana allurar a sanyi (cold chain) don kar ta lalace, kuma ka samo ainihin shekaru da magunguna daga likitan dabbobi domin jadawali na sauyawa daga wuri zuwa wuri."),
 ("lvk_pol_0005","livestock","poultry / chicks","ha","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: poultry husbandry manual",
  "Wasu 'yan kajina (chicks) suna da kashi a jikin duwawu (pasty vent). Mene ne dalili kuma me zan yi?",
  "Pasty vent (kashi da ke manne a duwawu) yawanci yana faruwa ne saboda matsalar zafi (sanyi ko zafi sosai a brooder), damuwa daga tafiya, ko ruwa/abinci mara kyau a kwanakin farko. Da hannu mai laushi da ruwan dumi, ka tsabtace duwawun a hankali don kar ya toshe. Ka gyara zafin brooder ya zama daidai (kusan 32-35°C a mako na farko), ka ba su ruwa mai tsabta da dumi, da abinci mai kyau na starter. Idan ya ci gaba a yawancin kajin, ka duba tsabta da zafi sosai, kuma ka tuntubi jami'in lafiyar dabbobi."),
 # ── NEWCASTLE ───────────────────────────────────────────────────────────────
 ("lvh_new_0001","livestock_health","poultry / Newcastle","en","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: veterinary poultry-disease manual",
  "Several of my chickens suddenly died, and others have greenish diarrhoea and a twisted neck. What is this?",
  "Sudden deaths together with greenish watery diarrhoea and nervous signs like a twisted neck (torticollis) or paralysis strongly suggest Newcastle disease, a fast-spreading viral disease that is the biggest killer of poultry in our area. There is no cure once birds are infected, so act on the rest of the flock now: isolate sick birds, stop all movement of birds, people and equipment between pens, and disinfect thoroughly. Do not sell or move birds, and dispose of dead ones properly. The protection going forward is strict Newcastle vaccination and biosecurity. Contact an animal-health officer quickly to confirm and to protect your remaining birds."),
 ("lvh_new_0002","livestock_health","poultry / Newcastle","ha","how_to","goal_steps_caution_check","basic",None,
  "verify: veterinary poultry-disease manual",
  "Yaya zan kare kajina daga cutar Newcastle?",
  "Newcastle cuta ce mai saurin kisa kuma babu maganinta da zarar ta kama, don haka rigakafi shi ne komai. Yi wa kajin allurar rigakafi: yi amfani da Lasota ko allurar I-2 (thermostable) musamman ga kajin gida, kuma ka maimaita bisa shawarar likitan dabbobi. Ka yi biosecurity: kar ka bar baki su shiga gidan kaji ba tare da kulawa ba, ka raba sabbin kaji na akalla mako biyu kafin ka hada su, kuma ka ware duk kaji mai rashin lafiya nan da nan. Ka tsaftace da disinfect kayan aiki akai-akai, ka adana allurar a sanyi don kar ta lalace."),
 ("lvh_new_0003","livestock_health","poultry / Newcastle","en","comparison","options_tradeoffs_reco","advanced",None,
  "verify: veterinary poultry-disease manual",
  "How do I tell Newcastle disease apart from infectious bronchitis or fowl cholera?",
  "These overlap and only a vet or lab can confirm, but the pattern helps. Newcastle often combines respiratory signs (gasping, coughing) WITH nervous signs (twisted neck, paralysis) and greenish diarrhoea, plus a sharp drop in egg production and high mortality. Infectious bronchitis is mainly respiratory with misshapen, soft-shelled eggs and usually milder mortality, and lacks the classic nervous signs. Fowl cholera (a bacterial disease) tends to strike suddenly with high fever, swollen wattles and dark combs, and often hits older birds, and unlike the viral diseases it can respond to treatment. Because they are managed differently, isolate the flock, send a sick or freshly dead bird for diagnosis, and treat the cause your vet confirms rather than guessing."),
 ("lvh_new_0004","livestock_health","poultry / Newcastle","ha","safety_correction","acknowledge_risk_correct_safe","intermediate",None,
  "verify: poultry biosecurity guide",
  "Kaji na suna mutuwa amma ina son in sayo sabbin kaji in kara yawan garken. Daidai ne?",
  "A'a, kar ka kawo sabbin kaji yanzu. Idan kana cikin barkewar cuta (kamar Newcastle), kawo sabbin kaji zai sa su kamu nan da nan kuma ka yada cutar, ka kuma yi asarar kudi biyu. Abin da ya kamata: ka fara warware abin da ke kashe kajin — ka ware masu rashin lafiya, ka tsaurara biosecurity, ka tuntubi likitan dabbobi don sanin cutar. Ka jira har sai barkewar ta kare gaba daya, ka tsabtace ka disinfect gidan kaji, sannan idan za ka kawo sabbi, ka fara raba su (quarantine) na akalla mako biyu kafin ka hada su da sauran. Kar ka taba kawo kaji yayin da garken ke rashin lafiya."),
 # ── COCCIDIOSIS ─────────────────────────────────────────────────────────────
 ("lvh_coc_0001","livestock_health","poultry / coccidiosis","en","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: veterinary poultry-disease manual",
  "My young birds are droopy with ruffled feathers and I see bloody droppings. What is it?",
  "Droopiness, ruffled feathers, huddling, reduced feeding and bloody or mucoid droppings in young birds point strongly to coccidiosis, a gut disease caused by Eimeria parasites. It thrives in damp, dirty litter and spreads through droppings, so it often flares after litter gets wet. Act on two fronts: fix the environment by removing wet litter and keeping it dry and clean with fresh water, and treat the birds with an anticoccidial as advised by your vet or the product instructions. Coccidiosis can kill quickly in heavy infections, so don't delay. Prevention is dry litter, clean feeders/drinkers, and where appropriate an anticoccidial in feed or a coccidiosis vaccine."),
 ("lvh_coc_0002","livestock_health","poultry / coccidiosis","ha","how_to","goal_steps_caution_check","intermediate",None,
  "verify: poultry husbandry manual",
  "Yaya zan hana cutar coccidiosis a kajina?",
  "Manufar ita ce a rage parasite (Eimeria) da ke bunkasa a cikin datti mai danshi. Ka kiyaye litter (shimfidar kasa) bushasshe kuma mai tsabta — ka cire wuraren da suka jika nan da nan, musamman kusa da masu ruwa. Kar ka cika gidan kaji da kaji fiye da kima, domin cunkoso na kara yaduwa. Ka ba su ruwa mai tsabta a cikin kwanonin da ba sa zubewa a kasa, ka wanke masu abinci da ruwa akai-akai. Inda ya dace, yi amfani da anticoccidial a cikin abinci ko allurar rigakafin coccidiosis bisa shawarar likitan dabbobi. Tsabta da bushewar litter su ne mafi muhimmancin kariya."),
 ("lvh_coc_0003","livestock_health","poultry / coccidiosis","en","comparison","options_tradeoffs_reco","intermediate",None,
  "verify: veterinary poultry-disease manual",
  "How do I tell coccidiosis from Newcastle disease in my flock?",
  "The clearest clues are the droppings, the age, and the signs. Coccidiosis usually hits younger birds on damp litter with bloody or mucoid droppings, droopiness and pale combs, but no nervous signs — it's a gut problem. Newcastle hits any age, spreads explosively with high sudden mortality, and combines respiratory signs (gasping) and nervous signs (twisted neck, paralysis) with greenish diarrhoea. Coccidiosis is linked to wet, dirty litter; Newcastle is a contagious virus unrelated to litter. Because Newcastle is far more dangerous and has no cure, if you see nervous signs and rapid spread, isolate the flock and call a vet immediately rather than treating for coccidiosis."),
 # ── GUMBORO / IBD ───────────────────────────────────────────────────────────
 ("lvh_gum_0001","livestock_health","poultry / Gumboro","en","diagnostic","observe_diagnose_explain_act","basic",None,
  "verify: veterinary poultry-disease manual",
  "My 4-week-old birds are suddenly dull, with whitish watery diarrhoea, vent pecking and trembling. What could it be?",
  "In birds around 3 to 6 weeks old, sudden dullness with whitish watery diarrhoea, soiled vents (and vent pecking), trembling and prostration is a classic picture of Gumboro disease (infectious bursal disease), a viral disease that attacks the young bird's immune organ. There is no specific cure, so care is supportive: give clean water with electrolytes and vitamins, keep the birds warm and comfortable, and reduce stress. Critically, isolate the affected flock and tighten biosecurity, because the virus is very hardy and spreads easily and survives long in the environment. Because Gumboro also weakens immunity and opens the door to other infections, confirm with a vet and review your vaccination programme."),
 ("lvh_gum_0002","livestock_health","poultry / Gumboro","ha","how_to","goal_steps_caution_check","intermediate",None,
  "verify: veterinary poultry-disease manual",
  "Yaya zan kare kajina daga cutar Gumboro?",
  "Babu maganin Gumboro kai tsaye, don haka rigakafi da biosecurity su ne kariya. Yi wa kajin allurar rigakafin Gumboro bisa jadawalin da likitan dabbobi ya ba da shawara (yawanci a makonnin farko, sau fiye da daya), domin lokacin allurar yana da muhimmanci sosai. Ka tsaurara biosecurity: ka iyakance baki, ka yi amfani da foot-dip na disinfectant, ka raba sabbin kaji, kuma ka tsabtace ka disinfect gidan kaji sosai — kwayar Gumboro tana da karfi kuma tana dadewa a muhalli. Idan cuta ta kama, ka ba da tallafi (ruwa mai electrolytes da bitamin) ka rage damuwa, kuma ka tuntubi likitan dabbobi."),
 ("lvh_gum_0003","livestock_health","poultry / Gumboro","en","comparison","options_tradeoffs_reco","intermediate",None,
  "verify: veterinary poultry-disease manual",
  "How is Gumboro different from coccidiosis? Both hit my young birds.",
  "Both strike young birds but differ in cause, droppings and what they damage. Gumboro is a virus that attacks the immune system (the bursa), typically around 3 to 6 weeks, with whitish watery diarrhoea, trembling, vent pecking and sudden onset across the flock; it spreads bird-to-bird regardless of litter. Coccidiosis is a parasite of the gut tied to wet, dirty litter, with bloody or mucoid droppings and droopiness. Coccidiosis responds to anticoccidial treatment; Gumboro has no specific cure and is managed by vaccination, biosecurity and supportive care. So check the droppings (bloody → coccidiosis; whitish watery with nervous trembling → Gumboro) and the litter condition, and confirm with a vet because the responses are different."),
 ("lvh_gum_0004","livestock_health","poultry / Gumboro","en","diagnostic","observe_diagnose_explain_act","advanced",None,
  "verify: veterinary poultry-disease manual / vaccination guidance",
  "My flock was vaccinated against Gumboro but still showed Gumboro-like signs. What could explain that?",
  "A vaccinated flock still breaking with Gumboro usually comes down to timing or handling rather than the vaccine being useless. The commonest reason is maternal-antibody interference: chicks from immune hens carry antibodies that neutralise an early vaccine, so if the dose is given too early it doesn't take, and if given too late the chicks are exposed before protection builds — the vaccination window has to match the maternal-antibody decline. Other causes are a broken cold chain (vaccine inactivated by heat), poor administration or coverage, very heavy field-virus or hardy variant strains overwhelming immunity, or immunosuppression. The fix is to review the vaccination timing and programme with a vet, verify cold-chain and technique, and tighten biosecurity to lower the virus challenge. This is one to confirm with a veterinarian rather than self-diagnose."),
 ("crp_mze_0009","crops","maize / planting","en","how_to","goal_steps_caution_check","basic",None,
  "verify: extension seed-testing guidance",
  "How can I check if my saved maize seed will germinate well before I plant a whole field?",
  "Do a simple germination test about a week before planting. Count out 100 seeds at random from your lot, wrap them in a damp cloth or place them between moist layers, keep them warm and re-moisten as needed, and after 5 to 7 days count how many have sprouted. If 90 or more sprout, the seed is good; 70 to 89 means plant a bit more thickly to compensate; below 70, get fresh seed rather than risk a poor stand. Testing first saves you from replanting a whole field that was never going to come up well."),
 ("crp_sor_0005","crops","sorghum / pest","ha","how_to","goal_steps_caution_check","intermediate",None,
  "verify: ICRISAT bird-damage management note",
  "Tsuntsaye (kamar quelea) suna cin dawa ta lokacin da hatsi ya nuna. Me zan yi?",
  "Tsuntsaye kamar quelea na iya yin babbar barna lokacin da hatsin dawa ya fara nuna. Hanyoyin rage barna: ka yi amfani da iri masu nunawa a lokaci daya da makwabta domin a raba matsin tsuntsaye (idan kai kadai ka nuna, duk tsuntsaye za su zo wurinka); ka yi amfani da iri masu kai a kasa (compact/goose-neck) ko masu dandano mai daci da tsuntsaye ba sa so idan akwai; ka sa mutane su rika korar tsuntsaye da safe da yamma lokacin da suke ciyarwa; ka yi amfani da abubuwan tsoratarwa (scarecrows, ribbons). Babu hanya daya da ke warware komai — gauraya hanyoyi shi ne mafita."),
]

def main():
    out = Path(__file__).resolve().parent / "gold_batch1.jsonl"
    counts = {"lang": {}, "category": {}, "difficulty": {}}
    with out.open("w", encoding="utf-8") as f:
        for (id_, cat, subj, lang, arch, pat, diff, loc, src, user, asst) in R:
            rec = {
                "messages": [
                    {"role": "system", "content": SYS},
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": asst},
                ],
                "meta": {
                    "id": id_, "category": cat, "subject": subj, "lang": lang,
                    "archetype": arch, "reasoning_pattern": pat, "sv": "S",
                    "difficulty": diff, "location": loc, "source_reference": src,
                    "needs_source_check": True,
                    "hausa_reviewed": False if lang == "ha" else True,
                },
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            for k, v in (("lang", lang), ("category", cat), ("difficulty", diff)):
                counts[k][v] = counts[k].get(v, 0) + 1
    print(f"wrote {len(R)} examples -> {out}\n")
    for dim, c in counts.items():
        print(f"{dim}: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))

if __name__ == "__main__":
    main()
