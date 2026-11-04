#!/usr/bin/env bash
# Rebuilds the reel «Suárez habla neerlandés» from the client's Drive folder, so the repo only carries sources.
# Run from the project root:  bash tools/fetch_assets.sh
# Needs: curl, ffmpeg (with libvpx), node + playwright, python3 (numpy, scipy, pillow, soundfile, opencv-python-headless<5, onnx,
# onnxruntime); the ElevenLabs key as
# a network secret (api.elevenlabs.io, header xi-api-key) for the transcript and the voice-over; ../reel-suarez for the
# upscaler converter; ../ugc-nawar-bf for the fonts, gsap and the whoosh.
set -euo pipefail
cd "$(dirname "$0")/.."
RAW=.raw && mkdir -p "$RAW" assets/video assets/fonts assets/vendor
echo "the interview (Drive folder «Luis Suárez»: «Luis Suarez habla Nederlands», 4:17, 1280×720, 25 fps)"
curl -sS -L --fail --retry 3 -o "$RAW/habla.mp4" "https://drive.usercontent.google.com/download?id=1Mqy1DWnBXp7L960UrXfz6x4-fSxtaUnp&export=download&confirm=t"
echo "brand fonts and gsap from the UGC Black Friday project"
cp ../ugc-nawar-bf/assets/fonts/poppins-latin-{700,800,900}-normal.woff2 ../ugc-nawar-bf/assets/fonts/inter-latin-{600,700}-normal.woff2 assets/fonts/
cp ../ugc-nawar-bf/assets/vendor/gsap.min.js assets/vendor/
echo "the transcript with word times (ElevenLabs Scribe, and a second pass to check it)"
ffmpeg -v error -y -i "$RAW/habla.mp4" -vn -ac 1 -ar 16000 "$RAW/habla16k.wav"
curl -sS --fail -X POST https://api.elevenlabs.io/v1/speech-to-text -F model_id=scribe_v2 -F timestamps_granularity=word \
  -F diarize=true -F "file=@$RAW/habla16k.wav" -o "$RAW/scribe.json"
curl -sS --fail -X POST https://api.elevenlabs.io/v1/speech-to-text -F model_id=scribe_v1 -F language_code=nld \
  -F timestamps_granularity=word -F diarize=true -F "file=@$RAW/habla16k.wav" -o "$RAW/scribe_v1.json"
echo "the upscaler (Real-ESRGAN general-x4v3 → ONNX, without running its pickle)"
curl -sS -L --fail -o "$RAW/realesr-general-x4v3.pth" https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth
python3 ../reel-suarez/tools/esrgan_onnx.py "$RAW/realesr-general-x4v3.pth" "$RAW/esrgan-x4v3.onnx"
echo "the face detector (YuNet, OpenCV Zoo)"
curl -sS -L --fail -o "$RAW/yunet.onnx" https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
python3 tools/frame.py --track
python3 tools/frame.py          # ~1.5 h on CPU
python3 tools/subs.py
echo "the closing ad: the ebook animation («Animación libro interactivo.html», folder «MARIO»), the BF ad's music and effects, the voice-over"
mkdir -p "$RAW/outro"
curl -sS -L --fail --retry 3 -o "$RAW/outro/libro.html" "https://drive.usercontent.google.com/download?id=1Hl0djiY93k8BA3-BdPS8rPrn6SbmbSL8&export=download&confirm=t"
curl -sS -L --fail --retry 3 -o "$RAW/outro/music.mp3" "https://drive.usercontent.google.com/download?id=1iMcSFRAOoly8OG6jDt3ENBwSntuhA8FL&export=download&confirm=t"
cp ../ugc-nawar-bf/assets/sfx/whoosh-short.mp3 "$RAW/outro/whoosh.mp3"
for f in pop click ping; do cp "../ugc-nawar-bf/assets/sfx/$f.mp3" "$RAW/outro/$f.mp3"; done
echo "Inter (variable, for the hook's ExtraBold and the ad) from the Black Friday page itself"
curl -sS -L --fail --retry 3 -o assets/fonts/inter-var-latin.woff2 "https://blackfriday.holandesnawar.com/fonts/inter-latin.woff2"
# the voice-over is not versioned (only its words and times, outro.json): a new take is generated if it is missing,
# and outro.json is rewritten with its times
[ -f "$RAW/outro/voz.mp3" ] || python3 tools/outro.py voz
python3 tools/outro.py libro
python3 tools/outro.py audio
python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high --fps 25 -o renders/reel-suarez-habla-v7-2.mp4"
