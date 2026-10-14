#!/usr/bin/env python3
"""Music bed for UGC ad #2 (v6: the client's own track, «musica v1», made with ElevenLabs).

The track: a modern light groove at 107.7 BPM (bar 2.228 s) — a soft 8-bar intro, then the groove from bar 8 on,
even all the way (no drops). It is placed so bar 8, where the groove comes in, lands on «La realidad es que…» (the
turn of the story); the intro runs under the problem, and nothing is heard under the hook.
It is background only: a gentle dip around 2.5 kHz and a little less air leave room for her voice, and the levels
are set in loudness units (K-weighted, as the ear hears it): HOOK_LUFS under the hook, rising over RISE s to
INTRO_LUFS when the first graphic comes in, LEVEL_LUFS from the turn on — about 21 LU under the voice (the take is
normalised to −16 LUFS) and 1.5 LU under the previous bed. Fades out over the end card.
Outputs assets/audio/music-bed.wav and audio.json.
"""
import json, os, re, subprocess
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, ".raw", "music.mp3")
BAR, BAR0, GROOVE_BAR = 4 * 60 / 107.7, 0.023, 8   # bar length, first downbeat, the bar where the groove comes in
EQ = "equalizer=f=2500:t=q:w=0.9:g=-3,highshelf=f=7000:g=-2"
LEVEL_LUFS = -37.0     # from the turn on
INTRO_LUFS = -38.5     # under the problem (before the turn)
HOOK_LUFS = -45.0      # under the hook, until the first graphic
RISE = 1.6             # hook → intro level
FADE = 2.2             # fade out over the end card
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
    groove = BAR0 + GROOVE_BAR * BAR
    # loudness of the two sections of the track as they come out of the EQ
    l_intro, l_groove = lufs(eq_wav, 1.0, groove - 1.5), lufs(eq_wav, groove + 1.0, 40.0)
    # the turn: «La» of «La realidad es que…», a breath before the word
    W = ed["words"]; k = next(i for i, w in enumerate(W) if w["text"].lower() == "realidad")
    turn = round((W[k - 1]["t"] if W[k - 1]["text"].lower() == "la" else W[k]["t"]) - 0.05, 3)
    s0 = turn - groove                                 # where the track's 0 lands in the ad
    n = int(round(total * sr)) + 1
    mus = np.zeros((n, 2), np.float32)
    a = max(0, int(round(s0 * sr))); src0 = max(0, int(round(-s0 * sr)))
    m = min(n - a, len(y) - src0); mus[a:a + m] = y[src0:src0 + m]
    tt = np.arange(n) / sr
    hook_end = ed["inserts"][0]["start"]
    gdb = np.where(tt < turn, INTRO_LUFS - l_intro, LEVEL_LUFS - l_groove)
    j = int(turn * sr); ramp = int(1.2 * sr)       # smooth the section gain change over half a bar
    gdb[j - ramp // 2:j + ramp // 2] = np.linspace(gdb[j - ramp // 2 - 1], gdb[j + ramp // 2 + 1], ramp)
    gdb += np.interp(tt, [0, hook_end, hook_end + RISE], [HOOK_LUFS - INTRO_LUFS, HOOK_LUFS - INTRO_LUFS, 0.0])
    mus *= (10 ** (gdb / 20)).astype(np.float32)[:, None]
    fi = int(0.8 * sr); mus[a:a + fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(FADE * sr); mus[n - fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus, sr)
    json.dump({"track": "musica v1", "starts_at": round(s0, 3), "groove_in": turn, "hook_until": hook_end,
               "fade_from": round(total - FADE, 3), "total": total}, open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {n / sr:.2f}s  track from {s0:.2f}s  groove (bar {GROOVE_BAR}) on «La realidad» at {turn:.2f}  "
          f"sections {l_intro:.1f}/{l_groove:.1f} LUFS → {INTRO_LUFS}/{LEVEL_LUFS}  fade from {total - FADE:.2f}")


if __name__ == "__main__":
    main()
