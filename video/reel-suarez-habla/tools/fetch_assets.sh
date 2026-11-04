#!/usr/bin/env bash
# Rebuilds the reel «Suárez habla neerlandés» from the client's Drive folder, so the repo only carries sources.
# Run from the project root:  bash tools/fetch_assets.sh
# Needs: curl, ffmpeg, python3 (numpy, scipy, pillow, opencv-python-headless<5, onnx, onnxruntime); the ElevenLabs key as
# a network secret (api.elevenlabs.io, header xi-api-key) for the transcript; ../reel-suarez for the upscaler converter.
set -euo pipefail
cd "$(dirname "$0")/.."
RAW=.raw && mkdir -p "$RAW" assets/video assets/fonts assets/vendor
echo "the interview (Drive folder «Luis Suárez»: «Luis Suarez habla Nederlands», 4:17, 1280×720, 25 fps)"
curl -sS -L --fail --retry 3 -o "$RAW/habla.mp4" "https://drive.usercontent.google.com/download?id=1Mqy1DWnBXp7L960UrXfz6x4-fSxtaUnp&export=download&confirm=t"
echo "brand fonts and gsap from the UGC Black Friday project"
cp ../ugc-nawar-bf/assets/fonts/poppins-latin-{700,900}-normal.woff2 ../ugc-nawar-bf/assets/fonts/inter-latin-{600,700}-normal.woff2 assets/fonts/
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
python3 tools/gen.py
echo "done. Then: npx hyperframes check && npx hyperframes render . --quality high --fps 25 -o renders/reel-suarez-habla-v5-tarjeta.mp4"
echo "(the version without the card: python3 tools/gen.py --sin-tarjeta, then render to renders/reel-suarez-habla-v5-solo-subtitulos.mp4)"
