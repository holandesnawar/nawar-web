#!/usr/bin/env bash
# Rebuild every heavy asset of the UGC Black Friday ad, so the repo only carries sources. Run from the project root:
#   bash tools/fetch_assets.sh
# Needs: curl, ffmpeg, python3 (numpy, scipy, soundfile, onnxruntime). Brand media come from the sibling VSL project
# (../vsl-formacion-nawar, after its own `bash tools/fetch_assets.sh`); the music is the client's own track (Drive).
set -euo pipefail
cd "$(dirname "$0")/.."
VSL=../vsl-formacion-nawar
RAW=.raw && mkdir -p "$RAW" assets/video assets/img assets/sfx assets/fonts assets/vendor assets/audio

dl() { curl -sS -L --fail --retry 3 -o "$RAW/$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"; echo "  got $2"; }
echo "the takes (Drive folder «PEDIDO 4 CLAUDE») and the music"
dl 1ucWR3IIv8ifqdK4HcUyi9Qzl1yPefi6r gancho.mov   # «intro gancho» — three hook variants; this version uses «Si vives…» (17.6 s)
dl 1GRe7vt-ynrdU8RQHu4wbpll2zjmUv7G- pedido.mov   # «Estado de pedido FO4233CD» — the body
dl 1iMcSFRAOoly8OG6jDt3ENBwSntuhA8FL music.mp3    # «musica v1» — the client's background track (ElevenLabs)
dl 1NEbiZ-7Hp1LeORMbohAwvFKGnfPhu7h0 libro2.mp4   # «Animación Libro» — the ebook «Holandés sin miedo» on black (7 s, v5)
# both takes: HEVC → H.264, light grade; audio cleaned and normalised to −16 LUFS
for t in g:gancho p:pedido; do
  ffmpeg -v error -y -i "$RAW/${t#*:}.mov" -vf "eq=contrast=1.05:saturation=1.05:gamma=0.98,format=yuv420p" \
    -af "highpass=f=80,afftdn=nr=10:nf=-42,loudnorm=I=-16:TP=-1.5:LRA=11" \
    -c:v libx264 -preset slow -crf 18 -g 15 -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "assets/video/take-${t%%:*}.mp4"
done

echo "brand media from the VSL project"
cp "$VSL"/assets/img/logo-nawar.png assets/img/
cp "$VSL"/assets/fonts/poppins-latin-{600,700,800,900}-normal.woff2 "$VSL"/assets/fonts/inter-latin-{500,600,700}-normal.woff2 assets/fonts/
cp "$VSL/assets/vendor/gsap.min.js" assets/vendor/
cp "$VSL"/assets/sfx/{whoosh,whoosh-short,glitch-1-short,pop,click,click-soft,chime,error,notification,ping,sparkle,typing,key-press}.mp3 assets/sfx/
python3 tools/sfx_impact.py      # the Black Friday hit and the page turn (synthesised)

echo "word times, edit, soundtrack, compositions"
python3 tools/align_fix.py && python3 tools/edit.py && python3 tools/libro_clip.py && python3 tools/build_audio.py
echo "the girl cut out for the Black Friday backdrops (a few minutes on CPU)"
python3 tools/mattes.py
python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high -o renders/nawar-ugc-bf-v6-4.mp4"
