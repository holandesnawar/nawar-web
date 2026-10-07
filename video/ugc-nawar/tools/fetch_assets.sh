#!/usr/bin/env bash
# Rebuild every heavy asset of the UGC ad, so the repo only carries sources. Run from the project root:
#   bash tools/fetch_assets.sh
# Needs: curl, ffmpeg, python3 (numpy, soundfile, pillow). Brand + product media come from the sibling VSL project
# (../vsl-formacion-nawar, after its own `bash tools/fetch_assets.sh`).
set -euo pipefail
cd "$(dirname "$0")/.."
VSL=../vsl-formacion-nawar
RAW=.raw && mkdir -p "$RAW" assets/video assets/img assets/sfx assets/fonts assets/vendor assets/audio

dl() { curl -sS -L --fail --retry 3 -o "$RAW/$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"; echo "  got $2"; }
echo "the take facing camera (Drive folder «Nawar UGC»)"
# v2 uses only take B (she talks to camera the whole ad). Take A, the side angle, was v1's second camera:
#   dl 1GIwAYxytwGszNvRXhA1f3plEfOMMbqoW angle-a.mov   # «Estado de pedido FO5151.mov»
dl 1Lemr-3lvQuxxuoTdtv04Xz7iPkT8WLUq angle-b.mov   # «Estado de pedido FO5151 (1).mov»
# HEVC → H.264 for the renderer; light grade; audio cleaned and normalised to −16 LUFS
for t in b; do
  ffmpeg -v error -y -i "$RAW/angle-$t.mov" \
    -vf "eq=contrast=1.06:saturation=1.10:gamma=0.98,colorbalance=rm=0.025:gm=0.0:bm=-0.025,format=yuv420p" \
    -af "highpass=f=80,afftdn=nr=10:nf=-42,loudnorm=I=-16:TP=-1.5:LRA=11" \
    -c:v libx264 -preset slow -crf 18 -g 15 -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "assets/video/take-$t.mp4"
done

echo "brand + product media from the VSL project"
cp "$VSL"/assets/img/{logo-nawar,ui-curso-movil,ui-lezen-texto,ui-luisteren-audio}.png assets/img/
cp "$VSL"/assets/fonts/poppins-latin-{600,700,800,900}-normal.woff2 "$VSL"/assets/fonts/inter-latin-{500,600,700}-normal.woff2 assets/fonts/
cp "$VSL/assets/vendor/gsap.min.js" assets/vendor/
cp "$VSL"/assets/sfx/{whoosh-short,pop,click,click-soft,chime,error,notification,ping,typing,key-press}.mp3 assets/sfx/
cp "$VSL"/assets/video/{paul-clase-1,completa-frase,clases-video-dentro}.mp4 assets/video/
cp "$VSL/.raw/music_v2.wav" "$RAW/music.wav"

echo "edit, soundtrack, compositions"
python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high -o renders/nawar-ugc-v2.mp4"
