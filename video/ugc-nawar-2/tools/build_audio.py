#!/usr/bin/env python3
"""Music bed for UGC ad #2.

Bed: the owner's VSL track (100 BPM, 2.4 s/bar), kept calm and even so the ad feels like a person talking, not a
commercial: the soft intro (bars 0–7) under the problem, the hats section (bars 8–15) entering exactly on «La
realidad es que…» (the turn of the story), then bars 8–15 again to the end — no drop, no final hit, the same level
under the end card and a gentle fade out.
Levels (v2, «muy alta la música al principio»): the hook is almost voice only — the bed starts at HOOK_DB and rises
to INTRO_DB over RISE s when the first graphic comes in; from the turn on it sits at LEVEL_DB, ~20 dB under the voice
(the take is normalised to −16 LUFS). Outputs assets/audio/music-bed.wav and audio.json.
"""
import json, os
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAR, BAR0 = 2.4, 0.041   # bar length, first downbeat in the file
LEVEL_DB = -36.0         # RMS of the bed from the turn on
INTRO_DB = -37.0         # under the problem (before the turn)
HOOK_DB = -43.0          # under the hook, until the first graphic
RISE = 1.6               # hook → intro level
FADE = 2.2               # fade out over the end card
XF = 0.012               # crossfade at every seam

def seg(y, sr, a_s, b_s):
    return y[int(round(a_s * sr)):int(round(b_s * sr))].copy()

def main():
    ed = json.load(open(os.path.join(ROOT, "edit.json"))); total = ed["total"]
    y, sr = sf.read(os.path.join(ROOT, ".raw", "music.wav"), dtype="float32")
    x = int(XF * sr)
    # the turn: bar 8 (the hats) lands on «La» of «La realidad es que…», a breath before the word
    W = ed["words"]; k = next(i for i, w in enumerate(W) if w["text"].lower() == "realidad")
    turn = round((W[k - 1]["t"] if W[k - 1]["text"].lower() == "la" else W[k]["t"]) - 0.05, 3)
    # straight run from the intro so that bar 8 lands on the turn, up to the end of bar 15
    lead_len = turn - 8 * BAR                       # music needed before bar 0 of the intro (if the turn is late)
    if lead_len <= 0:
        first = seg(y, sr, BAR0 - lead_len, BAR0 + 16 * BAR)
    else:   # lead in with the end of the intro phrase (bar 7), then the intro from bar 0 (crossfaded, bar grid kept)
        lead = seg(y, sr, BAR0 + 8 * BAR - lead_len - XF, BAR0 + 8 * BAR); body = seg(y, sr, BAR0, BAR0 + 16 * BAR)
        body[:x] *= np.linspace(0, 1, x)[:, None]; lead[-x:] *= np.linspace(1, 0, x)[:, None]
        first = np.concatenate([lead[:-x], lead[-x:] + body[:x], body[x:]])
    loop = seg(y, sr, BAR0 + 8 * BAR, BAR0 + 16 * BAR)
    n = int(round(total * sr)) + 1
    mus = np.zeros((n + len(loop), y.shape[1]), np.float32)
    mus[:len(first)] += first
    k = len(first)
    while k < n:                                    # bar-8 loop, 12 ms equal-gain crossfade at each seam
        c = loop.copy(); c[:x] *= np.linspace(0, 1, x)[:, None]
        mus[k - x:k] *= np.linspace(1, 0, x)[:, None]
        mus[k - x:k - x + len(c)] += c
        k += len(c) - x
    mus = mus[:n]
    j = int(turn * sr)
    rms = np.sqrt(np.mean(mus[:j] ** 2)) + 1e-9      # measure the intro and the rest separately; each gets its own target
    rms2 = np.sqrt(np.mean(mus[j:] ** 2)) + 1e-9
    g = np.where(np.arange(n) < j, 10 ** (INTRO_DB / 20) / rms, 10 ** (LEVEL_DB / 20) / rms2).astype(np.float32)
    ramp = int(1.2 * sr)                            # smooth the gain change over half a bar
    g[j - ramp // 2:j + ramp // 2] = np.linspace(g[j - ramp // 2 - 1], g[j + ramp // 2 + 1], ramp)
    hook_end = ed["inserts"][0]["start"]            # the hook: from 0 to the first graphic
    tt = np.arange(n) / sr
    hook_db = np.interp(tt, [0, hook_end, hook_end + RISE], [HOOK_DB - INTRO_DB, HOOK_DB - INTRO_DB, 0.0])
    g *= (10 ** (hook_db / 20)).astype(np.float32)
    mus *= g[:, None]
    fi = int(0.8 * sr); mus[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(FADE * sr); mus[n - fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus, sr)
    json.dump({"hats_in": turn, "hook_until": hook_end, "fade_from": round(total - FADE, 3), "total": total},
              open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {n / sr:.2f}s  hook {HOOK_DB} dB until {hook_end:.2f}  hats in at {turn:.2f}  fade from {total - FADE:.2f}")

if __name__ == "__main__":
    main()
