# Assignment 1 Report: The Heritage Short Pipeline

**Candidate Submission**: B2W0: AI-Content Generation — Codebase and Report  
**Project Title**: *የደሴው ሬዲዮ ጠጋኝ (The Radio Craftsman of Dessie)*  
**Repository**: Public GitHub Repository  
**Target Duration**: 75.0 Seconds | **Language**: Amharic (አማርኛ) with English Subtitles  

---

## 1. Executive Summary & Creative Vision

Over the past three days, I set out to construct a miniature autonomous film studio in code: a multi-model software pipeline orchestrated around an immutable JSON contract (`storyboard.json`) that transforms a personal family oral history into a 75-second cinematic heritage short. 

The story, *የደሴው ሬዲዮ ጠጋኝ (The Radio Craftsman of Dessie)*, recounts how my father, Ato Girma, as an eight-year-old boy in the misty highlands of Dessie in 1978, revived his grandfather's silent valve radio by diagnosing a single severed copper wire and soldering it with patience and steady hands. The narrative bridges generations, demonstrating that the discipline of building modular neural pipelines in 2026 is spiritually continuous with the analog craftsmanship of 1978.

The project was designed with three audience personas in mind:
1. **Bethlehem (Diaspora Youth)**: Needs cultural resonance and clear English subtitles on mobile feeds (9:16).
2. **Ato Assefa (Highland Elder)**: Demands historical respect, dignified Amharic cadence, and acoustic warmth.
3. **Dawit (Technical Peer)**: Evaluates schema contracts, input-hash caching, audio ducking, and reproducible engineering.

---

## 2. Reflection and Learning from Audience Testing

Following the human-centered design thinking loop (*Empathize → Define → Ideate → Prototype → Test*), I conducted two formal feedback rounds with at least three representative viewers at distinct fidelity milestones:

### Test Milestone 1: The Radio Cut (Audio-Only Prototype)
Before spending a single GPU minute on visual diffusion, I assembled a 75-second "Radio Cut" (`outputs/final/radio_cut.mp4`): Amharic TTS narration over a temporary masenqo/krar score on a black screen.
- **Audience Feedback**: Viewers pointed out that the spoken Amharic in Shot 04 rushed through the word "ምስጢር" (secret) at 5.2 syllables/sec, causing comprehension to slip. Furthermore, when the radio broke in Shot 03, the silence was too sudden and jarring.
- **What Changed**: I lowered the target speech rate to 3.8 syllables/sec, added explicit emotional prosody descriptors (`voice_style: "Warm, contemplative elder voice"`), and added a solitary sustained cello harmonic in the score to musically cushion the radio's power failure.

### Test Milestone 2: The Near-Final Cut (Dual Aspect Ratios)
After generating keyframes, camera dynamics, and the final Tizita score, I shared both the 16:9 and 9:16 cuts with viewers.
- **Audience Feedback**: A video editor noted that in the vertical 9:16 export, the bottom-centered English subtitles collided with the description and engagement overlay on mobile platforms.
- **What Changed**: I refactored the FFmpeg assembly script to elevate the subtitle baseline by 85 pixels (`MarginV=85`) and enforced a maximum line length of 42 characters across 2 lines.

---

## 3. The Hardest Technical Problem & How It Was Solved

### The Bottleneck: Wan 2.2 VRAM Out-Of-Memory (OOM) on Kaggle 16GB T4
The most demanding engineering challenge was running the open-weight **Wan 2.2 TI2V-5B** image-to-video diffusion transformer within the free Kaggle environment (2x T4 16GB VRAM). Attempting native 720p (1280x720) generation across 81 frames repeatedly crashed CUDA memory during temporal 3D-VAE decoding, requesting upwards of 17.8 GB of VRAM.

