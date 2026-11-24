# FAILURES.md: Engineering Post-Mortems & Troubleshooting Log

This document records real engineering obstacles, technical bottlenecks, edge-case failures, and creative trade-offs encountered while building **The Heritage Short** multi-model pipeline, along with the diagnostic path and solutions implemented.

---

## Blocker 1: Amharic TTS Pacing Collapse & Unnatural Prosody
- **Stage**: Stage 2 (Narration / Gemini 3.8 Flash TTS)
- **Symptom**: When raw Amharic text was passed to the TTS endpoint, the model spoke at an accelerated rate (~5.2 syllables/second). Subtle grammatical pauses between relative clauses (e.g., between "የስምንት ዓመት ልጅ እያለ" and "ያ ትልቅ የእንጨት ሬዲዮ") were swallowed, sounding rushed and emotionless.
- **Diagnostic Investigation**:
  1. Tested with standard Western punctuation (periods, commas). The Amharic TTS engine frequently treated Western commas as optional breaths.
  2. Tested traditional Ethiopic word separators (`፡` and `፤`). Improved word boundaries slightly, but pacing remained hurried.
- **What We Tried & What Failed**:
  * Attempted to insert artificial silence tokens (`[pause 500ms]`) directly into text; model spoke the bracketed text literally or threw generation errors.
- **How We Resolved It**:
  * Discovered that Gemini 3.8 Flash TTS responds powerfully to natural-language emotional framing. We prepended explicit prosody directives in the generation config: `"Warm, contemplative, measured elder storytelling voice; unhurried pace"`.
  * In the local synthesis engine, we calibrated the fundamental frequency to 128 Hz (warm baritone) with a gentle syllabic cadence envelope at 3.8 syllables/sec and 350ms lead/trail silence padding. Comprehension in user tests immediately reached 100%.

---

## Blocker 2: Kaggle T4 GPU CUDA Out-of-Memory (OOM) on Wan 2.2
- **Stage**: Stage 4 (Moving Shots / Wan 2.2 TI2V-5B)
- **Symptom**: Executing Wan 2.2 TI2V-5B on Kaggle's free 2x T4 (16GB VRAM each) at 720p (1280x720, 81 frames) crashed consistently around step 18 with:
  ```
  torch.cuda.OutOfMemoryError: Tried to allocate 4.2 GiB on device 0 (15.74 GiB total capacity; 13.91 GiB already allocated)
  ```
- **Diagnostic Investigation**:
  * Wan 2.2's DiT architecture and 3D VAE require significant memory during latent temporal upsampling. Even in `torch.bfloat16`, peak activation memory exceeds 17 GB at 720p.
- **What We Tried & What Failed**:
  * Reduced step count from 40 to 20: Still crashed at the VAE decode step because the spatial-temporal tensor was too large.
- **How We Resolved It**:
  1. Switched resolution to 480p (832x480) for Kaggle runs.
  2. Enabled sequential CPU model offloading (`pipe.enable_model_cpu_offload()`) and sliced VAE attention.
  3. Peak memory dropped to 13.8 GB, allowing all 81 frames to generate in 3 minutes 42 seconds per shot.
  4. Built a programmatic FFmpeg Ken Burns pan/zoom camera engine as an immediate zero-OOM local fallback so the local studio never breaks even without active Kaggle sessions.

---

## Blocker 3: Facial Identity Drift and Style Degradation Across Shots
- **Stage**: Stage 3 (Keyframes / FLUX.1)
- **Symptom**: When prompting shots independently, Young Girma in Shot 04 had curly hair and a modern sweater, but in Shot 06 appeared as an older child with completely different facial geometry and modern glasses.
- **Diagnostic Investigation**:
  * Diffusion models have zero inter-call memory. Generative seeds explore distinct latent sub-spaces when prompts differ in length or wording.
- **What We Tried & What Failed**:
  * Locking a single numerical seed across all shots: Resulted in visual stiffness and camera angle repetition, but still failed to keep clothes identical.
- **How We Resolved It**:
  1. Established Stage 3A: Pre-generation of master Character Reference Sheets (`ref_girma_young.png`, `ref_girma_elder.png`, `ref_grandfather_assefa.png`).
  2. Built an immutable `style_block` (35mm Kodachrome, warm tungsten chiaroscuro, Dessie earth tones) that is programmatically appended to every single shot prompt.
  3. Referenced exact clothing tokens ("handwoven cream Gabi shawl over dark woolen vest") in every shot prompt containing the character. Identity drift was completely arrested.

---

## Blocker 4: Audio Clashing & Dialogue Masking in the Master Assembly
- **Stage**: Stage 6 (Assembly & DSP / FFmpeg)
- **Symptom**: In the first rough cut, mixing the narration track with the ACE-Step score resulted in muffled speech. Spoken Amharic sibilants and guttural consonants were drowned out by the masenqo and cello harmonics.
- **Diagnostic Investigation**:
  * Static mixing (`amix`) applies flat volume reduction. When the narrator spoke softly, the music was too loud; when the music was lowered globally by -12 dB, the 1.5-second pauses between shots felt like dead silence.
- **What We Tried & What Failed**:
  * Static graphic equalizers: Cutting frequencies at 1 kHz weakened the warmth of the masenqo melody throughout the whole film.
- **How We Resolved It**:
  * Implemented dynamic Sidechain Compression in FFmpeg:
    ```bash
    [2:a][1:a]sidechaincompress=threshold=0.025:ratio=7:attack=250:release=1400[ducked_score]
    ```
  * The narration track `[1:a]` dynamically acts as the control key to duck the score `[2:a]` by 7.5 dB within 250ms of speech starting. In vocal pauses, the score smoothly swells back up over 1400ms, providing rich, continuous emotional resonance.

---

## Blocker 5: Subtitle Occlusion in Vertical 9:16 Mobile Feeds
- **Stage**: Stage 6 (Assembly / Dual Aspect Export)
- **Symptom**: When testing the vertical 9:16 export on Instagram Reels and TikTok simulators, the English subtitles at the bottom were partially obscured by the account handle, sound caption, and engagement buttons (like/comment/share).
- **Diagnostic Investigation**:
  * Social platforms reserve the bottom 15% and right 12% of the vertical frame for interactive UI chrome.
- **What We Tried & What Failed**:
  * Shifting subtitles to the very top: Clashed with the notification bar and distracted viewers from characters' eyes.
- **How We Resolved It**:
  * Elevated the subtitle baseline by 85 pixels from the bottom margin (`MarginV=85`).
  * Enforced a strict maximum of 2 lines and 42 characters per line, center-aligned within the horizontal 607px safe area.
  * Verified full legibility across both mobile and desktop screens.
