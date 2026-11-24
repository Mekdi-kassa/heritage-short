#!/usr/bin/env python3
"""
Master Orchestrator for The Heritage Short Pipeline.
One-command execution of all 5 stages around the storyboard.json contract:
1. Script & Contract Validation
2. Narration Generation (Amharic TTS) & Subtitle Alignment
3. Keyframes & Character Reference Sheets
4. Moving Shots & Camera Dynamics (Wan 2.2 / FFmpeg)
5. Music Score Synthesis (ACE-Step 1.5)
6. Assembly & Audio Ducking (Radio Cut, 16:9, and 9:16)

Usage:
  python run_pipeline.py --all
  python run_pipeline.py --stage [validate|script|narration|keyframes|shots|music|assemble|radio_cut]
  python run_pipeline.py --shot shot_06
  python run_pipeline.py --clean-cache
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Ensure pipeline package is importable
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pipeline.cache import cache
from pipeline.logger import logger
from pipeline.validate import validate_storyboard
from pipeline.script import run_script_stage
from pipeline.narration import run_narration_stage
from pipeline.keyframes import run_keyframes_stage
from pipeline.shots import run_shots_stage
from pipeline.music import run_music_stage
from pipeline.assemble import run_assembly_stage


def print_banner() -> None:
    print(r"""
========================================================================
    AI-CONTENT GENERATION: THE HERITAGE SHORT PIPELINE
    Story: የደሴው ሬዲዮ ጠጋኝ (The Radio Craftsman of Dessie)
    Contract: storyboard.json | Language: Amharic (አማርኛ)
========================================================================
""")


def main():
    parser = argparse.ArgumentParser(description="The Heritage Short Multi-Model AI Video Studio")
    parser.add_argument("--all", action="store_true", help="Run the entire pipeline end-to-end")
    parser.add_argument("--stage", type=str, choices=["validate", "script", "narration", "keyframes", "shots", "music", "assemble", "radio_cut"], help="Run a specific stage")
    parser.add_argument("--shot", type=str, help="Regenerate a specific shot (e.g. shot_06)")
    parser.add_argument("--clean-cache", action="store_true", help="Wipe .cache manifest to force fresh regeneration")
    parser.add_argument("--target", type=str, default="all", choices=["all", "radio", "final"], help="Assembly target")
    args = parser.parse_args()

    print_banner()

    storyboard_path = BASE_DIR / "storyboard.json"
    schema_path = BASE_DIR / "schema" / "storyboard.schema.json"
    outputs_dir = BASE_DIR / "outputs"

    if args.clean_cache:
        print("[*] Clearing pipeline cache manifest...")
        cache.clear()
        print("[✓] Cache cleared successfully.")
        if not args.all and not args.stage and not args.shot:
            return

    # If shot-specific regeneration requested
    if args.shot:
        shot_id = args.shot.strip()
        print(f"[*] Live Target Regeneration requested for single shot: '{shot_id}'")
        # Invalidate cache for keyframes, narration, shots for this shot
        for stage in ["keyframes", "narration", "shots"]:
            key = cache.get_cache_key(stage, shot_id)
            if key in cache._manifest:
                del cache._manifest[key]
        cache._save_manifest()
        print(f"[✓] Invalidated cache entries for '{shot_id}'. Regenerating...")

        run_keyframes_stage(storyboard_path, outputs_dir)
        run_shots_stage(storyboard_path, outputs_dir)
        run_narration_stage(storyboard_path, outputs_dir)
        run_assembly_stage(storyboard_path, outputs_dir, target="all")
        print(f"\n[✓] Live regeneration complete for {shot_id}. Check outputs/ and runs.jsonl.")
        return

    # Stage-specific execution
    if args.stage:
        stg = args.stage
        if stg == "validate":
            valid = validate_storyboard(storyboard_path, schema_path)
            sys.exit(0 if valid else 1)
        elif stg == "script":
            run_script_stage(storyboard_path, schema_path)
        elif stg == "narration":
            run_narration_stage(storyboard_path, outputs_dir)
        elif stg == "keyframes":
            run_keyframes_stage(storyboard_path, outputs_dir)
        elif stg == "shots":
            run_shots_stage(storyboard_path, outputs_dir)
        elif stg == "music":
            run_music_stage(storyboard_path, outputs_dir)
        elif stg == "radio_cut":
            run_narration_stage(storyboard_path, outputs_dir)
            run_music_stage(storyboard_path, outputs_dir)
            run_assembly_stage(storyboard_path, outputs_dir, target="radio")
        elif stg == "assemble":
            run_assembly_stage(storyboard_path, outputs_dir, target=args.target)
        return

    # Default or --all: Run all stages end to end
    start_total = time.time()
    print("[*] Initiating Complete End-to-End Pipeline Execution...\n")

    # 1. Validation & Script
    run_script_stage(storyboard_path, schema_path)

    # 2. Narration (Amharic TTS) & Subtitle Alignment
    run_narration_stage(storyboard_path, outputs_dir)

    # 3. Keyframes & Character Reference Sheets
    run_keyframes_stage(storyboard_path, outputs_dir)

    # 4. Moving Shots (Wan 2.2 / FFmpeg)
    run_shots_stage(storyboard_path, outputs_dir)

    # 5. Music Score (ACE-Step 1.5)
    run_music_stage(storyboard_path, outputs_dir)

    # 6. Assembly & Audio Ducking
    run_assembly_stage(storyboard_path, outputs_dir, target="all")

    total_latency = time.time() - start_total
    print("\n" + "=" * 70)
    print(f"[✓] PIPELINE EXECUTION COMPLETED IN {total_latency:.2f} SECONDS")
    print(f"[*] Runs Log:    {BASE_DIR / 'runs.jsonl'}")
    print(f"[*] Final Video: {outputs_dir / 'final' / 'heritage_short_16x9.mp4'}")
    print(f"[*] Final Video: {outputs_dir / 'final' / 'heritage_short_9x16.mp4'}")
    print(f"[*] Radio Cut:   {outputs_dir / 'final' / 'radio_cut.mp4'}")
    print("=" * 70)


if __name__ == "__main__":
    main()
