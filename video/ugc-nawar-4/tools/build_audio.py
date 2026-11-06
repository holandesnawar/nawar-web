#!/usr/bin/env python3
"""Music bed for UGC #4 (v2): the owner's calm VSL track («musica-v2», the one under UGC #1), not the ad-style groove —
the client: «la música no me gusta mucho, es el mismo estilo anuncio; otra cosa más tranquila de fondo».

The track: 100 BPM (bar 2.4 s): a soft intro (bars 0–7), then the hats section (bars 8–15). It runs from its intro so
that bar 8 lands on «y no es falta de ganas» (TURN in edit.py), then bars 8–15 again, bar-aligned, to the end — no drop,
no final hit. Background only: less low end and a gentle dip around 2.5 kHz leave room for her voice; the levels are
loudness units, about 22 LU under the voice (the take is normalised to −16 LUFS). Fades in on the first frame and out on
her last words. Outputs assets/audio/music-bed.wav and audio.json.
"""
import json, os, re, subprocess
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, ".raw", "music-vsl.mp3")
BAR, BAR0, PART2 = 2.4, 0.041, 8          # bar length, first downbeat, the bar where the hats come in
EQ = "highpass=f=100,lowshelf=f=200:g=-4,equalizer=f=2500:t=q:w=0.9:g=-3"
INTRO_LUFS, LEVEL_LUFS = -39.0, -38.0     # intro / from the turn on
FADE_IN, FADE_OUT = 0.4, 0.8
SR = 48000


def lufs(path, ss, t):
    out = subprocess.run(["ffmpeg", "-nostats", "-ss", f"{ss:.3f}", "-t", f"{t:.3f}", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def main():
    ed = json.load(open(os.path.join(ROOT, "edit.json"))); total = ed["total"]
    eq_wav = os.path.join(ROOT, ".raw", "music-eq.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", MUSIC, "-af", EQ, "-ar", str(SR), "-ac", "2", eq_wav], check=True)
    y, sr = sf.read(eq_wav, dtype="float32")
    p2 = BAR0 + PART2 * BAR; p2_end = BAR0 + 16 * BAR
    l_intro, l_p2 = lufs(eq_wav, 1.0, p2 - 1.5), lufs(eq_wav, p2, p2_end - p2)
    turn = round(ed["turn"] - 0.03, 3)
    s0 = turn - p2                                   # where the track's 0 lands in the ad (negative: already playing)
    n = int(round(total * sr)) + 1
    # the track's timeline from s0: intro, then bars 8–15 over and over
    src = np.arange(n) / sr - s0
    loop = p2_end - p2
    src = np.where(src >= p2_end, p2 + (src - p2) % loop, src)
    idx = np.clip(np.round(src * sr).astype(int), 0, len(y) - 1)
    mus = y[idx].copy()
    mus[src < 0] = 0
    tt = np.arange(n) / sr
    gdb = np.where(tt < turn, INTRO_LUFS - l_intro, LEVEL_LUFS - l_p2)
    j = int(turn * sr); r = int(0.4 * sr)
    gdb[max(0, j - r // 2):j + r // 2] = np.linspace(gdb[max(0, j - r // 2 - 1)], gdb[min(n - 1, j + r // 2 + 1)], len(gdb[max(0, j - r // 2):j + r // 2]))
    mus *= (10 ** (gdb / 20)).astype(np.float32)[:, None]
    fi = int(FADE_IN * sr); mus[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(FADE_OUT * sr); mus[n - fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus, sr)
    json.dump({"track": "musica-v2 (VSL)", "starts_at": round(s0, 3), "part2_in": turn, "fade_from": round(total - FADE_OUT, 3),
               "total": total}, open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {n / sr:.2f}s  track from {s0:.2f}s  bar {PART2} on «y no es» at {turn:.2f}  sections {l_intro:.1f}/{l_p2:.1f} LUFS "
          f"→ {INTRO_LUFS}/{LEVEL_LUFS}")


if __name__ == "__main__":
    main()
