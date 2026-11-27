#!/usr/bin/env python3
"""Word times for the captions: Whisper (small, multilingual) words of each take → tools/align/whisper_<take>.json.

tools/align/raw_<take>.json is Whisper's own output ([start, end, word]); its onsets drift by up to ±0.35 s on these
takes, and it mishears a few words. This fixes the text (FIX: candidates scored against the audio with Whisper itself)
and the one timing error that matters: Whisper puts the first word of a phrase too early (by up to 0.35 s at the start
of a take) while the words after it are right. So the first word of each phrase (after a gap or a full stop) is moved
to where the voice comes back after the pause (energy 24 dB under the take's speech level for ≥ 80 ms), if there is
one 0.15 s before to 0.45 s after it; the other words stay, only pushed on if they would overlap.
"""
import json, os, subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {"g": ".raw/gancho.mov", "p": ".raw/pedido.mov"}
# (take, index in raw, replacement words) — «impractical» is «sin practicar», «pedircita» is two words…
FIX = {"g": {"ves": "vives", "países": "Países", "bajos.": "Bajos.", "bajos": "Bajos"},
       "p": {"pedircita": "pedir cita", "impractical.": "sin practicar.", "senidos": "sonidos", "cambien": "cambian",
             "como": "cómo"}}
# first words the onset rule can't reach (no pause before them: the take's own jump cut removed it, or room noise
# before the first word), read off the energy envelope by hand: (word, Whisper's start) → real start
MANUAL = {"p": {("Antes", 0.74): 1.00, ("algo", 5.48): 5.70, ("algo", 12.74): 12.94,
               # phrase starts after a short pause inside Whisper's previous word (its words touch, so the gap rule above
               # misses them), measured on the envelope and checked with forced alignment (QA of v1)
               ("la", 4.72): 5.01, ("cada", 16.94): 17.21, ("tú", 18.48): 18.69, ("porque", 21.74): 21.88,
               ("este", 25.64): 25.85, ("para", 28.12): 28.41, ("con", 29.04): 29.27, ("y", 44.46): 44.83,
               # words inside a phrase that Whisper starts in the previous word's final consonant or a short pause (QA of
               # v2: silences, bursts and fricatives read off spectrograms)
               ("puede", 2.40): 2.60, ("por", 18.02): 18.22, ("es", 21.18): 21.38, ("casi", 21.98): 22.12,
               ("todo", 22.26): 22.48, ("está", 23.34): 23.52, ("creado", 25.08): 25.28, ("70", 26.58): 26.74,
               ("páginas", 27.02): 27.24, ("prácticos", 31.34): 31.53, ("cómo", 32.00): 32.23, ("por", 33.60): 33.95,
               ("que", 34.22): 34.36, ("cuando", 35.28): 35.54, ("por", 37.08): 37.28, ("un", 37.40): 37.58,
               ("euro", 37.72): 37.87, ("solo", 38.10): 38.23, ("entras", 45.66): 45.88, ("prioritaria", 47.54): 47.71,
               # QA of v5 (energy envelope + short transcriptions): the Black Friday hits land on these words
               ("y", 3.48): 3.58, ("del", 41.52): 41.69, ("Black", 41.78): 41.97, ("Friday,", 42.10): 42.33},
          "g": {("te", 23.06): 23.24, ("este", 22.16): 22.26, ("Black", 22.44): 22.55, ("Friday", 22.66): 22.78}}
# words Whisper hears that she doesn't say: «un» before «entero» (the creator's own jump cut lands there; the voice
# comes back straight on the «e» of «entero»)
DROP = {"p": {("un", 36.64)}}
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


def fix_take(take):
    raw = json.load(open(os.path.join(ROOT, "tools", "align", f"raw_{take}.json")))
    words = []
    for a, b, t in raw:
        if (t, round(a, 2)) in DROP.get(take, set()):
            continue
        rep = FIX[take].get(t, t).split(" ")
        for k, r in enumerate(rep):                    # split words share the span
            words.append([a + (b - a) * k / len(rep), a + (b - a) * (k + 1) / len(rep), r])
    e = envelope(os.path.join(ROOT, SRC[take]))
    ons = onsets(e, quiet=float(np.percentile(e[e > -40], 50)) - 24, gap=8)
    out, anchors = [], []
    for i, w in enumerate(words):
        a = w[0]
        first = i == 0 or w[0] - words[i - 1][1] > 0.04 or words[i - 1][2][-1:] in ".,?!"
        if first:
            near = [o for o in ons if a - 0.15 <= o <= a + 0.45]
            if near:
                o = min(near, key=lambda o: abs(o - a)); anchors.append((w[2], round(a, 2), round(o, 2))); a = o
        a = MANUAL.get(take, {}).get((w[2], round(w[0], 2)), a)
        if out and a < out[-1][0] + 0.06: a = out[-1][0] + 0.06
        out.append([round(a, 3), round(max(w[1], a + 0.06), 3), w[2]])
    json.dump(out, open(os.path.join(ROOT, "tools", "align", f"whisper_{take}.json"), "w"), ensure_ascii=False)
    print(f"take {take}: {len(out)} words, {len(anchors)} anchors: " + " · ".join(f"{t} {a}→{b}" for t, a, b in anchors))


if __name__ == "__main__":
    for tk in SRC:
        fix_take(tk)
