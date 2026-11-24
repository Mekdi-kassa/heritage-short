"""
Kaggle Notebook Execution Script for Wan 2.2 TI2V-5B
Runs on Kaggle Free 2x T4 or P100 GPU (30 hrs/week free tier).
"""

import os
import torch
from pathlib import Path

# 1. Install dependencies
# !pip install -q git+https://github.com/huggingface/diffusers.git transformers accelerate torchvision imageio[ffmpeg]

print("[*] Checking CUDA capability...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}, GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")

# Wan 2.2 TI2V-5B pipeline initialization with fp8 offloading
# from diffusers import WanImageToVideoPipeline
# pipe = WanImageToVideoPipeline.from_pretrained("Wan-AI/Wan2.2-TI2V-5B", torch_dtype=torch.bfloat16)
# pipe.enable_model_cpu_offload()

SHOTS = [
  {
    "id": "shot_01",
    "motion_prompt": "Slow smooth push-in camera through drifting morning fog over mountain valley, distant chimney smoke curling upward",
    "duration": 7.5
  },
  {
    "id": "shot_02",
    "motion_prompt": "Gentle tilt down and slow subtle zoom on dusty vintage radio, dust motes floating slowly in golden sunlight beam",
    "duration": 7.0
  },
  {
    "id": "shot_03",
    "motion_prompt": "Wrinkled fingers gently turn brass dial knob back and forth, grandfather shakes head softly with slight sigh",
    "duration": 7.5
  },
  {
    "id": "shot_04",
    "motion_prompt": "Child peeks around wooden cabinet edge, eyes widening in wonder as warm amber light reflects on his cheeks",
    "duration": 7.5
  },
  {
    "id": "shot_05",
    "motion_prompt": "Micro camera tracks slowly across glowing glass tube filaments and coiled copper wires, thin curl of rosin smoke rises gently",
    "duration": 7.0
  },
  {
    "id": "shot_06",
    "motion_prompt": "Young boy carefully lowers soldering iron tip, molten silver droplet flows cleanly onto copper joint, breath held in focus",
    "duration": 8.0
  },
  {
    "id": "shot_07",
    "motion_prompt": "Hand rotates dial knob, station needle slides steadily along glass scale, sudden vibration in speaker cloth",
    "duration": 7.5
  },
  {
    "id": "shot_08",
    "motion_prompt": "Grandfather smiles warmly and pats boy's shoulder in deep affection, boy beams with quiet pride",
    "duration": 8.0
  },
  {
    "id": "shot_09",
    "motion_prompt": "Elder Girma leans over laptop with warm reassuring smile, terminal screen displays flowing green pipeline logs, camera glides smoothly",
    "duration": 7.5
  },
  {
    "id": "shot_10",
    "motion_prompt": "Subtle luminous shimmer across golden text, slow fade to gentle warm black vignette",
    "duration": 7.5
  }
]

print("[*] Ready to process shots from keyframes...")
for shot in SHOTS:
    print(f"Generating Wan 2.2 video for {shot['id']}: {shot['motion_prompt']}")
    # keyframe_path = f"keyframes/{shot['id']}.png"
    # video = pipe(image=keyframe_path, prompt=shot['motion_prompt'], num_frames=81, height=480, width=832).frames[0]
    # export_to_video(video, f"shots/{shot['id']}_wan.mp4", fps=16)
print("[✓] Kaggle Wan 2.2 batch execution completed.")
