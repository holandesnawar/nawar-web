#!/usr/bin/env bash
# Rebuild every heavy asset of UGC ad #4 («Nuestro Black Friday empieza hoy»), so the repo only carries sources. Run from
# the project root:
#   bash tools/fetch_assets.sh
# Needs: curl, ffmpeg, python3 (numpy, scipy, soundfile, pillow). Brand media come from the sibling VSL project
# (../vsl-formacion-nawar, after its own `bash tools/fetch_assets.sh`); the music is the client's own track (Drive).
set -euo pipefail
cd "$(dirname "$0")/.."
VSL=../vsl-formacion-nawar
RAW=.raw && mkdir -p "$RAW" assets/video assets/img assets/sfx assets/fonts assets/vendor assets/audio

dl() { curl -sS -L --fail --retry 3 -o "$RAW/$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"; echo "  got $2"; }
echo "v2: the client's cut and the website recording (Drive «BF 2»), the ebook animation, the calm VSL music, two stock clips"
dl 1ICfGZcfKjO_ka9FffpNE15w88yu1DFvR cortado.mp4  # «Cortado BF2 Video.mp4» — the client's own cut of the ad (60 fps)
dl 1kI-Hx921ioe0ocrZs0ORYR6TIgh5XGHc web.mov      # «Grabación de pantalla 2026-11-06…» — the priority-list page, scrolled
dl 1NEbiZ-7Hp1LeORMbohAwvFKGnfPhu7h0 libro2.mp4   # «Animación Libro» — the ebook «Holandés sin miedo» on black (7 s)
# v3: Mixkit (free license): three 4K clips — «People having a work meeting around a
# table», «Two coworkers talking and laughing», «Couple of friends chatting during Christmas dinner»
dl 1iMcSFRAOoly8OG6jDt3ENBwSntuhA8FL music.mp3    # v4: «musica v1» — the client's track (UGC #2), shaped to the script in build_audio.py
for i in 4547 4872 42157; do curl -sS -L --fail -o "$RAW/stock-$i.mp4" "https://assets.mixkit.co/videos/$i/$i-2160.mp4"; done
# the cut: 60 → 30 fps, light grade; audio cleaned and normalised to −16 LUFS
ffmpeg -v error -y -i "$RAW/cortado.mp4" -vf "fps=30,eq=contrast=1.05:saturation=1.05:gamma=0.98,format=yuv420p" \
  -af "highpass=f=80,afftdn=nr=10:nf=-42,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:v libx264 -preset slow -crf 18 -g 15 -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart assets/video/take-c.mp4
# the stock clips, cut and cropped to 9:16 from 4K: (clip, from, length, crop x, name)
for c in "4547 6.5 3.5 420 stock-table" "4872 5.2 4.0 2080 stock-laugh" "42157 0.0 4.5 1500 stock-xmas"; do set -- $c
  ffmpeg -v error -y -ss $2 -t $3 -i "$RAW/stock-$1.mp4" -vf "crop=1215:2160:$4:0,scale=1080:1920:flags=lanczos,fps=30,eq=contrast=1.04:saturation=1.05,format=yuv420p" \
    -an -c:v libx264 -preset slow -crf 18 -g 15 -movflags +faststart "assets/video/$5.mp4"
done
# the website recording (394×852 at 75 fps) → 462×1000 at 30 fps, silent
ffmpeg -v error -y -i "$RAW/web.mov" -vf "fps=30,scale=462:1000:flags=lanczos,format=yuv420p" -an -c:v libx264 -preset slow -crf 16 -g 15 \
  -movflags +faststart assets/video/web.mp4
# and the same page blurred and darker, full frame, behind the phone
ffmpeg -v error -y -i assets/video/web.mp4 -vf "scale=1080:-2:flags=bicubic,crop=1080:1920:0:(ih-1920)/2,boxblur=30:2,eq=brightness=-0.18:saturation=1.1,format=yuv420p" \
  -an -c:v libx264 -preset medium -crf 22 -g 15 -movflags +faststart assets/video/web-bg.mp4

echo "brand media from the VSL project"
cp "$VSL"/assets/img/logo-nawar.png assets/img/
cp "$VSL"/assets/fonts/poppins-latin-{600,700,800,900}-normal.woff2 "$VSL"/assets/fonts/inter-latin-{500,600,700}-normal.woff2 assets/fonts/
cp "$VSL/assets/vendor/gsap.min.js" assets/vendor/
cp "$VSL"/assets/sfx/{whoosh,whoosh-short,pop,click,click-soft,chime,error,notification,ping,sparkle,typing,key-press}.mp3 assets/sfx/
python3 tools/sfx_impact.py      # the page turn of the ebook (synthesised)

echo "word times, edit, ebook clip, soundtrack, compositions"
python3 tools/align_fix.py && python3 tools/edit.py && python3 tools/libro_clip.py && python3 tools/build_audio.py
python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high -o renders/nawar-ugc4-v4.mp4"
