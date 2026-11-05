#!/usr/bin/env python3
"""Music bed for UGC #4: the client's own track «musica v1» (ElevenLabs), the one of UGC #2 and the Black Friday ad.

The track: a modern light groove at 107.7 BPM (bar 2.228 s) — a soft 8-bar intro, then the groove from bar 8 on, even
all the way (no drops). It is placed so bar 8, where the groove comes in, lands on «¿Por qué tan pronto?» — right after
the hook; the intro runs very low under the hook. Background only: a gentle dip
around 2.5 kHz and less low end leave room for her voice, and the levels are set in loudness units: INTRO_LUFS under
the hook, LEVEL_LUFS from the groove on — about 21 LU under the voice (the take is normalised to −16 LUFS), as calm as
UGC #2. Fades out under her held last frame.
Outputs assets/audio/music-bed.wav and audio.json.
"""
import json, os, re, subprocess
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, ".raw", "music.mp3")
BAR, BAR0, GROOVE_BAR = 4 * 60 / 107.7, 0.023, 8   # bar length, first downbeat, the bar where the groove comes in
EQ = "highpass=f=110,lowshelf=f=150:g=-6,lowshelf=f=250:g=-6,equalizer=f=2500:t=q:w=0.9:g=-3"   # the track is mostly low end,
                                                     # which phone speakers drop: cut it so its keys and hats carry instead
LEVEL_LUFS = -37.0     # from «¿Por qué tan pronto?» on (≈21 LU under the voice)
INTRO_LUFS = -42.0     # the soft intro under the hook
PAUSE_LIFT_DB = 8.0    # the music comes up this much where she pauses on purpose (a gap between two shots)
FADE = 0.5             # fade out across her held last frame
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
    # the turn: «¿Por qué tan pronto?», a breath before the word
    turn = round(ed["turn"] - 0.05, 3)
    s0 = turn - groove                                 # where the track's 0 lands in the ad
    n = int(round(total * sr)) + 1
    mus = np.zeros((n, 2), np.float32)
    a = max(0, int(round(s0 * sr))); src0 = max(0, int(round(-s0 * sr)))
    m = min(n - a, len(y) - src0); mus[a:a + m] = y[src0:src0 + m]
    tt = np.arange(n) / sr
    gdb = np.where(tt < turn, INTRO_LUFS - l_intro, LEVEL_LUFS - l_groove)
    j = int(turn * sr); ramp = int(0.3 * sr)          # the groove comes in on the beat (short smoothing)
    gdb[j - ramp // 2:j + ramp // 2] = np.linspace(gdb[j - ramp // 2 - 1], gdb[j + ramp // 2 + 1], ramp)
    for s1, s2 in zip(ed["shots"], ed["shots"][1:]):   # v6.5: where she pauses on purpose (a gap between two shots, PAUSE in
        g0, g1 = s1["start"] + s1["duration"], s2["start"]  # edit.py) the music comes up so it carries the moment, not dead air
        if g1 - g0 > 0.3:
            i0, i1, r = int((g0 + 0.02) * sr), int((g1 - 0.06) * sr), int(0.18 * sr)
            lift = np.zeros(n, np.float32); lift[i0:i1] = PAUSE_LIFT_DB
            lift[i0:i0 + r] = np.linspace(0, PAUSE_LIFT_DB, r); lift[i1 - r:i1] = np.linspace(PAUSE_LIFT_DB, 0, r)
            gdb = gdb + lift
    mus *= (10 ** (gdb / 20)).astype(np.float32)[:, None]
    fi = int(0.8 * sr); mus[a:a + fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(FADE * sr); mus[n - fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus, sr)
    json.dump({"track": "musica v1", "starts_at": round(s0, 3), "groove_in": turn,
               "fade_from": round(total - FADE, 3), "total": total}, open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {n / sr:.2f}s  track from {s0:.2f}s  groove (bar {GROOVE_BAR}) on «¿Por qué tan pronto?» at {turn:.2f}  "
          f"sections {l_intro:.1f}/{l_groove:.1f} LUFS → {INTRO_LUFS}/{LEVEL_LUFS}  fade from {total - FADE:.2f}")


if __name__ == "__main__":
    main()
