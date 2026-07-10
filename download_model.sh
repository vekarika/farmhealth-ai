#!/usr/bin/env bash
# Downloads the fine-tuned, quantized agriculture-advisor GGUF to model/.
#
# Rules enforced by the ADTC evaluator:
#   - Idempotent (safe to re-run; skips if the file already exists).
#   - No credentials (the weight URL must be public).
#   - Output path must exactly match `_runtime.model_path` in metadata.json.
#
# AFTER you fine-tune + quantize + upload your GGUF to a PUBLIC Hugging Face repo,
# replace MODEL_URL below with the `resolve/main` direct link to the .gguf file.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_DIR="$HERE/model"
MODEL_FILE="$MODEL_DIR/farmhealth-ai-qwen2.5-1.5b-Q4_K_M.gguf"

# ── Replace with your PUBLIC Hugging Face direct download URL ──────────────────
MODEL_URL="https://huggingface.co/vekarika/farmhealth-ai-qwen2.5-1.5b-gguf/resolve/main/farmhealth-ai-qwen2.5-1.5b-Q4_K_M.gguf"
# ──────────────────────────────────────────────────────────────────────────────

mkdir -p "$MODEL_DIR"

if [[ -f "$MODEL_FILE" ]]; then
  echo "model already present at $MODEL_FILE — skipping download"
  exit 0
fi

echo "downloading $MODEL_URL → $MODEL_FILE …"

if command -v curl > /dev/null 2>&1; then
  curl -L --fail --progress-bar -o "$MODEL_FILE.partial" "$MODEL_URL"
elif command -v wget > /dev/null 2>&1; then
  wget --show-progress -O "$MODEL_FILE.partial" "$MODEL_URL"
else
  echo "error: neither curl nor wget found" >&2
  exit 1
fi

mv "$MODEL_FILE.partial" "$MODEL_FILE"
echo "done: $MODEL_FILE"
