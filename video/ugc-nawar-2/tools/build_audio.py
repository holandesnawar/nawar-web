#!/usr/bin/env python3
"""Music bed + ringback tone for the UGC ad (v2).

Bed: the owner's VSL track (100 BPM, 2.4 s/bar), kept calm and even so the ad feels like a person talking, not a
commercial: the soft intro (bars 0–7) under the problem, the hats section (bars 8–15) entering exactly on «La realidad es que…»,
then bars 8–15 again to the end — no drop, no final hit, the same level under the end card and a gentle fade out.
It sits ~18 dB under the voice (the take is normalised to −16 LUFS). Ringback: a 425 Hz European call tone for
«llamas». Outputs assets/audio/music-bed.wav, assets/audio/ringback.wav, audio.json.
"""
import json, os
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAR, BAR0 = 2.4, 0.041
LEVEL_DB = -34.0       # RMS of the bed (v2.2: one notch lower)
FADE = 2.2             # fade out over the end card

def seg(y, sr, a_s, b_s):
    return y[int(round(a_s * sr)):int(round(b_s * sr))].copy()

def main():
    ed = json.load(open(os.path.join(ROOT, "edit.json"))); total = ed["total"]
    y, sr = sf.read(os.path.join(ROOT, ".raw", "music.wav"), dtype="float32")
    # the turn of the story («La realidad es que…»): the hats come in on the shot where she says it
    real = next(w["t"] for w in ed["words"] if w["text"].lower() == "realidad")
    nawar = max(s["start"] for s in ed["shots"] if s["start"] <= real)
    # straight run from the intro so that bar 8 lands on «En Nawar», up to the end of bar 15
    a0 = BAR0 + 8 * BAR - nawar
    if a0 >= 0:
        first = seg(y, sr, a0, BAR0 + 16 * BAR)
    else:   # the turn comes later than the 8-bar intro: lead in with the end of the intro phrase, then the intro from bar 0
        lead = seg(y, sr, BAR0 + 8 * BAR + a0, BAR0 + 8 * BAR); body = seg(y, sr, BAR0, BAR0 + 16 * BAR)
        x0 = int(0.012 * sr); body[:x0] *= np.linspace(0, 1, x0)[:, None]; lead[-x0:] *= np.linspace(1, 0, x0)[:, None]
        first = np.concatenate([lead[:-x0], lead[-x0:] + body[:x0], body[x0:]])
    loop = seg(y, sr, BAR0 + 8 * BAR, BAR0 + 16 * BAR)
    n = int(round(total * sr)) + 1
    mus = np.zeros((n + len(loop), y.shape[1]), np.float32)
    mus[:len(first)] += first
    k = len(first); x = int(0.012 * sr)
    while k < n:                                    # bar-8 loop, 12 ms equal-gain crossfade at each seam
        c = loop.copy(); c[:x] *= np.linspace(0, 1, x)[:, None]
        mus[k - x:k] *= np.linspace(1, 0, x)[:, None]
        mus[k - x:k - x + len(c)] += c
        k += len(c) - x
    mus = mus[:n]
    rms = np.sqrt(np.mean(mus[: int(nawar * sr)] ** 2)) + 1e-9   # level the intro and the rest to the same RMS
    rms2 = np.sqrt(np.mean(mus[int(nawar * sr):] ** 2)) + 1e-9
    g = np.where(np.arange(n) < int(nawar * sr), 10 ** (LEVEL_DB / 20) / rms, 10 ** (LEVEL_DB / 20) / rms2).astype(np.float32)
    ramp = int(1.2 * sr); j = int(nawar * sr)                     # smooth the gain change over a bar half
    g[j - ramp // 2:j + ramp // 2] = np.linspace(g[j - ramp // 2 - 1], g[j + ramp // 2 + 1], ramp)
    mus *= g[:, None]
    fi = int(0.35 * sr); mus[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(FADE * sr); mus[n - fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus, sr)
    # ringback: 425 Hz (+ a little 850 Hz), 0.8 s, soft edges
    rs = 48000; tt = np.arange(int(0.8 * rs)) / rs
    tone = 0.5 * np.sin(2 * np.pi * 425 * tt) + 0.12 * np.sin(2 * np.pi * 850 * tt)
    env = np.minimum(1, tt / 0.02) * np.minimum(1, (0.8 - tt) / 0.06); tone *= env * 0.5
    sf.write(os.path.join(ROOT, "assets", "audio", "ringback.wav"), tone.astype(np.float32), rs)
    json.dump({"hats_in": round(nawar, 3), "fade_from": round(total - FADE, 3), "total": total},
              open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {n / sr:.2f}s  hats in at {nawar:.2f}  fade from {total - FADE:.2f}")

if __name__ == "__main__":
    main()
