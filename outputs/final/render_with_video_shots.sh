#!/bin/bash
# Run this AFTER downloading shot_01_wan.mp4 → shot_10_wan.mp4 from Kaggle
# and placing them in outputs/shots/

SHOTS_DIR='/Users/mac/Desktop/tenx/outputs/shots'
FINAL_DIR='/Users/mac/Desktop/tenx/outputs/final'
AUDIO_DIR='/Users/mac/Desktop/tenx/outputs/audio'
SUBS='/Users/mac/Desktop/tenx/outputs/subtitles/amharic.srt'
FFMPEG='/Users/mac/Downloads/ffmpeg 2'

# Build concat list from real video shots
CONCAT="$FINAL_DIR/shots_concat_video.txt"
> "$CONCAT"
for i in 01 02 03 04 05 06 07 08 09 10; do
    echo "file '$SHOTS_DIR/shot_${i}_wan.mp4'" >> "$CONCAT"
done

echo "[*] Rendering 16x9 with real video shots + Amharic subtitles + narration..."
"$FFMPEG" -y \
  -f concat -safe 0 -i "$CONCAT" \
  -i "$AUDIO_DIR/narration_full_track.wav" \
  -i "$AUDIO_DIR/score_final.wav" \
  -filter_complex "
    [0:v]scale=1920:1080:force_original_aspect_ratio=decrease,
    pad=1920:1080:(ow-iw)/2:(oh-ih)/2,
    subtitles='$SUBS':force_style='FontSize=24,FontName=Arial,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Shadow=1,Alignment=2'[vout];
    [2:a]volume=0.25[music];
    [1:a]aformat=sample_rates=44100:channel_layouts=stereo[narr];
    [music][narr]amix=inputs=2:duration=first[aout]
  " \
  -map '[vout]' -map '[aout]' \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k \
  "$FINAL_DIR/heritage_short_16x9_final.mp4"

echo "[✓] Done! Output: $FINAL_DIR/heritage_short_16x9_final.mp4"
open "$FINAL_DIR"
