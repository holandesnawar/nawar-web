#!/usr/bin/env python3
"""transcript.json for v2: voice-B word alignment (tools/align/a3-v2b.json) mapped onto the placed voiceover.

voiceover.wav file time = master - vo_offset; each take keeps its own shift (audio_v2.json).
A few words the aligner squeezed together are re-timed by hand from the waveform envelope.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = {  # word index → (start, end) in voice-file seconds
    396: (125.95, 126.00), 397: (126.00, 126.05), 398: (126.05, 126.25),       # "de la escuela"
    399: (126.27, 126.31), 400: (126.31, 126.36), 401: (126.36, 126.65),       # "y te responden"
    563: (178.74, 178.86), 564: (178.86, 178.95), 565: (178.95, 179.05),        # "ya lo has"
    566: (179.05, 179.45), 567: (179.65, 180.50), 568: (180.82, 181.20), 569: (181.35, 182.01),  # "probado. Ahora toca hablar."
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
