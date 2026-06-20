#!/usr/bin/env python3
"""
Dataset generator v2 — scales the gold core toward 100+ against DATASET_SPEC.md v0.1.

Supersedes expand_dataset.py. Emits the FULL authoring schema (meta incl. difficulty,
source_reference, location, sv, reasoning_pattern) so output merges with gold_batch1.jsonl.

Batch 1 mode (default) restricts to the format-stable subjects only:
  crops: maize, rice, sorghum   |   poultry husbandry   |   livestock health: Newcastle, coccidiosis, Gumboro

Setup:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python training/data/expand_dataset_v2.py --target 70 --out training/data/gold_generated.jsonl

Then REVIEW every row (facts + Hausa), dedup against gold_batch1.jsonl, and concatenate:
    cat training/data/gold_batch1.jsonl training/data/gold_generated.jsonl > training/data/gold_authoring.jsonl
    jq -c '{messages: .messages}' training/data/gold_authoring.jsonl > training/data/agri_train.jsonl

Generated rows are DRAFTS: needs_source_check=true, hausa_reviewed=false. Verify before training.
"""
from __future__ import annotations
import argparse, json, os, random, sys
from pathlib import Path

SYS_TRAIN = ("You are FarmHealth AI, an offline agricultural and livestock-health advisor for "
             "farmers and extension officers in northern Nigeria. Give practical, region-appropriate "
             "advice. Answer in the language the user used.")

# subject -> (category, source_reference, default_sv)
BATCH1_SUBJECTS = {
    "maize":       ("crops", "verify: IITA maize agronomy guide", "S"),
    "rice":        ("crops", "verify: Africa Rice production guide", "S"),
    "sorghum":     ("crops", "verify: ICRISAT sorghum agronomy guide", "S"),
    "poultry husbandry": ("livestock", "verify: poultry husbandry/extension manual", "S"),
    "Newcastle disease": ("livestock_health", "verify: veterinary poultry-disease manual", "S"),
    "coccidiosis": ("livestock_health", "verify: veterinary poultry-disease manual", "S"),
    "Gumboro disease": ("livestock_health", "verify: veterinary poultry-disease manual", "S"),
}

ARCHETYPE_PATTERN = {
    "diagnostic": "observe_diagnose_explain_act",
    "how_to": "goal_steps_caution_check",
    "timing": "condition_window_caveat",
    "quantitative": "figure_apply_caveat",
    "comparison": "options_tradeoffs_reco",
    "safety_correction": "acknowledge_risk_correct_safe",
}
# market_decision intentionally excluded from Batch 1 (volatile / format-dependent)

DIFF_WEIGHTS = [("basic", 0.50), ("intermediate", 0.35), ("advanced", 0.15)]

TEACHER_SYS = """You write supervised fine-tuning examples for FarmHealth AI, an offline \
agricultural & livestock-health advisor for smallholder farmers and extension officers in \
northern Nigeria (Nasarawa, Kaduna, Adamawa, Kwali).

Hard rules:
- Agronomy/veterinary content must be correct, mainstream and conservative.
- NEVER give drug names or dosages or exact agrochemical rates. Name the IPM/biosecurity/management \
approach and say to follow the product label / consult a vet or extension officer.
- For disease questions: focus on signs, prevention, biosecurity, and when to consult a vet.
- Match the ANSWER STRUCTURE to the archetype you are given.
- Keep answers practical, 3-7 sentences, no markdown, no preamble.
- Write the requested language (Hausa = natural Hausa; a human will review).

Answer skeletons by archetype:
  diagnostic       -> observation restated -> likely cause(s) -> why -> immediate action -> prevention -> when to escalate
  how_to           -> goal -> ordered steps -> key cautions -> how to know it worked
  timing           -> trigger condition -> recommended window -> what to avoid -> fallback if late/early
  quantitative     -> conservative figure -> how to apply -> verify-with-label/local caveat -> why timing matters
  comparison       -> options -> trade-offs of each -> recommendation tied to the stated condition
  safety_correction-> acknowledge intent -> why it's risky -> correct approach -> safe practice/PPE

Output ONLY a JSON array of objects {"user": "...", "assistant": "..."}. No other text."""

def build_prompt(subject, archetype, difficulty, lang, n):
    lang_name = "Hausa" if lang == "ha" else "English"
    return (f"Generate {n} distinct {difficulty}-difficulty {archetype} question-answer pairs in "
            f"{lang_name} about {subject} for the northern Nigerian smallholder context. Vary the "
            f"specifics (state, growth stage/age, symptom, season). Follow the {archetype} skeleton. "
            f"Return only the JSON array.")

def pick_difficulty():
    r, acc = random.random(), 0.0
    for d, w in DIFF_WEIGHTS:
        acc += w
        if r <= acc:
            return d
    return "basic"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="training/data/gold_generated.jsonl")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--target", type=int, default=70, help="approx number of examples to generate")
    ap.add_argument("--per-call", type=int, default=3)
    args = ap.parse_args()

    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY")
    client = anthropic.Anthropic()

    subjects = list(BATCH1_SUBJECTS.items())
    archetypes = list(ARCHETYPE_PATTERN.items())
    seen, written = set(), 0
    out_path = Path(args.out); out_path.parent.mkdir(parents=True, exist_ok=True)
    counters = {"id": 0}

    with out_path.open("w", encoding="utf-8") as f:
        while written < args.target:
            subject, (category, src, sv) = random.choice(subjects)
            archetype, pattern = random.choice(archetypes)
            difficulty = pick_difficulty()
            lang = "ha" if random.random() < 0.40 else "en"   # ~40% HA
            try:
                resp = client.messages.create(
                    model=args.model, max_tokens=1600, system=TEACHER_SYS,
                    messages=[{"role": "user",
                               "content": build_prompt(subject, archetype, difficulty, lang, args.per_call)}],
                )
                text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
                text = text.replace("```json", "").replace("```", "").strip()
                pairs = json.loads(text)
            except Exception as e:  # noqa: BLE001
                print(f"  ! {subject}/{archetype}: {e}")
                continue
            for p in pairs:
                u, a = p.get("user", "").strip(), p.get("assistant", "").strip()
                if not (u and a) or u[:80].lower() in seen:
                    continue
                seen.add(u[:80].lower())
                counters["id"] += 1
                rec = {
                    "messages": [
                        {"role": "system", "content": SYS_TRAIN},
                        {"role": "user", "content": u},
                        {"role": "assistant", "content": a},
                    ],
                    "meta": {
                        "id": f"gen_{category[:3]}_{counters['id']:04d}",
                        "category": category, "subject": subject, "lang": lang,
                        "archetype": archetype, "reasoning_pattern": pattern, "sv": sv,
                        "difficulty": difficulty, "location": None, "source_reference": src,
                        "needs_source_check": True,
                        "hausa_reviewed": False if lang == "ha" else True,
                    },
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                written += 1
            print(f"[{written}/{args.target}] {subject} | {archetype} | {difficulty} | {lang}")
    print(f"\nwrote {written} generated drafts -> {out_path}")
    print("NEXT: review facts + Hausa, dedup against gold_batch1.jsonl, then concat into gold_authoring.jsonl")

if __name__ == "__main__":
    main()
