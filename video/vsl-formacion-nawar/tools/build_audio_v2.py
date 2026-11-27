#!/usr/bin/env python3
"""v2 soundtrack: voice B split in three takes + the owner's track re-edited on its own bar grid.

Story beats it serves (master time = video time):
  - music runs under the voice until "...los entrenamos uno a uno." and then STOPS dead
    (end of the riser/tension bar, exactly where the song's drop would land)
  - "Vale, ¿y qué hay dentro? Te lo cuento." is spoken over silence (the Offlesson-style pause)
  - the DROP hits on the laptop reveal; the voice comes back 1 bar later ("Dieciséis semanas…")
  - breakdown from "Al terminar…", riser under "…ya lo has probado", tension under "Ahora toca hablar",
    the drop comes back on "Completa tu matrícula" and the song's final hit lands right after "…cuando lo hablas."

Writes assets/audio/voiceover.wav (file time = master - VO_OFFSET), assets/audio/music_raw.wav (un-ducked),
assets/audio/music.wav (ducked under the voice) and audio_v2.json (the cut plan, consumed by timing.py).
"""
import json, os, subprocess
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, ".raw", "voz-v2-b.wav")           # voice B, loudnorm -16 LUFS, 48 kHz mono (tools/fetch_assets.sh)
MUSIC = os.path.join(ROOT, ".raw", "music_v2.wav")           # owner's track, 44.1 kHz stereo (tools/fetch_assets.sh)
VO_OFFSET = 0.40
BAR, BAR0 = 2.4, 0.041                                       # 100 BPM, first downbeat in the file

# voice takes (voice-file seconds): cut inside the pauses either side of "Vale … cuento."
CUT1, CUT2 = 97.34, 99.95
UNO_END, VALE_START, CUENTO_END, COMPLETA = 97.16, 97.52, 99.79, 182.34
S = UNO_END + VO_OFFSET + 0.14           # music stops (master)
SHIFT2 = S + 0.60 - VALE_START           # "Vale" 0.6 s into the silence
D = CUENTO_END + SHIFT2 + 0.35           # the drop
POST_BARS_TO_REDROP = 36                 # drop → re-drop on "Completa"
SHIFT3 = D + POST_BARS_TO_REDROP * BAR + 0.03 - COMPLETA

PRE = [0, 4, 1, 2, 3, 4, 5, 6, 7] + list(range(8, 16)) + list(range(16, 22)) + [6, 7] + list(range(8, 16)) + list(range(16, 24))
POST = list(range(24, 48)) + [40, 41, 42, 47] + list(range(16, 24)) + [24, 44, 45, 46, 47]
FINAL = 48                                # final hit + tail (to the end of the file)

def bars_to_audio(seq, y, sr, xf=0.012):
    """Concatenate whole bars; contiguous runs are copied straight, joins get a short equal-power crossfade."""
    n = int(round(BAR * sr)); x = int(xf * sr)
    out = np.zeros((n * len(seq) + x, y.shape[1]), dtype=np.float32)
    k = 0
    while k < len(seq):
        j = k
        while j + 1 < len(seq) and seq[j + 1] == seq[j] + 1:
            j += 1
        a = int(round((BAR0 + BAR * seq[k]) * sr)); L = n * (j - k + 1)
        chunk = y[a:a + L + x].copy()
        if chunk.shape[0] < L + x:
            chunk = np.pad(chunk, ((0, L + x - chunk.shape[0]), (0, 0)))
        fin = np.sin(np.linspace(0, np.pi / 2, x))[:, None]
        if k > 0:
            chunk[:x] *= fin
        chunk[L:] *= np.cos(np.linspace(0, np.pi / 2, x))[:, None]
        o = n * k
        out[o:o + L + x] += chunk
        k = j + 1
    return out[: n * len(seq)]

MUSIC_RMS_DB = -18.0      # bed level with no voice on top (the drops, the pause, the end card)
DUCK_DB = -14.0           # extra attenuation while the voice speaks → voice sits ~14–15 dB above the bed

