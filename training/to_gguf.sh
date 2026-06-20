#!/usr/bin/env bash
# Convert a merged fp16 HF model directory to GGUF and quantize to Q4_K_M (+ Q5_K_M).
#
# Usage:
#   bash training/to_gguf.sh out/agri-advisor-1.5b/merged-fp16
#
# Produces:
#   model/agri-advisor-qwen2.5-1.5b-f16.gguf       (intermediate, full precision)
#   model/agri-advisor-qwen2.5-1.5b-Q4_K_M.gguf    (primary submission candidate)
#   model/agri-advisor-qwen2.5-1.5b-Q5_K_M.gguf    (fallback if Q4 accuracy drops)
#
# Requires llama.cpp checked out and built (see commands below if you don't have it).

set -euo pipefail

MERGED_DIR="${1:?usage: to_gguf.sh <merged-fp16-dir>}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$HERE/model"
NAME="agri-advisor-qwen2.5-1.5b"
LLAMA_DIR="${LLAMA_CPP_DIR:-$HOME/llama.cpp}"

mkdir -p "$OUT_DIR"

# ── One-time llama.cpp setup (uncomment if you have not built it yet) ──────────
# git clone https://github.com/ggerganov/llama.cpp "$LLAMA_DIR"
# cmake -B "$LLAMA_DIR/build" "$LLAMA_DIR" && cmake --build "$LLAMA_DIR/build" -j
# pip install -r "$LLAMA_DIR/requirements.txt"
# ──────────────────────────────────────────────────────────────────────────────

F16="$OUT_DIR/${NAME}-f16.gguf"
Q4="$OUT_DIR/${NAME}-Q4_K_M.gguf"
Q5="$OUT_DIR/${NAME}-Q5_K_M.gguf"

echo "[1/3] converting merged fp16 → GGUF f16…"
python "$LLAMA_DIR/convert_hf_to_gguf.py" "$MERGED_DIR" \
  --outfile "$F16" --outtype f16

QUANT_BIN="$LLAMA_DIR/build/bin/llama-quantize"
[[ -x "$QUANT_BIN" ]] || QUANT_BIN="$LLAMA_DIR/llama-quantize"

echo "[2/3] quantizing → Q4_K_M (primary)…"
"$QUANT_BIN" "$F16" "$Q4" Q4_K_M

echo "[3/3] quantizing → Q5_K_M (fallback)…"
"$QUANT_BIN" "$F16" "$Q5" Q5_K_M

echo
echo "done. quantized models:"
ls -lh "$Q4" "$Q5"
echo
echo "next steps:"
echo "  1. smoke test:  $LLAMA_DIR/build/bin/llama-cli -m \"$Q4\" -p \"Test: best planting window for maize in Kaduna?\" -n 128"
echo "  2. profile:     bash profiling/run_profiler.sh"
echo "  3. upload the chosen .gguf to a PUBLIC Hugging Face repo and update download_model.sh"
