#!/usr/bin/env python3
"""Music bed + ringback tone for the UGC ad.

Bed: the owner's VSL track re-edited on its bar grid (100 BPM, 2.4 s/bar): the hats section twice under the
problem/product part, the drop on «…16 semanas» (bar 24) for the result + CTA, the final hit on the end card.
It sits ~14 dB under the voice (the takes are normalised to −16 LUFS). Ringback: a 425 Hz European call tone
for «llamas». Outputs assets/audio/music-bed.wav, assets/audio/ringback.wav, audio.json.
"""
import json, os
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAR, BAR0 = 2.4, 0.041
SEQ = list(range(8, 16)) + list(range(8, 16)) + [24, 25, 26, 27, 28]
FINAL = 48

def bars(seq, y, sr, xout=0.12):
    n = int(round(BAR * sr)); a_out = int(xout * sr); out = np.zeros((n * len(seq) + a_out, y.shape[1]), np.float32)
    k = 0
    while k < len(seq):
        j = k
        while j + 1 < len(seq) and seq[j + 1] == seq[j] + 1: j += 1
        a = int(round((BAR0 + BAR * seq[k]) * sr)); L = n * (j - k + 1)
        c = y[a:a + L + a_out].copy()
        if k: c[:int(0.01 * sr)] *= np.linspace(0, 1, int(0.01 * sr))[:, None]
        c[L:] *= (np.cos(np.linspace(0, np.pi / 2, a_out)) ** 2)[:, None]
        out[n * k:n * k + L + a_out] += c
        k = j + 1
    return out[: n * len(seq)]

def main():
    ed = json.load(open(os.path.join(ROOT, "edit.json"))); total = ed["total"]
    y, sr = sf.read(os.path.join(ROOT, ".raw", "music.wav"), dtype="float32")
    bed = bars(SEQ, y, sr)
    drop = BAR * SEQ.index(24); hit = BAR * len(SEQ)
    a = int(round((BAR0 + BAR * FINAL) * sr)); tail = y[a:a + int((total - hit + 0.2) * sr)].copy()
    fo = np.ones(len(tail)); k0 = int(0.5 * sr); fo[k0:] = np.linspace(1, 0, len(tail) - k0) ** 2; tail *= fo[:, None]
    mus = np.zeros((int(round(total * sr)) + 1, 2), np.float32)
    mus[:len(bed)] += bed[: len(mus)]
    h = int(round(hit * sr)); mus[h:h + len(tail)] += tail[: len(mus) - h]
    # level: −30 dBFS RMS before the drop, −27.5 after, the final hit a touch above (no voice there)
    t = np.arange(len(mus)) / sr
    g = np.where(t < drop, 10 ** (-30 / 20), 10 ** (-27.5 / 20))
    g = np.where(t >= hit, 10 ** (-24 / 20), g)
    rms_pre = np.sqrt(np.mean(bed[: int(drop * sr)] ** 2)) + 1e-9
    mus *= (g / rms_pre)[:, None]
    fi = int(0.4 * sr); mus[:fi] *= np.linspace(0, 1, fi)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus, sr)
    # ringback: 425 Hz (+ a little 850 Hz), 0.8 s, soft edges
    rs = 48000; tt = np.arange(int(0.8 * rs)) / rs
    tone = 0.5 * np.sin(2 * np.pi * 425 * tt) + 0.12 * np.sin(2 * np.pi * 850 * tt)
    env = np.minimum(1, tt / 0.02) * np.minimum(1, (0.8 - tt) / 0.06); tone *= env * 0.5
    sf.write(os.path.join(ROOT, "assets", "audio", "ringback.wav"), tone.astype(np.float32), rs)
    json.dump({"drop": round(drop, 3), "final_hit": round(hit, 3), "total": total}, open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {len(mus) / sr:.2f}s  drop {drop:.2f}  final hit {hit:.2f}")

if __name__ == "__main__":
    main()
