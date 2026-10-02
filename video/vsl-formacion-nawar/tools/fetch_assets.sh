#!/usr/bin/env bash
# Rebuild every heavy/derived asset from the owner's shared Google Drive folder, so the repo only
# carries sources. Run from the project root:  bash tools/fetch_assets.sh
# Needs: curl, ffmpeg (with rubberband), python3 + pip (librosa soundfile espeakng-loader scipy pillow), node 22.
set -euo pipefail
cd "$(dirname "$0")/.."
RAW=.raw && mkdir -p "$RAW" assets/audio assets/video assets/img assets/sfx assets/fonts assets/vendor

dl() { curl -sS -L --fail --retry 3 -o "$RAW/$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"; echo "  got $2"; }
echo "downloading from Drive…"
dl 1OBYh_T7NRN6wPoat_WWgWA38609v_98e voz.mp3                 # v1 voice (ElevenLabs «Confident Oct 2 2026», kept for reference)
dl 1y8Xw_5oZKp9jU7SghmwMPW0lCrLt_zVO formacion-cv.mov
dl 1LV7e_Z6ToRQ06TI1ilDc9emNQYtlLyM5 inicio-home.mov
dl 12xQ_z9byuPvWBk0HTyLGM6XBlxnTEuoi clases-video-dentro.mov
dl 13FyLNUjLd0zb1997qyXOUk3X6e2c9PlK consultas-dentro.mov
dl 1U_EeTWKKZ41njGJ-DdQYNZdwil_pVakG material.pdf
dl 1P3ITYqftdRT38geYbVmgyeMxd-pnww43 nawar-wide.png
dl 1BpH4EhH1iNFhOdoDvx65svGZ8027yX2s nawar-square.png


echo "platform recordings → 2560w H.264, silent"
for f in inicio-home formacion-cv clases-video-dentro; do
  ffmpeg -v error -y -i "$RAW/$f.mov" -an -vf "scale=2560:-2:flags=lanczos,fps=30" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -g 30 -movflags +faststart "assets/video/$f.mp4"
done
# consultas: keep only the new-consulta form (7.0–18.6 s); the list/modal parts show student names
ffmpeg -v error -y -ss 7.0 -i "$RAW/consultas-dentro.mov" -t 11.6 -an -vf "scale=2560:-2:flags=lanczos,fps=30" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -g 30 -movflags +faststart assets/video/consulta-nueva.mp4

echo "screenshots from Material.pdf"
mkdir -p "$RAW/mat" && pdfimages -png "$RAW/material.pdf" "$RAW/mat/img"
python3 - <<'EOF'
from PIL import Image, ImageFilter
R = ".raw/mat/img-"
def am(img, mask, out):
    im = Image.open(R + img + ".png").convert("RGB"); a = Image.open(R + mask + ".png").convert("L")
    im.putalpha(a); im.save("assets/img/" + out + ".png")
am("001", "002", "ui-eventos-calendario"); am("003", "004", "ui-consulta-respondida")
am("005", "006", "ui-videoclase-verbos"); am("007", "008", "ui-lezen-texto")
am("012", "013", "web-edificio-nawar"); am("014", "015", "web-hero-aprende")
for src, out in (("000", "ui-curso-desktop"), ("009", "ui-luisteren-audio"), ("010", "ui-curso-desktop-17"), ("011", "ui-curso-movil"), ("016", "web-ebook")):
    Image.open(R + src + ".png").save("assets/img/" + out + ".png")
# blur the student's name in the answered consulta
im = Image.open("assets/img/ui-consulta-respondida.png"); box = (570, 462, 850, 506)
im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(9)), box); im.save("assets/img/ui-consulta-respondida.png")
# logo: tight crop of the transparent wordmark
lg = Image.open(".raw/nawar-wide.png"); lg.crop(lg.split()[-1].getbbox()).save("assets/img/logo-nawar.png")
EOF

echo "fonts + gsap (npm)"
npm i --no-save gsap@3.15.0 @fontsource/poppins @fontsource/inter @fontsource/caveat >/dev/null 2>&1
for w in 500 600 700 800 900; do cp node_modules/@fontsource/poppins/files/poppins-latin-$w-normal.woff2 assets/fonts/; done
cp node_modules/@fontsource/poppins/files/poppins-latin-800-italic.woff2 assets/fonts/
for w in 400 500 600 700 800; do cp node_modules/@fontsource/inter/files/inter-latin-$w-normal.woff2 assets/fonts/; done
cp node_modules/@fontsource/caveat/files/caveat-latin-700-normal.woff2 assets/fonts/
for f in gsap SplitText MotionPathPlugin CustomEase DrawSVGPlugin Flip; do cp node_modules/gsap/dist/$f.min.js assets/vendor/; done

echo "sfx (HyperFrames media-use pack)"
cp ~/.claude/skills/media-use/audio/assets/sfx/*.mp3 assets/sfx/ 2>/dev/null || echo "  (install the hyperframes skills first: npx hyperframes skills)"
ffmpeg -v error -y -i assets/sfx/glitch-1.mp3 -t 0.6 -af "afade=t=out:st=0.42:d=0.18" assets/sfx/glitch-1-short.mp3   # v2: short crack

echo "v2 media (same Drive folder)"
dl 1DeeW7B-n481P_BydJD1D5i76fE30af6Q voz-v2-b.mp3        # voice B (chosen v2 take)
dl 1exOUAXG0zPIZVFJNXh6yB3_Ujf5KXXsQ musica-v2.mp3       # owner's music track
dl 11L-TAspXnce5gh7CaVyiNM-bMTQ3ivXy ejercicios1.mov     # flashcards tool
dl 165i7-clttvPwknNyin2VLeGMJxznXfVo ejercicios2.mov     # «Completa la frase»
dl 17WJmsLyC2i71qv6UgMqGR4oXVYQtIuk1 ejercicios3.jpg     # «Ordena las palabras»
dl 1U2pHBAtkSSAwqHdAbN-tmS-58gHN83vO nuestra-vision.mov  # website hero + vision
ffmpeg -v error -y -i "$RAW/voz-v2-b.mp3" -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -ac 1 "$RAW/voz-v2-b.wav"
ffmpeg -v error -y -i "$RAW/musica-v2.mp3" -ac 2 -ar 44100 "$RAW/music_v2.wav"
ffmpeg -v error -y -i "$RAW/ejercicios1.mov" -an -vf "fps=30,format=yuv420p" -c:v libx264 -preset slow -crf 16 -g 30 -movflags +faststart assets/video/flashcards.mp4
ffmpeg -v error -y -i "$RAW/ejercicios2.mov" -an -vf "fps=30,format=yuv420p" -c:v libx264 -preset slow -crf 16 -g 30 -movflags +faststart assets/video/completa-frase.mp4
ffmpeg -v error -y -i "$RAW/nuestra-vision.mov" -an -vf "fps=30,scale=1722:904,format=yuv420p" -c:v libx264 -preset slow -crf 16 -g 30 -movflags +faststart assets/video/nuestra-vision.mp4
python3 -c "from PIL import Image; Image.open('$RAW/ejercicios3.jpg').convert('RGB').save('assets/img/ui-ordena-palabras.png')"

echo "v2 soundtrack: voice takes + re-edited music + ducking"
python3 tools/build_audio_v2.py
echo "done. Word timings are versioned in transcript.json / timing.json (tools/transcript_v2.py + tools/timing.py)."
