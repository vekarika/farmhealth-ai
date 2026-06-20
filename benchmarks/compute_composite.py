#!/usr/bin/env python3
"""
Convert benchmark numbers into an estimated ADTC composite score, so the data picks the model.

ADTC formula:  S_total = 0.50*S_acc + 0.30*S_perf + 0.20*S_eff - P_thermal
  S_perf = 100 * (TPS_act / TPS_max)        # TPS_max provisional reference = 15.0
  S_eff  = 100 * ((7 - peak_ram_gb) / 7)    # 7 GB budget; >7 = disqualified
  S_acc  = dev-time quality proxy (0-100) from quality_eval.py   # real S_acc = hidden validation set
  P_thermal = 10 if throttled/temp>85C else 0

Usage:
    python benchmarks/compute_composite.py benchmarks/results.csv

results.csv columns: model,peak_ram_gb,tps,quality,throttled
  throttled: 1 if thermal throttling/temperature>85C observed, else 0
"""
import csv, sys

TPS_REFERENCE = 15.0      # provisional (DevPost). Recompute vs best candidate too.
RAM_BUDGET_GB = 7.0
W_ACC, W_PERF, W_EFF = 0.50, 0.30, 0.20

def s_perf(tps, tps_max):
    return min(100.0, 100.0 * (tps / tps_max)) if tps_max > 0 else 0.0

def s_eff(ram):
    return max(0.0, 100.0 * ((RAM_BUDGET_GB - ram) / RAM_BUDGET_GB))

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "benchmarks/results.csv"
    # optional: estimated African Use Case bonus (0-10, judge-assessed additive points)
    bonus = 0.0
    for a in sys.argv[2:]:
        if a.startswith("--bonus="):
            bonus = max(0.0, min(10.0, float(a.split("=", 1)[1])))
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            if not r.get("model"):
                continue
            r["peak_ram_gb"] = float(r["peak_ram_gb"])
            r["tps"] = float(r["tps"])
            r["quality"] = float(r["quality"])
            r["throttled"] = int(r.get("throttled", 0) or 0)
            rows.append(r)
    if not rows:
        sys.exit("no rows in results.csv")

    tps_max_field = max(r["tps"] for r in rows)        # relative-to-best-candidate view

    print(f"{'model':<34} {'RAM':>5} {'TPS':>6} {'Qual':>5} {'Sperf*':>7} {'Seff':>6} "
          f"{'Stot(ref)':>9} {'Stot(rel)':>9} {'flags'}")
    print("-" * 104)
    ranked = []
    for r in rows:
        if r["peak_ram_gb"] > RAM_BUDGET_GB:
            print(f"{r['model']:<34} {r['peak_ram_gb']:>5.2f} {'--':>6} {'--':>5} "
                  f"{'--':>7} {'--':>6} {'DQ-OOM':>9} {'DQ-OOM':>9} OVER 7GB → disqualified")
            continue
        sp_ref = s_perf(r["tps"], TPS_REFERENCE)
        sp_rel = s_perf(r["tps"], tps_max_field)
        se = s_eff(r["peak_ram_gb"])
        pth = 10.0 if r["throttled"] else 0.0
        tot_ref = W_ACC*r["quality"] + W_PERF*sp_ref + W_EFF*se - pth + bonus
        tot_rel = W_ACC*r["quality"] + W_PERF*sp_rel + W_EFF*se - pth + bonus
        flags = "THROTTLED" if r["throttled"] else ""
        ranked.append((tot_rel, r["model"], tot_ref))
        print(f"{r['model']:<34} {r['peak_ram_gb']:>5.2f} {r['tps']:>6.1f} {r['quality']:>5.0f} "
              f"{sp_ref:>7.1f} {se:>6.1f} {tot_ref:>9.1f} {tot_rel:>9.1f} {flags}")

    print("\n* Sperf(ref) uses provisional TPS_max=15; Sperf(rel) uses best candidate. "
          "Real ranking is relative to the FASTEST team's TPS.")
    if ranked:
        ranked.sort(reverse=True)
        print(f"\nBest by Stot(rel): {ranked[0][1]}")
        print("Note: S_acc here is a DEV PROXY. Replace with validation-set accuracy once obtained.")
        print(f"African Use Case bonus applied: +{bonus:.0f} pts (additive, judge-assessed 0-10). "
              f"Pass --bonus=N to model it.")

if __name__ == "__main__":
    main()
