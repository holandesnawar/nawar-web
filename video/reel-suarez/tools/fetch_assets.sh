#!/usr/bin/env bash
# Rebuilds the reel «Aprendiendo neerlandés con Luis Suárez» from the client's Drive folder, so the repo only carries
# sources. Run from the project root:  bash tools/fetch_assets.sh
# Needs: curl, ffmpeg, python3 (numpy, scipy, pillow, onnx, onnxruntime); the ElevenLabs key as a network secret
# (api.elevenlabs.io, header xi-api-key) for the transcript.
set -euo pipefail
cd "$(dirname "$0")/.."
RAW=.raw && mkdir -p "$RAW" assets/video assets/fonts assets/vendor
dl() { curl -sS -L --fail --retry 3 -o "$RAW/$2" "https://drive.usercontent.google.com/download?id=$1&export=download&confirm=t"; echo "  got $2"; }
echo "the ad and the client's transcript (Drive folder «Luis Suárez»)"
dl 1SLndkTv7Ni7RvtWoi0uySaJxutWtQc6E suarez.mp4     # «Comercial Geestige Suarez Ajax» (45 s, 512×288, 25 fps)
dl 1sI6ZgY5Zonoyex9jRRADVY2bkliTFrHE suarez.txt     # its transcript, by speaker
echo "brand fonts and gsap from the UGC Black Friday project"
cp ../ugc-nawar-bf/assets/fonts/poppins-latin-{700,800,900}-normal.woff2 ../ugc-nawar-bf/assets/fonts/inter-latin-700-normal.woff2 assets/fonts/
cp ../ugc-nawar-bf/assets/vendor/gsap.min.js assets/vendor/
echo "the transcript with word times (ElevenLabs Scribe)"
ffmpeg -v error -y -i "$RAW/suarez.mp4" -vn -ac 1 -ar 16000 "$RAW/suarez16k.wav"
curl -sS --fail -X POST https://api.elevenlabs.io/v1/speech-to-text -F model_id=scribe_v1 -F language_code=nld \
  -F timestamps_granularity=word -F diarize=true -F "file=@$RAW/suarez16k.wav" -o "$RAW/scribe.json"
echo "the ×4 upscale (Real-ESRGAN general-x4v3, ONNX on CPU, ~20 min)"
curl -sS -L --fail -o "$RAW/realesr-general-x4v3.pth" https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth
python3 tools/esrgan_onnx.py "$RAW/realesr-general-x4v3.pth" "$RAW/esrgan-x4v3.onnx"
python3 tools/upscale.py 123 993
python3 tools/frame.py
python3 tools/subs.py
python3 tools/emoji.py
python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high --fps 25 -o renders/reel-suarez-v1.mp4"
