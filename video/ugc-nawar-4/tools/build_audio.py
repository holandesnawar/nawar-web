#!/usr/bin/env python3
"""Music bed for UGC #4 (v4): the client's own «musica v1» (ElevenLabs; the track of UGC #2 and the Black Friday ad —
the client: the earlier ads' music «sí estaba bien»), shaped to the script (the client: «los primeros segundos más tipo
"uu, sorpresa", y luego, según el guion, que suba o baje intensidad»).

The track: a light groove at 107.7 BPM (bar 2.228 s), a soft 8-bar intro, then the groove from bar 8 on. Two layers of
it, crossfaded (no cut in the music):
  · the hook («Nuestro Black Friday empieza hoy. Sí, antes de tiempo.»): the groove straight away, present (HOOK_LUFS),
    on a soft hit + sparkle on «Black Friday» (gen.py) — the surprise;
  · the problem (from «¿Por qué tan pronto?»): it drops to the soft intro, low (LOW_LUFS);
  · «Por eso lo abrimos ahora» (TURN): the groove comes back on its downbeat (MID_LUFS);
  · the offer (from «La primera oferta»): a little higher (OFFER_LUFS), then it fades on her last words.
The take is normalised to −16 LUFS: the bed sits 17–26 LU under her voice. Less low end and a dip at 2.5 kHz keep it out
of her way. Outputs assets/audio/music-bed.wav and audio.json.
"""
import json, os, re, subprocess
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, ".raw", "music.mp3")
BAR, BAR0, GROOVE_BAR = 4 * 60 / 107.7, 0.023, 8
EQ = "highpass=f=110,lowshelf=f=150:g=-6,lowshelf=f=250:g=-6,equalizer=f=2500:t=q:w=0.9:g=-3"
HOOK_LUFS, LOW_LUFS, MID_LUFS, OFFER_LUFS = -37.0, -44.0, -35.5, -35.0   # v6: the pains calm and low, a lift at the turn
XF, FADE_OUT = 0.35, 0.8
SR = 48000


def lufs(path, ss, t):
    out = subprocess.run(["ffmpeg", "-nostats", "-ss", f"{ss:.3f}", "-t", f"{t:.3f}", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])


def ramp(n, sr, pts):
    """piecewise-linear gain (dB) over the ad from (time, dB) points."""
    t = np.arange(n) / sr; ts, vs = zip(*pts)
    return np.interp(t, ts, vs).astype(np.float32)


def main():
    ed = json.load(open(os.path.join(ROOT, "edit.json"))); total = ed["total"]
    eq_wav = os.path.join(ROOT, ".raw", "music-eq.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", MUSIC, "-af", EQ, "-ar", str(SR), "-ac", "2", eq_wav], check=True)
    y, sr = sf.read(eq_wav, dtype="float32")
    groove = BAR0 + GROOVE_BAR * BAR
    l_intro, l_groove = lufs(eq_wav, 1.0, groove - 1.5), lufs(eq_wav, groove + 1.0, 40.0)
    n = int(round(total * sr)) + 1
    low_at = next(i["start"] for i in ed["inserts"] if i["id"] == "ins-01")   # v6: from 0:05 («Porque cada mes…»), calm
    turn = ed["turn"]; offer = ed["offer"]
    # layer A, the groove, from bar 8 at t = 0; its downbeat nearest the turn is where it comes back
    a = y[int(groove * sr):int(groove * sr) + n]; a = np.pad(a, ((0, n - len(a)), (0, 0)))
    back = round(round(turn / BAR) * BAR - 0.02, 3)
    # layer B, the soft intro, from its start at the end of the hook
    soft_wav = os.path.join(ROOT, ".raw", "music-soft.wav")              # v6: the intro, mellower (no highs, a touch slower in feel)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", eq_wav, "-af", "lowpass=f=2200,treble=g=-4", soft_wav], check=True)
    ys, _ = sf.read(soft_wav, dtype="float32")
    b = np.zeros((n, 2), np.float32); i0 = int(low_at * sr); m = min(n - i0, len(ys)); b[i0:i0 + m] = ys[:m]
    off = -80.0
    ga = ramp(n, sr, [(0, HOOK_LUFS - l_groove), (low_at - XF / 2, HOOK_LUFS - l_groove), (low_at + XF / 2, off), (back - XF, off),
                      (back, MID_LUFS - l_groove), (offer - 0.2, MID_LUFS - l_groove), (offer + 0.6, OFFER_LUFS - l_groove),
                      (total, OFFER_LUFS - l_groove)])
    gb = ramp(n, sr, [(0, off), (low_at - XF / 2, off), (low_at + XF / 2, LOW_LUFS - l_intro), (back - XF, LOW_LUFS - l_intro),
                      (back + 0.1, off), (total, off)])
    mus = a * (10 ** (ga / 20))[:, None] + b * (10 ** (gb / 20))[:, None]
    fi = int(0.35 * sr); mus[:fi] *= np.linspace(0, 1, fi)[:, None] ** 2   # v5: comes up right behind the opening boom
    fo = int(FADE_OUT * sr); mus[n - fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus.astype(np.float32), sr)
    json.dump({"track": "musica v1", "hook_groove": [0, low_at], "soft_from": low_at, "groove_back": back, "offer_lift": offer,
               "total": total}, open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {n / sr:.2f}s: groove 0–{low_at:.2f} at {HOOK_LUFS} · soft intro to {back:.2f} at {LOW_LUFS} · groove back at {back:.2f} "
          f"({MID_LUFS}) · offer from {offer:.2f} ({OFFER_LUFS})")


if __name__ == "__main__":
    main()
