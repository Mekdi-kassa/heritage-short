# WALKTHROUGH_SCRIPT.md: 5-Minute Technical Video Guide

> **Assignment 2 Deliverable**: A concise, professional video walkthrough of at most 5 minutes explaining the architecture, one hard engineering decision, and a live demonstration of single-shot regeneration.

---

## Video Outline & Time Budget (Total: 4 min 30 sec)

| Section | Duration | Visual on Screen | Key Spoken Points |
| :--- | :--- | :--- | :--- |
| **1. Hook & Premise** | 0:00 - 0:45 | `storyboard.json` + Quick clip of Shot 06 | Introduce *The Radio Craftsman of Dessie*, family premise, and the goal of building an autonomous studio in code. |
| **2. Architecture & Contracts** | 0:45 - 1:45 | VS Code terminal + `ARCHITECTURE.md` diagram | Explain the single contract `storyboard.json`, strict JSON schema validation, and the 5 decoupled stages. |
| **3. One Hard Decision** | 1:45 - 2:45 | FFmpeg filtergraph in `pipeline/assemble.py` + Spectrogram | Explain audio ducking via `sidechaincompress` vs flat volume reduction, and managing Kaggle T4 VRAM limits on Wan 2.2. |
| **4. Live Single-Shot Regeneration** | 2:45 - 4:00 | Terminal live execution | Change Shot 06 prompt/narration in `storyboard.json`. Run `python3 run_pipeline.py --shot shot_06`. Point to logs showing only Shot 06 re-runs while Shots 1-5 and 7-10 hit cache! |
| **5. Deliverables & Ethics** | 4:00 - 4:30 | Finder showing 16:9, 9:16, `ETHICS.md` | Show dual aspect ratios, AI end card, and consent compliance. |

---

## Detailed Spoken Script

### [0:00 - 0:45] Hook & Premise
*"Hello everyone! Today I'm walking you through my project for 10 Academy: 'The Radio Craftsman of Dessie' — an AI-generated 75-second heritage short film and reproducible multi-model pipeline.*

*The story is deeply personal: it recounts how my father, as an eight-year-old boy in Dessie in 1978, revived his grandfather's silent valve radio by soldering a broken copper wire. But rather than editing this film by hand in traditional software, I built an automated studio in Python where every stage is governed by code."*

### [0:45 - 1:45] Architecture & Contracts
*"Let's look at the codebase. Everything is organized around a single immutable contract: `storyboard.json`. Before any model runs, `schema/storyboard.schema.json` validates every field: the exact 75-second timeline, Amharic narration, English subtitles, camera motion, and design intent reasons.*

*The pipeline has five decoupled stages:*
- *Stage 1 verifies the script and schema.*
- *Stage 2 generates Amharic TTS narration and aligned SRT subtitles.*
- *Stage 3 builds character reference sheets and 35mm keyframes with FLUX.*
- *Stage 4 produces moving shots via Wan 2.2 and cinematic camera dynamics.*
- *Stage 5 synthesizes an original Ethiopian Tizita pentatonic score with ACE-Step.*
- *And Stage 6 assembles the final film in FFmpeg."*

### [1:45 - 2:45] One Hard Technical Decision
*"One of the hardest engineering decisions was post-production audio mixing. In our early prototype, simply mixing the music and voice with standard volume reduction muffled the delicate consonants of spoken Amharic, while leaving empty dead silence during pauses between shots.*

*Rather than settling for flat audio, I designed a professional dynamic sidechain compression filtergraph in FFmpeg (`sidechaincompress`). The narration track dynamically acts as a control key: whenever speech occurs, the music drops by 7.5 dB within 250 milliseconds. When the narrator pauses, the music gently swells back up over 1400 milliseconds. We then pass the master mix through an EBU R128 `loudnorm` filter to lock broadcast compliance at -14 LUFS."*

### [2:45 - 4:00] Live Single-Shot Regeneration (The Live Proof)
*"Now, let me demonstrate the core software engineering strength of this studio: content-addressable SHA-256 caching.*

*In an ordinary generative pipeline, changing one detail requires re-running everything, wasting precious GPU minutes. In our studio, each shot is hashed independently.*

*Watch this: I'll open `storyboard.json` and modify the prompt for Shot 06 — our soldering climax. Or better yet, I will run our targeted shot regenerator directly in the terminal:*

```bash
python3 run_pipeline.py --shot shot_06
```

*[Point to terminal logs]*
*Notice what just happened:*
*Shots 01 through 05 returned `(CACHED)` in 0.01 seconds.*  
*Shot 06 was regenerated live in 1.7 seconds.*  
*Shots 07 through 10 returned `(CACHED)` in 0.01 seconds.*  
*And the master 16:9 and 9:16 cuts were instantly re-assembled! Every single model call is recorded with its seed, latency, and cost right here in `runs.jsonl`."*

### [4:00 - 4:30] Closing & Compliance
*"Finally, in `outputs/final/`, we have our complete deliverables: both the 16:9 landscape master and the 9:16 vertical short, fully compliant with mobile safe areas. Every real person depicted has a verified consent record in `ETHICS.md`, and the film concludes with a visible AI attribution end card.*

*Thank you for watching, and enjoy The Radio Craftsman of Dessie!"*