### The Solution: Multi-Layer Optimization & Resilient Fallback Architecture
1. **Resolution Drafting & Offloading**: I adjusted the generation profile to 480p (832x480) with sequential CPU model offloading (`pipe.enable_model_cpu_offload()`) and fp8 quantization. This reduced peak memory to 13.8 GB, allowing all 81 frames to generate in 3 minutes 42 seconds per clip.
2. **Deterministic Camera Fallback**: To ensure that the repository runs seamlessly on any local machine even when GPU quotas are exhausted or offline, I engineered a programmatic FFmpeg camera dynamics engine (`pipeline/shots.py`) that applies smooth 24fps Ken Burns pan-and-scan, push-in, and tracking movements directly to keyframes.
3. **Content-Addressable Invalidation**: By hashing prompts and durations with SHA-256, changing one shot only invalidates that specific clip, saving massive GPU queue time.

---

## 4. Suggested Practices Tested Honestly

### Practice That Beat My Instinct: Character Reference Sheets Before Keyframes
*My initial instinct* was to write vivid, spontaneous prompts for each shot directly, trusting the image model to produce an Ethiopian boy in various settings.  
*The result of following advice*: I adhered to the recommended practice of generating dedicated Character Reference Sheets (`ref_girma_young.png`, `ref_girma_elder.png`, `ref_grandfather_assefa.png`) and appending a locked global `style_block` to all prompts. This practice dramatically eliminated character drift. In User Test 2, all viewers immediately recognized Young Girma across Shots 04, 06, 07, and 08 without hesitation.

### Practice That Did Not Beat My Instinct: Relying Exclusively on Text-to-Video Prompts
*The suggested practice* frequently suggests drafting video clips directly from text descriptions.  
*Why it failed*: Text-to-video for an intricate historical narrative produced severe hallucinations—random modern clothing, mutating radios, and distorted hands soldering air.  
*My counter-solution*: Image-to-Video (TI2V) conditioned strictly on approved 35mm keyframes, where the video prompt describes *only* camera motion and physical action, proved incomparably superior. Conditioning on fixed pixels anchored the lighting and spatial composition, allowing the diffusion model to focus exclusively on temporal motion vectors.

---

## 5. Curiosity Beyond the Floor (Ceiling Work)

Rather than simply connecting pre-built cloud APIs, I extended the project into three advanced engineering directions:

1. **Pure-Python Pentatonic Audio DSP Synthesizer (`pipeline/music.py`)**:
   Recognizing that external music APIs frequently introduce unexpected vocal artifacts, I engineered a zero-dependency audio synthesis engine in pure Python. It synthesizes a 75-second multi-track score in the authentic **Ethiopian Tizita pentatonic scale** (E minor: E, F#, G, B, C) featuring bowed saw/sine harmonics with pitch vibrato (masenqo), damped exponential decay plucks (krar), and a warm fundamental cello drone.
2. **Granular SHA-256 Cache & Single-Shot Live Regeneration**:
   I built an idempotent caching engine (`pipeline/cache.py`) that fingerprints stage inputs. Changing a single line in `storyboard.json` and running `python3 run_pipeline.py --shot shot_06` regenerates only Shot 06 in 1.7 seconds, while all other 9 shots return in 0.01 seconds from cache.
3. **Automated Kaggle Batch Runner (`kaggle_wan22_runner.py`)**:
   I authored a standalone, headless Kaggle notebook script that ingests the validated `storyboard.json` and executes Wan 2.2 TI2V-5B batch inference with automated error recovery.

---

## 6. What I Would Build Next

If given another week with this codebase, I would:
1. **Train a Custom Character LoRA**: Train a lightweight Low-Rank Adaptation (LoRA) checkpoint on traditional Wollo highland textiles, architecture, and family facial photographs to achieve 100% photo-realistic facial continuity.
2. **Self-Service Family Oral History Web App**: Wrap this CLI pipeline in a lightweight web interface where older family members can upload a voice note in Amharic or Afaan Oromo and receive a synchronized, scored animatic short within minutes.
