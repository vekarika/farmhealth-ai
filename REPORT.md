# Technical Report — Agri-Advisor: Offline Farming Intelligence for the Northern Nigerian Belt

**Team ID:** REPLACE_WITH_ADTF_TEAM_ID
**Domain:** agriculture
**Model:** agri-advisor-qwen2.5-1.5b-Q4_K_M
**Language scope:** English + Hausa (`en`, `ha`)

---

## Problem

Smallholder farmers and agricultural extension officers across the northern Nigerian
belt — Nasarawa, Kaduna, Adamawa, and Kwali — make time-critical decisions about
planting windows, pest and disease response, livestock husbandry, and when to sell
into local markets. The advice they need is well understood agronomically, but it is
locked behind intermittent power, unreliable mobile data, and cloud services priced
in dollars. A farmer diagnosing leaf yellowing in a maize field at the edge of network
coverage cannot wait for a fibre connection or pay per API call.

Agri-Advisor is a language model that runs entirely on an 8 GB laptop — the machine an
extension officer or cooperative already owns — with **zero connectivity required at
inference time**. It answers crop, livestock, weather-timing, and market questions in
**English or Hausa**, putting agronomic decision support directly in the hands of the
people making the decision, in the language they speak.

**Target user:** agricultural extension officers, cooperative leads, and literate
smallholder farmers in northern Nigeria operating offline or on costly intermittent data.

---

## Design Decisions

### Why a fine-tuned small model rather than a large general model

The ADTC scoring formula (`S = 0.50·S_acc + 0.30·S_perf + 0.20·S_eff − P_thermal`)
rewards being lean: 30% of the score is generation speed relative to the fastest team,
and 20% rewards low peak RAM under the 7 GB ceiling. A large model would forfeit half
the score chasing marginal accuracy. Because accuracy is graded on a **fixed agriculture
domain** (not open-ended knowledge), a small base model fine-tuned on agronomic Q&A can
reach competitive accuracy while keeping a small, fast, low-memory footprint.

- **Base model:** Qwen2.5-1.5B-Instruct (Apache-2.0). Chosen for strong instruction-
  following at small scale, a permissive licence, and a multilingual tokenizer that
  handles Hausa text reasonably before fine-tuning.
- **Fine-tuning:** QLoRA on a bilingual (EN/HA) agriculture instruction dataset covering
  crop agronomy, pest/disease diagnosis, livestock husbandry, weather-timing, and market
  advisory for the target region's staple crops and livestock.
- **Quantization:** Q4_K_M — the standard quality/footprint balance for CPU inference via
  llama.cpp. (Alternatives evaluated below.)
- **Runtime:** llama.cpp / GGUF (mandated by the challenge).

### Alternatives considered

| Option | Outcome |
|---|---|
| Qwen2.5-0.5B-Instruct fine-tune | A/B candidate — maximises speed + efficiency; submit if accuracy holds within target |
| Qwen2.5-3B / Llama-3.2-3B | Rejected — speed and efficiency penalties outweigh accuracy gain under the formula |
| Q8_0 / Q5_K_M quant | Higher quality but larger RAM/slower — held as fallback if Q4_K_M accuracy drops too far |
| Q2_K / Q3 quant | Rejected — domain accuracy degraded too aggressively in testing |
| RAG-only, no fine-tune | Rejected for the *scored* model — retrieval is not in the automated accuracy loop; RAG retained as the cross-disciplinary showcase layer (see below) |

### Cross-disciplinary pairing (load-bearing)

The challenge requires the LLM to connect to a second deep-tech discipline in a
load-bearing way. Our pairing is **information retrieval — a location-aware offline RAG
system** over local agronomic data the model cannot hold in its weights:

- per-LGA planting calendars and recommended windows,
- current local market prices and input costs,
- recent pest/disease outbreak advisories.

The farmer's location selects the relevant local corpus; the model reasons and answers in
English or Hausa while retrieval supplies the volatile, region-specific ground truth.

**Why it is load-bearing, not cosmetic:** delete the retrieval layer and every
location-specific, time-sensitive fact disappears — prices, dated calendars, outbreak
alerts — leaving only generic advice. The system's usefulness depends on the pairing.
(Optional stretch for the Best Integration Award: an on-device computer-vision crop-disease
classifier that turns a leaf photo into a diagnosis the LLM explains and acts on.)

---

## Constraints

- **Hardware target:** 4 vCPU, 8 GB DDR4 RAM, integrated graphics, Ubuntu 22.04 — no
  discrete GPU. Pure CPU inference via llama.cpp.
- **Memory:** hard 7 GB peak-RSS ceiling; OOM = disqualification. Q4_K_M on a 1.5B model
  keeps peak RAM well under budget (see Benchmarks).
- **Connectivity:** zero network dependency at inference — the entire reason the model is
  on-device.
- **Data:** agronomic guidance is regionally specific; the dataset is scoped to the target
  belt's staple crops/livestock and to Hausa as the dominant local language.

---

## Benchmarks

> Self-reported development benchmarks. Replace the placeholder values with real numbers
> from `adtc-profiler run --mode participant` on your target-class machine
> (HP EliteBook 840 G6 stands in for the ADTC Standard Laptop).

| Metric | Value |
|---|---|
| Dev machine | HP EliteBook 840 G6 (i5/i7 8th-gen, integrated, 8 GB) |
| Base model | Qwen2.5-1.5B-Instruct |
| Quantization | GGUF Q4_K_M |
| Peak RAM (RSS) | _TODO_ GB |
| Time to first token | _TODO_ ms |
| Generation speed | _TODO_ t/s |
| Thermal throttling | _TODO_ |
| Local accuracy proxy (arc_easy / domain set) | _TODO_ |

Official scores are measured by the ADTC profiler on the standard evaluation machine.
