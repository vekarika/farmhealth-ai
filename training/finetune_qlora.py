#!/usr/bin/env python3
"""
QLoRA fine-tune of a small base model on the bilingual (EN/HA) agriculture dataset.

Designed to run on a single modest GPU (Google Colab T4, or your ThinkPad T14 if it
has a usable GPU). For a 1.5B model with QLoRA this fits comfortably in ~8 GB VRAM.

Usage:
    pip install -U "transformers>=4.44" "trl>=0.9" "peft>=0.12" \
        "bitsandbytes>=0.43" "datasets>=2.20" accelerate
    python training/finetune_qlora.py \
        --base Qwen/Qwen2.5-1.5B-Instruct \
        --data training/data/agri_train.jsonl \
        --out  out/agri-advisor-1.5b

Swap --base Qwen/Qwen2.5-0.5B-Instruct to train the ultra-lean A/B candidate.

Output is a MERGED fp16 model directory ready for GGUF conversion (see to_gguf.sh).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig, PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from trl import SFTConfig, SFTTrainer


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="Qwen/Qwen2.5-1.5B-Instruct")
    p.add_argument("--data", default="training/data/agri_train.jsonl",
                   help="JSONL with a 'messages' field per row (chat format).")
    p.add_argument("--out", default="out/agri-advisor-1.5b")
    p.add_argument("--epochs", type=float, default=3.0)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--bsz", type=int, default=2)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--max-len", type=int, default=2048)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out = Path(args.out)
    adapter_dir = out / "adapter"
    merged_dir = out / "merged-fp16"
    out.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(args.base)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 4-bit base for memory-efficient training; we merge back to fp16 afterward.
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.base, quantization_config=bnb, device_map="auto",
        torch_dtype=torch.bfloat16,
    )

    peft_cfg = LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    )

    ds = load_dataset("json", data_files=args.data, split="train")

    def to_text(row):
        return {"text": tokenizer.apply_chat_template(
            row["messages"], tokenize=False, add_generation_prompt=False)}

    ds = ds.map(to_text, remove_columns=ds.column_names)

    sft_cfg = SFTConfig(
        output_dir=str(adapter_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.bsz,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=10,
        save_strategy="epoch",
        bf16=True,
        max_length=args.max_len,
        packing=True,
        dataset_text_field="text",
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model, args=sft_cfg,
        train_dataset=ds, processing_class=tokenizer,
        peft_config=peft_cfg,
    )
    trainer.train()
    trainer.save_model(str(adapter_dir))

    # ── Merge LoRA into the base and save fp16 for clean GGUF conversion ──────────
    print("merging adapter into base (fp16)…")
    del model
    torch.cuda.empty_cache()
    base = AutoModelForCausalLM.from_pretrained(
        args.base, torch_dtype=torch.float16, device_map="cpu")
    merged = PeftModel.from_pretrained(base, str(adapter_dir))
    merged = merged.merge_and_unload()
    merged.save_pretrained(str(merged_dir), safe_serialization=True)
    tokenizer.save_pretrained(str(merged_dir))
    print(f"done. merged fp16 model at: {merged_dir}")
    print("next: bash training/to_gguf.sh", merged_dir)


if __name__ == "__main__":
    main()
