#!/usr/bin/env bash
# Quick base-model benchmark: TPS + peak RAM per candidate, on TARGET-CLASS hardware.
# Run on the EliteBook 840 G6 (your ADTC Standard Laptop stand-in), not a beefy dev box.
#
# This is the FAST screening pass. The adtc-profiler remains the authoritative final check
# (see profiling/run_profiler.sh) once you've picked a candidate.
#
# Prereqs: llama.cpp built (llama-bench + llama-cli), GGUF files downloaded into ./models_bench/
#
# Usage: edit the MODELS list to point at your local GGUF paths, then:
#   bash benchmarks/run_benchmark.sh

set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LLAMA_DIR="${LLAMA_CPP_DIR:-$HOME/llama.cpp}"
BENCH="$LLAMA_DIR/build/bin/llama-bench"
RESULTS="$HERE/benchmarks/results.csv"

# label:path/to/model.gguf  — edit these to your downloaded candidates
MODELS=(
  "qwen2.5-0.5b-q4km:$HERE/models_bench/qwen2.5-0.5b-instruct-q4_k_m.gguf"
  "qwen2.5-1.5b-q4km:$HERE/models_bench/qwen2.5-1.5b-instruct-q4_k_m.gguf"
  "qwen2.5-3b-q4km:$HERE/models_bench/qwen2.5-3b-instruct-q4_k_m.gguf"
)

echo "model,peak_ram_gb,tps,quality,throttled" > "$RESULTS"

for entry in "${MODELS[@]}"; do
  label="${entry%%:*}"; path="${entry#*:}"
  [[ -f "$path" ]] || { echo "skip $label (missing $path)"; continue; }
  echo "=== $label ==="

  # TPS: llama-bench reports tokens/sec for generation (tg). Grab the tg t/s value.
  tps="$("$BENCH" -m "$path" -p 0 -n 128 -r 3 2>/dev/null \
        | awk -F'|' '/tg/ {gsub(/ /,"",$NF); val=$(NF-1)} END{gsub(/ /,"",val); print val}')"
  tps="${tps:-0}"

  # Peak RAM: run a short generation under /usr/bin/time -v and read Maximum resident set size (KB)
  rss_kb="$(/usr/bin/time -v "$LLAMA_DIR/build/bin/llama-cli" -m "$path" \
            -p "Best planting window for maize in Kaduna?" -n 64 2>&1 \
            | awk '/Maximum resident set size/ {print $NF}')"
  ram_gb="$(awk "BEGIN{printf \"%.2f\", ${rss_kb:-0}/1024/1024}")"

  echo "  TPS=$tps  peakRAM=${ram_gb}GB"
  echo "$label,$ram_gb,$tps,,0" >> "$RESULTS"   # quality filled by quality_eval.py
done

echo
echo "wrote $RESULTS (quality column blank — fill via quality_eval.py, then:)"
echo "  python benchmarks/compute_composite.py $RESULTS"
echo
echo "NOTE: also monitor temperature with the adtc-profiler for the official thermal flag."
