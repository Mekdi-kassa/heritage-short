# PUBLIC_POST.md: Public Social Media Post Draft

> **Assignment 2 Deliverable**: A public post written by the creator telling the story behind the film, why it matters, and one key engineering lesson learned, with the platform's AI label explicitly disclosed.

---

### Platform: LinkedIn / X (Twitter) / YouTube Post

**Title**: *The Radio Craftsman of Dessie (የደሴው ሬዲዮ ጠጋኝ): What Soldering Radios in 1978 Taught Me About Building AI Pipelines in 2026*

Growing up, there was one story my father told me that I never forgot.

In 1978, in the misty highland town of Dessie, Ethiopia, his family's grand wooden valve radio went dead. In those days, a radio wasn't just a gadget; it was the entire town's connection to the world—the evening news, market prices, and the warm voice of Tilahun Gessesse. When the broadcast vanished, my grandfather sighed, assuming it was gone forever.

My father, just eight years old at the time, didn't accept the silence. He unlatched the back panel, peered into the warm amber glow of vacuum tubes, and found a single severed copper wire. With no engineering degree, just a hand-heated iron tip, patience, and clean hands, he soldered the joint. When he turned the brass knob, static crackled—and music flooded the room. 

My grandfather held his shoulder and told him:
*"He who mends what is broken with gentle hands learns how to listen to the world."*

Over the past three days as part of 10 Academy's engineering challenge, I turned that memory into a 75-second heritage short film. But I didn't edit it in Premiere or generate clips by hand. I built an autonomous studio in Python: a multi-model pipeline governed by a strict JSON schema contract that orchestrates Gemini 3.8 Flash for Amharic narration, FLUX for 35mm highland keyframes, Wan 2.2 for camera motion, ACE-Step for an original Tizita pentatonic score, and FFmpeg for sidechain audio ducking.

**The biggest lesson I learned building this:**
The real value of an AI engineer isn't in calling a single frontier API; it is in the precision of the architecture around the call. Models will change every six months, but the discipline of setting strict contracts, caching hashes so re-runs cost nothing, handling CUDA out-of-memory errors on free GPUs, and making sure the music ducks gracefully beneath the storyteller's voice—that is the craftsmanship that survives.

Whether twisting copper wires in Wollo in 1978 or wiring neural pipelines in code in 2026, engineering has always been an act of listening.

Watch the film below (available in both 16:9 cinema and 9:16 mobile format).

---
**AI Disclosure**: This film was created with artificial intelligence tools (Gemini 3.8 Flash TTS, FLUX.1, Wan 2.2, ACE-Step 1.5, and FFmpeg) guided by human storytelling and family oral history. Fully labeled under platform AI disclosure policies.

#AI #GenerativeAI #Ethiopia #Heritage #10Academy #MachineLearning #Python #Storytelling #OpenSource #SoftwareEngineering
