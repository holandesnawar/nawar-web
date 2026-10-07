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
echo "the two takes (Drive folder «Nawar UGC»)"
dl 1GIwAYxytwGszNvRXhA1f3plEfOMMbqoW angle-a.mov   # «Estado de pedido FO5151.mov» — side angle
dl 1Lemr-3lvQuxxuoTdtv04Xz7iPkT8WLUq angle-b.mov   # «Estado de pedido FO5151 (1).mov» — facing camera (hook + CTA)
# HEVC → H.264 for the renderer; light grade; audio cleaned and both takes normalised to −16 LUFS
for t in a b; do
  ffmpeg -v error -y -i "$RAW/angle-$t.mov" \
    -vf "eq=contrast=1.06:saturation=1.10:gamma=0.98,colorbalance=rm=0.025:gm=0.0:bm=-0.025,format=yuv420p" \
    -af "highpass=f=80,afftdn=nr=10:nf=-42,loudnorm=I=-16:TP=-1.5:LRA=11" \
    -c:v libx264 -preset slow -crf 18 -g 15 -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "assets/video/take-$t.mp4"
done

echo "brand + product media from the VSL project"
cp "$VSL/assets/img/logo-nawar.png" assets/img/
cp "$VSL"/assets/fonts/poppins-latin-{600,700,800,900}-normal.woff2 "$VSL"/assets/fonts/inter-latin-{600,700}-normal.woff2 assets/fonts/
cp "$VSL/assets/vendor/gsap.min.js" assets/vendor/
cp "$VSL"/assets/sfx/{whoosh-short,whoosh,pop,click,click-soft,chime,error,glitch-1-short,notification,sparkle,typing}.mp3 assets/sfx/
cp "$VSL"/assets/video/{paul-clase-1,paul-clase-2,completa-frase}.mp4 assets/video/
cp "$VSL/.raw/music_v2.wav" "$RAW/music.wav"
# the real «Próximos eventos» card (two live classes a week apart) from the stitched dashboard page
python3 -c "from PIL import Image; Image.open('$VSL/assets/img/ui-inicio-page.png').crop((18, 1362, 698, 1496)).save('assets/img/ui-eventos-semana.png')"

echo "edit, soundtrack, compositions"
python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high -o renders/nawar-ugc.mp4"
