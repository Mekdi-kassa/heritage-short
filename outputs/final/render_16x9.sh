#!/bin/bash
FFMPEG='/Users/mac/Downloads/ffmpeg 2'
KF='/Users/mac/Desktop/tenx/outputs/keyframes'
AUDIO='/Users/mac/Desktop/tenx/outputs/audio'
SUBS='/Users/mac/Desktop/tenx/outputs/subtitles/amharic.srt'
OUT='/Users/mac/Desktop/tenx/outputs/final/heritage_short_16x9.mp4'

"$FFMPEG" -y \
  -i "$KF/shot_01.png" \
  -i "$KF/shot_02.png" \
  -i "$KF/shot_03.png" \
  -i "$KF/shot_04.png" \
  -i "$KF/shot_05.png" \
  -i "$KF/shot_06.png" \
  -i "$KF/shot_07.png" \
  -i "$KF/shot_08.png" \
  -i "$KF/shot_09.png" \
  -i "$KF/shot_10.png" \
  -i "$AUDIO/narration_full_track.wav" \
  -i "$AUDIO/score_final.wav" \
  -filter_complex "
    [0:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=188:s=1920x1080:fps=25,setsar=1[v0];
    [1:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=175:s=1920x1080:fps=25,setsar=1[v1];
    [2:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=187:s=1920x1080:fps=25,setsar=1[v2];
    [3:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=188:s=1920x1080:fps=25,setsar=1[v3];
    [4:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=175:s=1920x1080:fps=25,setsar=1[v4];
    [5:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=200:s=1920x1080:fps=25,setsar=1[v5];
    [6:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=187:s=1920x1080:fps=25,setsar=1[v6];
    [7:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=200:s=1920x1080:fps=25,setsar=1[v7];
    [8:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=188:s=1920x1080:fps=25,setsar=1[v8];
    [9:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,zoompan=z='min(zoom+0.0003,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=187:s=1920x1080:fps=25,setsar=1[v9];
    [v0][v1][v2][v3][v4][v5][v6][v7][v8][v9]concat=n=10:v=1:a=0,subtitles='$SUBS':force_style='FontSize=22,FontName=Kefa,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Shadow=1,Alignment=2'[vout];
    [10:a]aresample=44100,aformat=channel_layouts=stereo,volume=2.0[narr];
    [11:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.2[music];
    [narr][music]amix=inputs=2:duration=first:weights=4 1[aout]
  " \
  -map '[vout]' -map '[aout]' \
  -c:v libx264 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$OUT"
