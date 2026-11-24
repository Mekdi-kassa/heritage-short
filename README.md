# የደሴው ሬዲዮ ጠጋኝ (The Radio Craftsman of Dessie)

> **A 75-second heritage short film and reproducible multi-model AI studio pipeline built for 10 Academy.**

[![Validation](https://img.shields.io/badge/Storyboard%20Schema-Valid-brightgreen)](#)
[![License: Apache 2.0 / MIT](https://img.shields.io/badge/License-Apache%202.0%20%7C%20MIT-blue)](#)
[![Zero-Cost Stack](https://img.shields.io/badge/Out--of--Pocket%20Cost-$0.00-success)](#)
[![Dual Aspect](https://img.shields.io/badge/Outputs-16:9%20%7C%209:16-orange)](#)

---

## 1. Story Overview

*In the misty highlands of Dessie in 1978, a young boy learns that broken radios and broken days can be mended with patience, copper wire, and an attentive ear. Decades later, that same craftsmanship bridges generations as his family builds neural pipelines in code.*

- **Duration**: 75.0 seconds (10 timed shots)
- **Narration Language**: Amharic (አማርኛ)
- **Subtitles**: English open captions (synchronized SRT)
- **Music**: Original Ethiopian Tizita minor pentatonic score (acoustic masenqo, krar, cello drone, washint flute)
- **Aspect Ratios**: 16:9 Landscape (`1920x1080`) and 9:16 Portrait (`1080x1920`)

---

## 2. One-Command Quickstart

A stranger can clone this repository, run **one command**, and regenerate the entire film end-to-end:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/the-heritage-short.git
cd the-heritage-short

# 2. Run the entire pipeline (validates contract, generates assets, ducks audio, exports video)
python3 run_pipeline.py --all
# or using Make:
make film
```

All generated deliverables will immediately populate `outputs/final/`:
- `outputs/final/heritage_short_16x9.mp4`: Master 16:9 landscape short.
- `outputs/final/heritage_short_9x16.mp4`: Master 9:16 vertical short with mobile safe-area padding.
- `outputs/final/radio_cut.mp4`: Audio animatic prototype (narration + score over black screen).

---

## 3. Targeted Single-Shot Live Regeneration (For Walkthrough Demo)

The pipeline employs a cryptographic **SHA-256 caching engine**. If you modify a prompt or narration line in `storyboard.json` (or target a shot directly), **only that single shot regenerates** while all other shots complete in 0.01 seconds from cache:

```bash
# Regenerate only Shot 06 live (demonstrated in walkthrough video)
python3 run_pipeline.py --shot shot_06
# or using Make:
make shot SHOT=shot_06
```

---

## 4. The Multi-Model Studio Stack (At $0.00 Cost)

| Pipeline Layer | Model / Technology | Provider / Host | Free Tier Access |
| :--- | :--- | :--- | :--- |
| **Contract & Schema** | JSON Schema (Draft 2020-12) | Local Pure Python | 100% Offline / Zero Dependency |
| **Script & Storyboard** | Gemini 3.8 Flash | Google AI Studio | Free Tier (Ethiopia supported) |
| **Narration (Amharic)**| Gemini 3.8 Flash TTS | Google AI Studio | 130+ languages free tier |
| **Keyframes & Consistency**| FLUX.1 schnell / klein | Cloudflare Workers AI | Daily free allowance |
| **Moving Shots** | Wan 2.2 TI2V-5B / FFmpeg | Kaggle (2x T4 GPU) / Local | 30 GPU hrs/week on Kaggle |
| **Score & Music** | ACE-Step 1.5 | Kaggle / Local Audio DSP | MIT License open weights |
| **Assembly & Ducking** | FFmpeg 7.0 (sidechaincompress) | Local CPU | Open Source |

---

## 5. Repository Structure

```
├── README.md               # Quickstart, stack overview, and execution instructions
├── storyboard.json         # The central contract: shots, prompts, narration, music cues
├── run_pipeline.py         # Master orchestrator CLI with caching and retries
├── Makefile                # Make targets: film, validate, radiocut, shot, clean
├── runs.jsonl              # Complete audit log of every model call (latency, seed, cost)
├── kaggle_wan22_runner.py  # Exported Kaggle batch execution runner for Wan 2.2
│
├── schema/
│   └── storyboard.schema.json  # Strict JSON Schema validating the storyboard contract
│
├── pipeline/               # Modular stage scripts (one per layer)
│   ├── __init__.py
│   ├── cache.py            # SHA-256 content-addressable caching engine
│   ├── logger.py           # Thread-safe runs.jsonl execution logger
│   ├── validate.py         # Strict contract validation runner
│   ├── script.py           # Stage 1: Contract verification & semantic review
│   ├── narration.py        # Stage 2: Amharic TTS & SRT subtitle alignment
│   ├── keyframes.py        # Stage 3: Character reference sheets & 35mm keyframes
│   ├── shots.py            # Stage 4: Wan 2.2 video generation & camera dynamics
│   ├── music.py            # Stage 5: ACE-Step 1.5 Tizita score synthesis
│   └── assemble.py         # Stage 6: Sidechain ducking, -14 LUFS normalizer, dual export
│
├── outputs/                # Generated media artifacts
│   ├── audio/              # Narration WAVs, score candidates, and master score
│   ├── keyframes/          # Character reference sheets & 720p keyframes
│   ├── shots/              # 24fps moving video clips
│   ├── subtitles/          # english.srt and amharic.srt open caption files
│   └── final/              # radio_cut.mp4, heritage_short_16x9.mp4, heritage_short_9x16.mp4
│
├── DESIGN.md               # Audience personas, emotional intent, and user test logs
├── ARCHITECTURE.md         # Stage contracts, dataflow diagram, caching, and DSP graph
├── EXPERIMENTS.md          # 10 controlled experiments (Hypothesis → Change → Result)
├── FAILURES.md             # Real blockers (OOM, prosody, style drift) & troubleshooting
├── COSTS.md                # Measured latency, GPU minutes, and list-price benchmarks
├── ETHICS.md               # Consent records, license audit, and AI disclosure plan
├── REPORT.md               # Comprehensive Assignment 1 submission report
├── WALKTHROUGH_SCRIPT.md   # Script and guide for 5-minute video demo
└── PUBLIC_POST.md          # Public post text with AI transparency disclosure
```

---

## 6. Project Documentation Index

- [DESIGN.md](file:///Users/mac/Desktop/tenx/DESIGN.md): Detailed audience personas, emotional intent, and verbatim feedback from two rounds of user testing.
- [ARCHITECTURE.md](file:///Users/mac/Desktop/tenx/ARCHITECTURE.md): Deep dive into stage boundaries, cryptographic caching, and FFmpeg filtergraphs.
- [EXPERIMENTS.md](file:///Users/mac/Desktop/tenx/EXPERIMENTS.md): 10 logged experiments with empirical evidence.
- [FAILURES.md](file:///Users/mac/Desktop/tenx/FAILURES.md): Real failures encountered (OOM on T4, Amharic prosody) and their engineering workarounds.
- [COSTS.md](file:///Users/mac/Desktop/tenx/COSTS.md): Full latency measurements and list-price cost comparisons ($0.38 list equivalent vs $6.01 frontier suite).
- [ETHICS.md](file:///Users/mac/Desktop/tenx/ETHICS.md): Informed consent record for family subjects, model license audit, and social platform labeling.
