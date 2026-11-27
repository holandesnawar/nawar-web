#!/usr/bin/env python3
"""transcript.json for v2: voice-B word alignment (tools/align/a3-v2b.json) mapped onto the placed voiceover.

voiceover.wav file time = master - vo_offset; each take keeps its own shift (audio_v2.json).
A few words the aligner squeezed together are re-timed by hand from the waveform envelope.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = {  # word index → (start, end) in voice-file seconds; checked against word-level Whisper (bias-corrected) + the envelope
    194: (57.20, 57.70),                                                        # "exactamente"
    395: (125.72, 126.00), 396: (126.00, 126.08), 397: (126.08, 126.18), 398: (126.18, 126.65),  # "dentro de la escuela"
    399: (126.84, 126.92), 400: (126.92, 127.05), 401: (127.20, 127.63),       # "y te responden."
    402: (127.97, 128.10), 403: (128.12, 128.50), 404: (128.56, 128.70), 405: (128.72, 128.86),
    406: (128.88, 129.25), 407: (129.28, 129.75),                               # "Tus dudas no se quedan esperando."
    443: (139.58, 139.83),                                                      # "saben"
    561: (178.88, 179.18), 562: (179.20, 179.45), 563: (179.66, 179.80), 564: (179.82, 179.90),
    565: (179.92, 180.08), 566: (180.10, 180.50),                               # "algún día … ya lo has probado."
    567: (180.85, 181.20), 568: (181.30, 181.55), 569: (181.60, 182.01),        # "Ahora toca hablar."
}
def main():
    plan = json.load(open(os.path.join(ROOT, "audio_v2.json")))
    words = json.load(open(os.path.join(ROOT, "tools", "align", "a3-v2b.json")))["words"]
    off = plan["vo_offset"]; out = []
    for i, w in enumerate(words):
        s, e = FIX.get(i, (w["start"], w["end"]))
        seg = next(g for g in plan["segments"] if g["from"] <= s < g["to"])
        p = w["punct"].replace("¿", "").replace("¡", "").strip()
        out.append({"id": f"w{i}", "text": w["text"], "start": round(s + seg["shift"] - off, 3),
                    "end": round(e + seg["shift"] - off, 3), "punct": p[:1] if p else ""})
    json.dump(out, open(os.path.join(ROOT, "transcript.json"), "w"), ensure_ascii=False, indent=1)
    print(len(out), "words; last ends", out[-1]["end"] + off, "master")
if __name__ == "__main__":
    main()
