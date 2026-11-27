#!/usr/bin/env python3
"""
Pure-Python Broadcast Audio Mixing & Sidechain Ducking Engine.
Zero external dependencies. Uses standard library wave, struct, and math.
Mixes narration voice track with background musical score:
- Applies sidechain ducking (reduces score volume by -8 dB during narration with smooth attack/release)
- Normalizes peak amplitude to prevent clipping (-1.0 dB true peak target)
- Outputs standard 44.1 kHz 16-bit stereo master WAV
"""

import math
import struct
import wave
from pathlib import Path


def mix_and_duck_audio(
    voice_wav_path: Path,
    score_wav_path: Path,
    output_wav_path: Path,
    total_duration_sec: float = 75.0,
    ducking_db: float = -8.0,
    attack_ms: float = 250.0,
    release_ms: float = 1400.0
) -> Path:
    target_sr = 44100
    total_samples = int(total_duration_sec * target_sr)
    output_wav_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Load voice track
    voice_samples = [0.0] * total_samples
    if voice_wav_path.exists():
        with wave.open(str(voice_wav_path), "rb") as wf:
            n_ch = wf.getnchannels()
            sw = wf.getsampwidth()
            in_sr = wf.getframerate()
            raw = wf.readframes(wf.getnframes())

            fmt = "<h" if sw == 2 else "<b"
            step = sw * n_ch
            n_frames = len(raw) // step

            for i in range(min(total_samples, int(n_frames * (target_sr / in_sr)))):
                orig_idx = int(i * (in_sr / target_sr))
                if orig_idx < n_frames:
                    val = struct.unpack_from(fmt, raw, orig_idx * step)[0]
                    # Normalize to -1.0 .. 1.0
                    voice_samples[i] = val / 32768.0

    # 2. Load score track
    score_samples_l = [0.0] * total_samples
    score_samples_r = [0.0] * total_samples
    if score_wav_path.exists():
        with wave.open(str(score_wav_path), "rb") as wf:
            n_ch = wf.getnchannels()
            sw = wf.getsampwidth()
            in_sr = wf.getframerate()
            raw = wf.readframes(wf.getnframes())

            fmt = "<h" if sw == 2 else "<b"
            step = sw * n_ch
            n_frames = len(raw) // step

            for i in range(min(total_samples, int(n_frames * (target_sr / in_sr)))):
                orig_idx = int(i * (in_sr / target_sr))
                if orig_idx < n_frames:
                    val_l = struct.unpack_from(fmt, raw, orig_idx * step)[0]
                    val_r = struct.unpack_from(fmt, raw, orig_idx * step + (sw if n_ch > 1 else 0))[0]
                    score_samples_l[i] = val_l / 32768.0
                    score_samples_r[i] = val_r / 32768.0

    # 3. Sidechain compression / ducking
    duck_gain = 10.0 ** (ducking_db / 20.0)  # ~0.398 for -8dB
    attack_samples = max(1, int(attack_ms * 0.001 * target_sr))
    release_samples = max(1, int(release_ms * 0.001 * target_sr))

    current_gain = 1.0
    out_l = [0.0] * total_samples
    out_r = [0.0] * total_samples

    # Compute RMS envelope of voice
    window = int(0.02 * target_sr)  # 20ms window
    voice_rms = [0.0] * total_samples

    running_sum = 0.0
    for i in range(total_samples):
        running_sum += voice_samples[i] * voice_samples[i]
        if i >= window:
            running_sum -= voice_samples[i - window] * voice_samples[i - window]
        voice_rms[i] = math.sqrt(max(0.0, running_sum / window))

    for i in range(total_samples):
        # Voice active threshold
        is_speaking = voice_rms[i] > 0.015

        target_gain = duck_gain if is_speaking else 1.0

        if target_gain < current_gain:
            # Attack (ducking down)
            current_gain -= (1.0 - duck_gain) / attack_samples
            current_gain = max(duck_gain, current_gain)
        else:
            # Release (swelling back up)
            current_gain += (1.0 - duck_gain) / release_samples
            current_gain = min(1.0, current_gain)

        # Mix voice and ducked score
        mix_l = voice_samples[i] * 1.05 + score_samples_l[i] * current_gain
        mix_r = voice_samples[i] * 1.05 + score_samples_r[i] * current_gain

        out_l[i] = mix_l
        out_r[i] = mix_r

    # 4. Master volume normalization (-1.0 dB true peak target)
    max_peak = max(max(abs(x) for x in out_l), max(abs(x) for x in out_r), 0.001)
    norm_factor = 0.89 / max_peak if max_peak > 0.89 else 0.95

    # 5. Write master output WAV
    with wave.open(str(output_wav_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(target_sr)

        raw_out = bytearray()
        for i in range(total_samples):
            val_l = int(max(-32767, min(32767, out_l[i] * norm_factor * 32767)))
            val_r = int(max(-32767, min(32767, out_r[i] * norm_factor * 32767)))
            raw_out.extend(struct.pack("<hh", val_l, val_r))

        wf.writeframes(raw_out)

    print(f"[✓] Pure-Python Audio DSP: Mixed & ducked master track -> {output_wav_path}")
    return output_wav_path


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    mix_and_duck_audio(
        base / "outputs" / "audio" / "narration_full_track.wav",
        base / "outputs" / "audio" / "score_final.wav",
        base / "outputs" / "audio" / "master_soundtrack_ducked.wav"
    )
