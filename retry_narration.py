#!/usr/bin/env python3
"""Retry TTS generation for shots 07, 08, 10 with rate-limit delays."""
import base64, json, os, time, urllib.request, urllib.error, wave
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL   = "gemini-2.5-flash-preview-tts"
URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
SAMPLE_RATE = 24000
AUDIO_DIR = Path("/Users/mac/Desktop/tenx/outputs/audio")

RETRY_SHOTS = [
    {"id": "shot_07", "duration": 7.5,
     "text": "ቁልፉ ሲዞር… ድንገት ፍንጣቂ ድምፅ ተሰማ፣ ከዚያም ያ ናፍቆት የነበረው የጥላሁን ዘፈን ክፍሉን ሞላው!"},
    {"id": "shot_08", "duration": 8.0,
     "text": "አያቴ ጊርማን አቅፎ እንዲህ አለው፡ 'የተሰበረውን ነገር በጨዋ እጅ የነካ ሰው፣ ሰዎችንም ማዳመጥ ያውቃል'።"},
    {"id": "shot_10", "duration": 7.5,
     "text": "የጥበብ ውርስ ይቀጥላል። ይሄ ፊልም በሰው ራዕይ እና በአርቴፊሻል ኢንተለጀንስ ታግዞ የተሰራ ነው።"},
]

ALL_SHOT_IDS = [f"shot_{i:02d}" for i in range(1, 11)]

def pcm_to_wav(pcm_bytes, path, rate=SAMPLE_RATE):
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate)
        wf.writeframes(pcm_bytes)

def pad_or_trim(path, target_sec):
    with wave.open(str(path), "rb") as wf:
        rate = wf.getframerate(); data = wf.readframes(wf.getnframes())
    target = int(rate * target_sec) * 2
    data = data[:target] if len(data) > target else data + b"\x00\x00" * ((target - len(data)) // 2)
    pcm_to_wav(data, path, rate)

def tts(text, shot_id):
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Charon"}}}
        }
    }
    for attempt in range(4):
        wait = 15 * (attempt + 1)
        try:
            req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode())
            inline = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            audio  = base64.b64decode(inline["data"])
            print(f"  [✓] {shot_id}: {len(audio)} bytes")
            return audio
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            print(f"  [attempt {attempt+1}] HTTP {e.code} — waiting {wait}s...")
            time.sleep(wait)
        except Exception as e:
            print(f"  [attempt {attempt+1}] error: {e} — waiting {wait}s...")
            time.sleep(wait)
    return None

print("Retrying shots 07, 08, 10 with delays...\n")
for shot in RETRY_SHOTS:
    sid, dur, text = shot["id"], shot["duration"], shot["text"]
    print(f"\n[{sid}] '{text[:50]}...'")
    time.sleep(10)  # pause before each request
    pcm = tts(text, sid)
    if pcm:
        out = AUDIO_DIR / f"narration_{sid}.wav"
        pcm_to_wav(pcm, out)
        pad_or_trim(out, dur)
        print(f"  → Saved {out.name}")

# Stitch full track in correct shot order
print("\n[*] Re-stitching full narration track...")
all_frames = bytearray()
rate = SAMPLE_RATE
for sid in ALL_SHOT_IDS:
    p = AUDIO_DIR / f"narration_{sid}.wav"
    with wave.open(str(p), "rb") as wf:
        rate = wf.getframerate()
        all_frames.extend(wf.readframes(wf.getnframes()))

out = AUDIO_DIR / "narration_full_track.wav"
pcm_to_wav(bytes(all_frames), out, rate)
print(f"[✓] Full track saved: {out}")
print("[✓] All done! Run the render script now.")
