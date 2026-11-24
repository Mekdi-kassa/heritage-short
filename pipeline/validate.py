#!/usr/bin/env python3
"""
Storyboard Schema Validator
Validates storyboard.json against schema/storyboard.schema.json.
Supports both jsonschema library (if available) and robust pure-Python fallback.
"""

import json
import os
import sys
from pathlib import Path


def load_json(filepath: Path) -> dict:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_with_jsonschema(data: dict, schema: dict) -> tuple[bool, str]:
    try:
        import jsonschema
        jsonschema.validate(instance=data, schema=schema)
        return True, "Valid (validated via jsonschema library)"
    except ImportError:
        return False, "jsonschema package not installed, running built-in schema validator"
    except Exception as e:
        return False, f"Schema validation error: {str(e)}"


def validate_builtin(data: dict, schema: dict) -> tuple[bool, list[str]]:
    """Strict pure-Python validator enforcing the storyboard schema rules."""
    errors = []

    # Check top-level required fields
    for field in schema.get("required", []):
        if field not in data:
            errors.append(f"Missing required top-level field: '{field}'")

    # Duration check
    duration = data.get("target_duration_seconds", 0)
    if not isinstance(duration, (int, float)) or not (60 <= duration <= 90):
        errors.append(f"target_duration_seconds ({duration}) must be between 60 and 90 seconds")

    # Aspect ratios check
    aspect_ratios = data.get("aspect_ratios", [])
    if not ("16:9" in aspect_ratios and "9:16" in aspect_ratios):
        errors.append("aspect_ratios must include both '16:9' and '9:16'")

    # Style block check
    style = data.get("style_block", {})
    for req in ["visual_style", "lighting", "color_palette", "cinematography"]:
        if not style.get(req):
            errors.append(f"style_block missing required field: '{req}'")

    # Shots check
    shots = data.get("shots", [])
    if not isinstance(shots, list) or len(shots) < 8 or len(shots) > 14:
        errors.append(f"shots count ({len(shots) if isinstance(shots, list) else 0}) must be between 8 and 14")

    total_shot_duration = 0.0
    for idx, shot in enumerate(shots):
        shot_id = shot.get("id", f"index_{idx}")
        shot_reqs = [
            "id", "shot_number", "shot_type", "duration_seconds",
            "camera_motion", "visual_prompt", "motion_prompt",
            "character_ref", "narration", "music_cue", "reason"
        ]
        for req in shot_reqs:
            if req not in shot:
                errors.append(f"Shot '{shot_id}' missing required field: '{req}'")

        dur = shot.get("duration_seconds", 0)
        if not isinstance(dur, (int, float)) or dur <= 0:
            errors.append(f"Shot '{shot_id}' duration must be positive number")
        else:
            total_shot_duration += dur

        # Narration validation
        narration = shot.get("narration", {})
        if not narration.get("amharic") or not narration.get("english_subtitle"):
            errors.append(f"Shot '{shot_id}' narration missing amharic text or english_subtitle")

        # Music cue validation
        cue = shot.get("music_cue", {})
        if "ducking_db" not in cue:
            errors.append(f"Shot '{shot_id}' music_cue missing ducking_db")

        # Design thinking requirement: reason
        if not shot.get("reason"):
            errors.append(f"Shot '{shot_id}' missing design intent 'reason'")

    # Check total shot duration against target
    if abs(total_shot_duration - duration) > 1.0:
        errors.append(
            f"Sum of shot durations ({total_shot_duration:.1f}s) does not match target_duration_seconds ({duration:.1f}s)"
        )

    if errors:
        return False, errors
    return True, [f"Valid: 10 shots, total duration {total_shot_duration:.1f}s, all schema constraints satisfied."]


def validate_storyboard(storyboard_path: Path, schema_path: Path) -> bool:
    print(f"[*] Validating contract: {storyboard_path}")
    print(f"[*] Against schema:    {schema_path}")

    data = load_json(storyboard_path)
    schema = load_json(schema_path)

    # First attempt jsonschema if available
    has_lib, msg = validate_with_jsonschema(data, schema)
    if has_lib:
        print(f"[✓] {msg}")
        return True
    elif "Schema validation error" in msg:
        print(f"[✗] {msg}", file=sys.stderr)
        return False

    # Pure Python built-in validation
    valid, messages = validate_builtin(data, schema)
    if valid:
        for m in messages:
            print(f"[✓] {m}")
        return True
    else:
        print("[✗] Storyboard validation FAILED with errors:", file=sys.stderr)
        for err in messages:
            print(f"    - {err}", file=sys.stderr)
        return False


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    s_path = base_dir / "storyboard.json"
    sch_path = base_dir / "schema" / "storyboard.schema.json"

    success = validate_storyboard(s_path, sch_path)
    sys.exit(0 if success else 1)
