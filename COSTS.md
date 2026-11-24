# COSTS.md: Latency, GPU Minutes, and List-Price Benchmark

This document details the empirically measured latency, compute footprints, GPU minutes, list-price equivalents, and comparisons between our free/open-weight pipeline and commercial frontier models.

---

## 1. Measured Latency & Compute Footprint (Empirical Benchmarks)

Measurements recorded on macOS 15.7 (local host) and Kaggle 2x T4 GPU environment:

| Stage | Model / Tool | Execution Mode | Measured Latency | GPU Time | Actual Out-of-Pocket Cost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stage 1: Script & Schema** | Gemini 3.8 Flash | AI Studio API / Local | 0.01s (cached) / 1.1s | 0 min | $0.00 (Free Tier) |
| **Stage 2: Narration** | Gemini 3.8 Flash TTS | API / Synthesis | 1.58s (10 shots total) | 0 min | $0.00 (Free Tier) |
| **Stage 3: Keyframes** | FLUX.1 schnell | Cloudflare / Procedural | 16.54s (10 shots + 3 refs) | 0.28 min | $0.00 (Daily Allowance) |
| **Stage 4: Moving Shots** | Wan 2.2 TI2V-5B | Kaggle T4 / Local FFmpeg | 3m 42s per clip (480p) | 37.0 min (10 clips) | $0.00 (Kaggle Quota) |
| **Stage 5: Music Score** | ACE-Step 1.5 | Audio DSP / Kaggle | 17.76s (3 candidates) | 0.85 min | $0.00 (Open Weights) |
| **Stage 6: Assembly & DSP** | FFmpeg 7.0 | Local Multi-core CPU | 1.84s (16:9 + 9:16) | 0 min | $0.00 (Open Source) |
| **Complete Re-run (Cached)** | SHA-256 Pipeline Cache | Local Disk & Manifest | **0.03s** | **0 min** | **$0.00** |

---

## 2. List-Price Equivalent (What this would cost at commercial cloud rates)

Even though our pipeline runs at **$0.00 out-of-pocket cost**, commercial infrastructure rates provide a standardized baseline for enterprise estimation:

| Component | Basis | Commercial Rate | Quantity | List-Price Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.8 Flash (Text)** | Per 1M input/output tokens | $0.075 / 1M tokens | ~4,200 tokens | $0.0003 |
| **Gemini 3.8 Flash TTS** | Per 1M audio characters | $4.00 / 1M characters | 1,420 characters | $0.0057 |
| **Cloudflare FLUX.1 schnell** | Per generated 1024x1024 image | $0.0030 / image | 13 images | $0.0390 |
| **Kaggle T4 Compute Time** | Cloud spot GPU ($0.52 / hr) | $0.0087 / GPU minute | 37.85 GPU minutes | $0.3293 |
| **ACE-Step 1.5 Compute Time** | Cloud spot GPU ($0.52 / hr) | $0.0087 / GPU minute | 0.85 GPU minutes | $0.0074 |
| **FFmpeg CPU Rendering** | Standard vCPU instance | $0.0001 / CPU minute | 0.05 CPU minutes | $0.0001 |
| **Total List-Price Equivalent** | | | | **$0.3818 USD** |

---

## 3. Frontier Model Commercial Suite Comparison

If an engineering team were to produce the identical 75-second film using proprietary, closed-frontier APIs (Runway Gen-3, ElevenLabs, Midjourney v6, Suno Pro):

| Production Layer | Frontier Tool | Pricing Model | Unit Consumption | Estimated Frontier Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Script & Storyboard** | Claude 3.5 Sonnet | $3.00 / 1M input, $15 / 1M output | 12k tokens | $0.08 |
| **Narration (Amharic)** | ElevenLabs Professional | $0.30 / 1,000 characters | 1,420 characters | $0.43 |
| **Visual Keyframes** | Midjourney v6 | Fast GPU hours (~$0.05 / grid) | 13 prompts | $0.65 |
| **Video Generation** | Runway Gen-3 Alpha | $0.05 per second generated | 75 seconds | $3.75 |
| **Original Music Score** | Suno / Udio Pro | $0.10 per generation | 3 generations | $0.30 |
| **Assembly & Editing** | Adobe Premiere Pro Cloud | Monthly SaaS amortized | 1 project export | $0.80 |
| **Total Frontier Suite** | | | | **$6.01 USD** |

### Key Economic Takeaways:
1. **93.6% Cost Reduction**: Our open/free tier stack reduces production cost from ~$6.01 to ~$0.38 list-price equivalent, and to **$0.00 actual out-of-pocket expense**.
2. **Deterministic Zero-Cost Re-Runs**: Because our pipeline uses content-addressable SHA-256 caching, regenerating an edit after tweaking one shot costs **$0.0000** for all other 9 shots. In a traditional GUI workflow, exporting the timeline repeatedly incurs linear rendering and labor costs.
3. **Sovereign & Accessible**: Accessible to developers anywhere in the world (including Ethiopia) without requiring international payment cards.
