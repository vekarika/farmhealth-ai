#!/usr/bin/env bash
# Run the official ADTC profiler in participant mode to get your local Gate-1 numbers.
# Run this ON YOUR TARGET-CLASS MACHINE (the EliteBook 840 G6 stand-in), not a beefy dev box,
# so the speed/memory/thermal numbers reflect something close to the judging hardware.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Install the profiler (once)
if ! command -v adtc-profiler >/dev/null 2>&1; then
  echo "installing adtc-profiler…"
  pip install "git+https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git"
  # For the real accuracy benchmark (lm-eval), also: pip install lm-eval
fi

# 2. Make sure the model is present
if ! ls "$HERE"/model/*.gguf >/dev/null 2>&1; then
  echo "no model found — running download_model.sh"
  bash "$HERE/download_model.sh"
fi

# 3. Fast smoke test (speed + memory + thermal; skips the heavy accuracy benchmark)
echo "→ smoke test (speed/memory/thermal)…"
adtc-profiler run \
  --submission "$HERE" \
  --mode participant \
  --output "$HERE/submission.json" \
  --skip-accuracy

echo
echo "key numbers (review submission.json for the rest):"
python - "$HERE/submission.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
mem = d.get("memory", {})
thr = d.get("throughput", {})
th  = d.get("cpu_thermal", {})
print(f"  peak RSS      : {mem.get('peak_rss_gb', mem.get('peak_rss_bytes'))}")
print(f"  throughput    : {thr.get('gen_tps', thr)}")
print(f"  thermal       : {th.get('throttled', th)}")
print(f"  measured_on   : {d.get('environment', {}).get('measured_on')}")
PY

echo
echo "Seff = 100 * ((7 - peak_RSS_GB) / 7)   ← keep peak RAM low to maximise this"
echo "When numbers look good, run WITHOUT --skip-accuracy (needs lm-eval) for the full picture."