def duck(mus, sr, vo, vsr, total, relief=()):
    """relief: (t0, t1, max_env) windows where the duck is capped so a drop/final hit punches through."""
    hop = int(0.01 * sr)
    n = len(mus) // hop + 1
    t = (np.arange(n) * hop) / sr - VO_OFFSET                   # voice-file time of each hop
    vi = (t * vsr).astype(int)
    w = int(0.02 * vsr)
    act = np.zeros(n)
    for k in range(n):
        if 0 <= vi[k] < len(vo) - w:
            act[k] = 1.0 if np.sqrt(np.mean(vo[vi[k]:vi[k] + w] ** 2)) > 10 ** (-40 / 20) else 0.0
    env = np.zeros(n); e = 0.0
    a_up, a_dn = 1 - np.exp(-1 / 4.0), 1 - np.exp(-1 / 45.0)   # 40 ms attack, 450 ms release (hops of 10 ms)
    for k in range(n):
        e += (act[k] - e) * (a_up if act[k] > e else a_dn); env[k] = e
    # look-ahead: start ducking 60 ms before the voice so consonant onsets stay clear
    env = np.maximum(env, np.concatenate([env[6:], np.zeros(6)]))
    tm = np.arange(n) * hop / sr
    for t0, t1, cap in relief:
        sel = (tm >= t0) & (tm < t1)
        env[sel] = np.minimum(env[sel], cap)
    g_hop = 10 ** ((DUCK_DB * env) / 20)
    g = np.interp(np.arange(len(mus)), np.arange(n) * hop, g_hop)
    rms = np.sqrt(np.mean(mus[: int(total * sr)] ** 2)) + 1e-9
    lvl = 10 ** (MUSIC_RMS_DB / 20) / rms
    out = mus * (lvl * g)[:, None]
    peak = np.abs(out).max()
    if peak > 0.89: out *= 0.89 / peak
    return out.astype(np.float32)

def main():
    y, sr = sf.read(MUSIC, dtype="float32")
    pre = bars_to_audio(PRE, y, sr)
    post = bars_to_audio(POST, y, sr)
    a = int(round((BAR0 + BAR * FINAL) * sr)); tail = y[a:].copy()
    tail_len = 3.6                                       # let the final hit ring, then fade
    tail = tail[: int(tail_len * sr)]
    tail *= np.concatenate([np.ones(int(1.2 * sr)), np.linspace(1, 0, len(tail) - int(1.2 * sr)) ** 2])[:, None]
    b0 = S - BAR * len(PRE)                             # master time of the first pre-drop bar (negative)
    total = round(D + BAR * len(POST) + tail_len, 3)
    mus = np.zeros((int(round(total * sr)) + 1, 2), dtype=np.float32)
    skip = int(round(-b0 * sr))
    pre = pre[skip:]
    fi = int(0.08 * sr); pre[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(0.018 * sr); pre[-fo:] *= np.linspace(1, 0, fo)[:, None]   # hard stop, no click
    mus[: len(pre)] += pre
    d = int(round(D * sr)); post_all = np.concatenate([post, tail])
    mus[d:d + len(post_all)] += post_all[: len(mus) - d]
    os.makedirs(os.path.join(ROOT, "assets", "audio"), exist_ok=True)
    sf.write(os.path.join(ROOT, "assets", "audio", "music_raw.wav"), mus, sr)

    v, vsr = sf.read(VOICE, dtype="float32")
    if v.ndim > 1: v = v.mean(1)
    def seg(a, b):
        s = v[int(a * vsr):int(b * vsr)].copy(); f = int(0.01 * vsr)
        s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f); return s
    vo_len = total - VO_OFFSET
    vo = np.zeros(int(round(vo_len * vsr)) + 1, dtype=np.float32)
    for (a, b, shift) in ((0, CUT1, VO_OFFSET), (CUT1, CUT2, SHIFT2), (CUT2, len(v) / vsr, SHIFT3)):
        s = seg(a, b); o = int(round((a + shift - VO_OFFSET) * vsr))
        vo[o:o + len(s)] += s[: len(vo) - o]
    sf.write(os.path.join(ROOT, "assets", "audio", "voiceover.wav"), vo, vsr)

    # duck the track under the voice (sample-accurate, on the master clock)
    sf.write(os.path.join(ROOT, "assets", "audio", "music.wav"), duck(mus, sr, vo, vsr, total, relief=[(D + POST_BARS_TO_REDROP * BAR - 0.03, D + POST_BARS_TO_REDROP * BAR + 0.22, 0.45), (D + BAR * len(POST) - 0.03, total, 0.0)]), sr)
    plan = {"vo_offset": VO_OFFSET, "total": total, "stop": round(S, 3), "drop": round(D, 3),
            "redrop": round(D + POST_BARS_TO_REDROP * BAR, 3), "final_hit": round(D + BAR * len(POST), 3),
            "breakdown": round(D + BAR * (24 + 4), 3), "riser": round(D + BAR * 34, 3),
            "pre_bar0": round(b0, 3), "bar": BAR,
            "segments": [{"from": 0, "to": CUT1, "shift": VO_OFFSET}, {"from": CUT1, "to": CUT2, "shift": round(SHIFT2, 3)},
                         {"from": CUT2, "to": round(len(v) / vsr, 3), "shift": round(SHIFT3, 3)}]}
    json.dump(plan, open(os.path.join(ROOT, "audio_v2.json"), "w"), indent=1)
    print(json.dumps(plan, indent=1))

if __name__ == "__main__":
    main()
