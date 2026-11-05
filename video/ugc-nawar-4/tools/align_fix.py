#!/usr/bin/env python3
"""Word times for the captions: ElevenLabs Scribe words of the take → tools/align/whisper_p.json ([start, end, word]; the
file keeps the old name the rest of the tools read).

tools/align/scribe_p.json is Scribe's own output (word timestamps) on the take's sound. Scribe's onsets are close, but
at the take's own jump cuts it puts the first word of a phrase too early (into the silence or the cut before it). So the
first word of each phrase (after a gap or a full stop), when its start sits in silence, is moved to where the voice comes
back after the pause (energy 24 dB under the take's speech level for ≥ 80 ms), if there is one 0.15 s before to 0.70 s
after it; the other words stay, only pushed on if they would overlap. MANUAL fixes the ones read off the envelope by hand.
"""
import json, os, subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {"p": ".raw/pedido.mov"}
FIX = {"p": {"ra--": "ra"}}
# (word, Scribe's start) → real start, read off the energy envelope
MANUAL = {"p": {("¿Por", 14.32): 15.12}}
SR, H = 16000, 160                                   # 10 ms frames


def envelope(path):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-af", "highpass=f=100",
                                      "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
    n = len(x) // H
    return 20 * np.log10(np.sqrt((x[:n * H].reshape(n, H) ** 2).mean(1)) + 1e-9)


def onsets(e, quiet, gap):
    """frame times where the voice comes back after ≥ gap quiet frames."""
    out, run = [], 0
    for i, v in enumerate(e):
        if v < quiet:
            run += 1
        else:
            if run >= gap:
                out.append(i * H / SR)
            run = 0
    return out


def scribe_words(take):
    d = json.load(open(os.path.join(ROOT, "tools", "align", f"scribe_{take}.json")))
    return [[w["start"], w["end"], w["text"]] for w in d["words"] if w["type"] == "word"]


def fix_take(take):
    words = []
    for a, b, t in scribe_words(take):
        rep = FIX[take].get(t, t).split(" ")
        for k, r in enumerate(rep):                    # split words share the span
            words.append([a + (b - a) * k / len(rep), a + (b - a) * (k + 1) / len(rep), r])
    e = envelope(os.path.join(ROOT, SRC[take]))
    quiet = float(np.percentile(e[e > -40], 50)) - 24
    ons = onsets(e, quiet=quiet, gap=8)
    out, anchors = [], []
    for i, w in enumerate(words):
        a = w[0]
        first = i == 0 or w[0] - words[i - 1][1] > 0.04 or words[i - 1][2][-1:] in ".,?!"
        fr = int(a * SR / H)
        silent = e[max(0, fr - 2):fr + 3].max() < quiet       # Scribe's start sits in the silence before the voice
        if first and silent:
            near = [o for o in ons if a - 0.15 <= o <= a + 0.70]
            if near:
                o = min(near, key=lambda o: abs(o - a)); anchors.append((w[2], round(a, 2), round(o, 2))); a = o
        a = MANUAL.get(take, {}).get((w[2], round(w[0], 2)), a)
        if out and a < out[-1][0] + 0.06: a = out[-1][0] + 0.06
        out.append([round(a, 3), round(max(w[1], a + 0.06), 3), w[2]])
    json.dump(out, open(os.path.join(ROOT, "tools", "align", f"whisper_{take}.json"), "w"), ensure_ascii=False)
    print(f"take {take}: {len(out)} words, {len(anchors)} anchors: " + " · ".join(f"{t} {a}→{b}" for t, a, b in anchors if abs(a - b) > 0.02))


if __name__ == "__main__":
    for tk in SRC:
        fix_take(tk)
