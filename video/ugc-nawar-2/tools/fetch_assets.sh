#!/usr/bin/env bash
# Rebuild every heavy asset of UGC ad #2, so the repo only carries sources. Run from the project root:
#   bash tools/fetch_assets.sh
# Needs: curl, ffmpeg, python3 (numpy, soundfile, pillow). Brand + product media come from the sibling VSL project
# (../vsl-formacion-nawar, after its own `bash tools/fetch_assets.sh`), music included (the VSL track, as in the first UGC).
set -euo pipefail
cd "$(dirname "$0")/.."
VSL=../vsl-formacion-nawar
RAW=.raw && mkdir -p "$RAW" assets/video assets/img assets/sfx assets/fonts assets/vendor assets/audio

dl() { curl -sS -L --fail --retry 3 -o "$RAW/$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"; echo "  got $2"; }
echo "the two takes (Drive folder «Nawar UGC»)"
dl 1gZtlpOoGKgn5jJxu-ie-G76nsutIXDgq pov1.mov   # «UGC.POV1» — facing camera, laptop hook (two hook takes)
dl 1NmzfJmTlzqmVDUoGotW0ZesKxb61eOV- pov2.mov   # «UGC.POV2» — side angle, from «En cuatro semanas»
# take 1: the laptop's HP logo and Intel sticker are blurred (tracked; tools/align/pov1_logo_track.json); light grade;
# audio cleaned and normalised to −16 LUFS — take 2: same grade and audio chain
python3 tools/blur_marks.py "$RAW/pov1.mov" assets/video/take-1.mp4
ffmpeg -v error -y -i "$RAW/pov2.mov" -vf "eq=contrast=1.05:saturation=1.05:gamma=0.98,format=yuv420p" \
  -af "highpass=f=80,afftdn=nr=10:nf=-42,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:v libx264 -preset slow -crf 18 -g 15 -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart assets/video/take-2.mp4
# her last frame (a quiet smile), held under the «haz clic» button at the end
ffmpeg -v error -y -ss 73.95 -i assets/video/take-1.mp4 -frames:v 1 assets/img/take-1-last.png

echo "brand + product media from the VSL project"
cp "$VSL"/assets/img/{logo-nawar,ui-curso-movil,ui-lezen-texto,ui-luisteren-audio}.png assets/img/
cp "$VSL"/assets/fonts/poppins-latin-{600,700,800,900}-normal.woff2 "$VSL"/assets/fonts/inter-latin-{500,600,700}-normal.woff2 assets/fonts/
cp "$VSL/assets/vendor/gsap.min.js" assets/vendor/
cp "$VSL"/assets/sfx/{whoosh-short,pop,click,click-soft,chime,error,notification,ping,sparkle,typing,key-press}.mp3 assets/sfx/
cp "$VSL"/assets/video/{paul-clase-1,paul-clase-2,completa-frase}.mp4 assets/video/   # 2 = lesson video, 1 = live class
cp "$VSL/.raw/music_v2.wav" "$RAW/music.wav"

echo "edit, soundtrack, compositions"
python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high -o renders/nawar-ugc2.mp4"
