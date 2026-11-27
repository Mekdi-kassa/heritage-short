"""
=============================================================
  Wan 2.2 TI2V-5B — Heritage Short Film Shot Generator
  Run this as a Kaggle Notebook (GPU T4 x2 or P100)
  Generates 10 animated video shots from keyframe PNGs
=============================================================

INSTRUCTIONS (read before running):
1. Upload your keyframe PNGs to Kaggle as a Dataset:
   outputs/keyframes/shot_01.png → shot_10.png
2. Set Runtime → Accelerator → GPU T4 x2
3. Run all cells top to bottom
4. Download the generated shot_01_wan.mp4 → shot_10_wan.mp4
5. Put them in outputs/shots/ on your Mac and re-render
"""

# ── CELL 1: Install dependencies ──────────────────────────────────────────────
# !pip install -q "diffusers>=0.33.0" transformers accelerate imageio[ffmpeg] Pillow torch torchvision

# ── CELL 2: Check GPU ─────────────────────────────────────────────────────────
import torch
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM:", round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1), "GB")

# ── CELL 3: Load Wan 2.2 TI2V pipeline ───────────────────────────────────────
from diffusers import WanImageToVideoPipeline, AutoencoderKLWan
from diffusers.utils import export_to_video
from PIL import Image
import numpy as np

print("Loading Wan 2.2 TI2V-5B pipeline (this takes ~5 min first time)...")
pipe = WanImageToVideoPipeline.from_pretrained(
    "Wan-AI/Wan2.2-TI2V-5B",
    torch_dtype=torch.bfloat16,
)
pipe.enable_model_cpu_offload()
print("Pipeline ready!")

# ── CELL 4: Shot definitions (prompts + durations) ───────────────────────────
import os

SHOTS = [
    {
        "id": "shot_01",
        "prompt": "Extreme wide cinematic establishing view of Dessie Ethiopia in early morning mist, rolling green Wollo mountains, tin and stone rooftops glowing under golden sunrise, woodsmoke drifting gently. Slow smooth push-in camera through drifting morning fog over mountain valley, distant chimney smoke curling upward. Cinematic, Kodak 35mm grain.",
        "duration": 7.5,
        "fps": 16,
    },
    {
        "id": "shot_02",
        "prompt": "Close-up of a large ornate wooden vintage radio from 1960s Ethiopia, brass dials glowing amber, dust motes floating slowly in golden sunlight beam through a window. Gentle tilt down and slow subtle zoom. Warm cinematic lighting.",
        "duration": 7.0,
        "fps": 16,
    },
    {
        "id": "shot_03",
        "prompt": "Elderly Ethiopian grandfather with gentle wise face, wrinkled dark hands gently turning brass dial knob of a broken radio, shakes head softly with slight sigh. Interior Ethiopian home, warm lamplight. Cinematic close-up.",
        "duration": 7.5,
        "fps": 16,
    },
    {
        "id": "shot_04",
        "prompt": "Ethiopian boy aged 8 with bright curious eyes peeking around a wooden cabinet edge, eyes widening in wonder as warm amber light reflects on his cheeks. 1960s Ethiopia interior. Cinematic shot.",
        "duration": 7.5,
        "fps": 16,
    },
    {
        "id": "shot_05",
        "prompt": "Extreme macro shot of glowing vacuum tube filaments and coiled copper radio wires, thin curl of rosin smoke rising gently. Micro camera tracks slowly across components. Warm amber glow. Cinematic macro.",
        "duration": 7.0,
        "fps": 16,
    },
    {
        "id": "shot_06",
        "prompt": "Young Ethiopian boy's hands carefully lowering a soldering iron tip onto a radio circuit board, molten silver solder droplet flows cleanly onto copper joint, breath held in concentration. Close-up hands. Cinematic.",
        "duration": 8.0,
        "fps": 16,
    },
    {
        "id": "shot_07",
        "prompt": "Hand of Ethiopian boy rotating a radio dial knob, the station needle slides steadily along a glass scale, sudden vibration visible in the cloth speaker, radio crackles back to life. Close-up cinematic shot.",
        "duration": 7.5,
        "fps": 16,
    },
    {
        "id": "shot_08",
        "prompt": "Ethiopian grandfather smiling warmly, embracing his young grandson with deep affection after the radio is repaired. Boy beams with quiet proud smile. 1960s Ethiopian home interior, warm lamplight. Emotional cinematic moment.",
        "duration": 8.0,
        "fps": 16,
    },
    {
        "id": "shot_09",
        "prompt": "Middle-aged Ethiopian man, elder Girma, leaning over a laptop with warm reassuring smile, terminal screen displays flowing green code pipeline logs. Modern office. Camera glides smoothly forward. Cinematic.",
        "duration": 7.5,
        "fps": 16,
    },
    {
        "id": "shot_10",
        "prompt": "Golden Amharic and English text title card glowing on dark background: 'The Legacy of Craft Endures'. Subtle luminous shimmer across text, slow fade to gentle warm black vignette. Cinematic title card.",
        "duration": 7.5,
        "fps": 16,
    },
]

# ── CELL 5: Generate all shots ────────────────────────────────────────────────
# Set this to your keyframes folder path on Kaggle
KEYFRAMES_DIR = "/kaggle/input/heritage-keyframes"   # <-- update if different
OUTPUT_DIR = "/kaggle/working/shots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for shot in SHOTS:
    shot_id = shot["id"]
    keyframe_path = os.path.join(KEYFRAMES_DIR, f"{shot_id}.png")
    output_path = os.path.join(OUTPUT_DIR, f"{shot_id}_wan.mp4")

    if os.path.exists(output_path):
        print(f"[SKIP] {shot_id} already exists")
        continue

    print(f"\n[GENERATING] {shot_id} ...")
    image = Image.open(keyframe_path).convert("RGB").resize((832, 480))

    num_frames = int(shot["duration"] * shot["fps"])
    # Wan requires num_frames = 4k+1
    num_frames = (num_frames // 4) * 4 + 1

    with torch.inference_mode():
        output = pipe(
            image=image,
            prompt=shot["prompt"],
            negative_prompt="blurry, low quality, watermark, text overlay, distorted faces",
            num_frames=num_frames,
            height=480,
            width=832,
            num_inference_steps=25,
            guidance_scale=5.0,
        )

    export_to_video(output.frames[0], output_path, fps=shot["fps"])
    print(f"[✓] Saved: {output_path}")

print("\n[✓] ALL SHOTS GENERATED!")
print("Download all mp4 files from:", OUTPUT_DIR)
print("Then place them in outputs/shots/ on your Mac")
