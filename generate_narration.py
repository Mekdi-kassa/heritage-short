#!/usr/bin/env python3
"""
Generates real Amharic TTS narration for all 10 shots using Gemini 2.5 Flash TTS.
Saves individual WAVs and stitches the full narration_full_track.wav.
"""
import base64, json, math, os, struct, urllib.request, urllib.error, wave
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL   = "gemini-2.5-flash-preview-tts"
URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
SAMPLE_RATE = 24000

SHOTS = [
    {"id": "shot_01", "duration": 7.5,
     "text": "ደሴ ላይ ንጋት የሚጀምረው በጭጋግ እና በቡና ሽታ ብቻ አልነበረም፤ በመንደሩ የሬዲዮ ድምፅ ጭምር እንጂ።"},
    {"id": "shot_02", "duration": 7.0,
     "text": "አባቴ ጊርማ የስምንት ዓመት ልጅ እያለ፣ ያ ትልቅ የእንጨት ሬዲዮ የቤቱ ልብ ነበር።"},
    {"id": "shot_03", "duration": 7.5,
     "text": "አንድ ቀን ምሽት ግን ዜናው ጠፋ። ሬዲዮው ዝም አለ፤ አያቴም በፀጥታው ውስጥ ረጅም የሃሳብ ትንፋሽ ተነፈሰ።"},
    {"id": "shot_04", "duration": 7.5,
     "text": "ግን ጊርማ ዝምታውን እንደ ፍፃሜ ሳይሆን እንደ ሚስጥር ነበር የተመለከተው።"},
    {"id": "shot_05", "duration": 7.0,
     "text": "በመስታወት አምፑሎች እና በተጠላለፉ የመዳብ ሽቦዎች መሃል የተበጠሰች ትንሽ ክር አገኘ።"},
    {"id": "shot_06", "duration": 8.0,
     "text": "ያለ ትምህርት ቤት፣ ያለ ዲፕሎማ፤ በትዕግስት እና በእጅ ንፅህና ብቻ ሽቦዎቹን በሙቀት አጋጠማቸው።"},
    {"id": "shot_07", "duration": 7.5,
     "text": "ቁልፉ ሲዞር… ድንገት ፍንጣቂ ድምፅ ተሰማ፣ ከዚያም ያ ናፍቆት የነበረው የጥላሁን ዘፈን ክፍሉን ሞላው!"},
    {"id": "shot_08", "duration": 8.0,
     "text": "አያቴ ጊርማን አቅፎ እንዲህ አለው፡ 'የተሰበረውን ነገር በጨዋ እጅ የነካ ሰው፣ ሰዎችንም ማዳመጥ ያውቃል'።"},
    {"id": "shot_09", "duration": 7.5,
     "text": "ዛሬ እኛም በኮምፒውተር የምንገነባው የሞዴል ቧንቧ፤ ያኔ አባቴ በደሴ ካገናኘው የመዳብ ሽቦ ፈፅሞ አይለይም።"},
    {"id": "shot_10", "duration": 7.5,
     "text": "የጥበብ ውርስ ይቀጥላል። ይሄ ፊልም በሰው ራዕይ እና በአርቴፊሻል ኢንተለጀንስ ታግዞ የተሰራ ነው።"},
]

AUDIO_DIR = Path("/Users/mac/Desktop/tenx/outputs/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def pcm_to_wav(pcm_bytes: bytes, path: Path, rate: int = SAMPLE_RATE):
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(pcm_bytes)


def pad_or_trim_wav(path: Path, target_sec: float):
    """Ensure WAV is exactly target_sec long."""
    with wave.open(str(path), "rb") as wf:
        rate = wf.getframerate()
        data = wf.readframes(wf.getnframes())
    target_frames = int(rate * target_sec)
    current_frames = len(data) // 2
    if current_frames < target_frames:
        # pad with silence
        data += b"\x00\x00" * (target_frames - current_frames)
    else:
        data = data[:target_frames * 2]
    pcm_to_wav(data, path, rate)


def generate_tts(text: str, shot_id: str) -> bytes:
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {"voiceName": "Charon"}
                }
            }
        }
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        inline = data["candidates"][0]["content"]["parts"][0]["inlineData"]
        mime   = inline.get("mimeType", "")
        audio_bytes = base64.b64decode(inline["data"])
        print(f"  [✓] {shot_id}: got {len(audio_bytes)} bytes  mime={mime}")
        return audio_bytes
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  [✗] {shot_id} HTTP {e.code}: {body[:200]}")
        return None
    except Exception as e:
        print(f"  [✗] {shot_id} error: {e}")
        return None


def stitch_full_track(shot_wavs: list[Path]) -> Path:
    all_frames = bytearray()
    rate = SAMPLE_RATE
    for p in shot_wavs:
        with wave.open(str(p), "rb") as wf:
            rate = wf.getframerate()
            all_frames.extend(wf.readframes(wf.getnframes()))
    out = AUDIO_DIR / "narration_full_track.wav"
    pcm_to_wav(bytes(all_frames), out, rate)
    return out


if __name__ == "__main__":
    print("=" * 55)
    print("  Gemini TTS — Amharic Narration Generator")
    print("=" * 55)

    shot_wavs = []
    for shot in SHOTS:
        sid   = shot["id"]
        text  = shot["text"]
        dur   = shot["duration"]
        out   = AUDIO_DIR / f"narration_{sid}.wav"
        print(f"\n[{sid}] '{text[:40]}...'")

        pcm = generate_tts(text, sid)
        if pcm:
            pcm_to_wav(pcm, out)
            pad_or_trim_wav(out, dur)
            print(f"  → Saved {out.name}")
        else:
            print(f"  → TTS failed; keeping existing file")

        shot_wavs.append(out)

    print("\n[*] Stitching full narration track...")
    full = stitch_full_track(shot_wavs)
    print(f"[✓] Full track: {full}")
    print("\n[✓] Done! Now re-run the render script.")
