#!/usr/bin/env python3
"""
Dev-time quality proxy for base/fine-tuned models.

Runs the held-out gold questions through a LOCALLY-served candidate model (Ollama) and grades
each answer 0-100 against the gold reference answer using an LLM judge (Anthropic API).

This is a DEVELOPMENT signal only — it is NOT the offline submission and NOT the official score.
The real S_acc comes from the organizers' hidden validation set. Use this to compare candidates.

Setup:
    # serve the candidate locally (offline inference):
    ollama serve &            # if not already running
    ollama pull qwen2.5:1.5b  # or your fine-tuned GGUF imported into ollama
    pip install anthropic requests
    export ANTHROPIC_API_KEY=sk-ant-...   # grader only; dev-time

Usage:
    python benchmarks/quality_eval.py --model qwen2.5:1.5b \
        --eval-file training/data/gold_eval_holdout.jsonl
"""
from __future__ import annotations
import argparse, json, sys
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

JUDGE_SYS = ("You grade an agricultural/livestock-health answer for farmers in northern Nigeria. "
             "Score 0-100 for correctness, practicality, and safety, using the reference as a guide "
             "(the candidate may be worded differently but still correct). Penalise wrong facts, "
             "unsafe advice, or specific drug/chemical dosages. Output ONLY an integer 0-100.")

def ask_local(model: str, question: str) -> str:
    r = requests.post(OLLAMA_URL, json={"model": model, "prompt": question, "stream": False}, timeout=180)
    r.raise_for_status()
    return r.json().get("response", "").strip()

def grade(client, question: str, reference: str, candidate: str) -> int:
    msg = (f"QUESTION:\n{question}\n\nREFERENCE ANSWER:\n{reference}\n\n"
           f"CANDIDATE ANSWER:\n{candidate}\n\nScore 0-100. Output only the integer.")
    resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=8,
                                  system=JUDGE_SYS, messages=[{"role": "user", "content": msg}])
    txt = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    digits = "".join(c for c in txt if c.isdigit())
    return max(0, min(100, int(digits))) if digits else 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="Ollama model name (the candidate to test)")
    ap.add_argument("--eval-file", default="training/data/gold_eval_holdout.jsonl")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    client = anthropic.Anthropic()

    rows = [json.loads(l) for l in open(args.eval_file, encoding="utf-8")]
    if args.limit:
        rows = rows[: args.limit]

    total, scored = 0, 0
    for i, r in enumerate(rows, 1):
        q = next(m["content"] for m in r["messages"] if m["role"] == "user")
        ref = next(m["content"] for m in r["messages"] if m["role"] == "assistant")
        try:
            cand = ask_local(args.model, q)
            s = grade(client, q, ref, cand)
        except Exception as e:  # noqa: BLE001
            print(f"  ! item {i}: {e}")
            continue
        total += s; scored += 1
        lang = r.get("meta", {}).get("lang", "?")
        print(f"[{i}/{len(rows)}] {lang} score={s}")
    if scored:
        print(f"\nMODEL {args.model}: mean quality = {total/scored:.1f} over {scored} items")
        print("→ put this number in the 'quality' column of benchmarks/results.csv")

if __name__ == "__main__":
    main()
