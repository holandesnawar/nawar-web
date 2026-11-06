#!/usr/bin/env python3
"""Music bed for UGC #4 (v3): «Serene View» (Arulo, Mixkit Stock Music Free License), a soft chillout — the client:
v1's groove «estilo anuncio», v2's VSL track «mucha tensión»: «algo tranquilo». It plays from its start under the whole
ad at one even level, about 22 LU under the voice (the take is normalised to −16 LUFS), with less low end and a gentle
dip around 2.5 kHz for her voice; fades in on the first frame and out on her last words.
Outputs assets/audio/music-bed.wav and audio.json.
"""
import json, os, re, subprocess
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, ".raw", "music-serene.mp3")
EQ = "highpass=f=100,lowshelf=f=200:g=-4,equalizer=f=2500:t=q:w=0.9:g=-3"
LEVEL_LUFS = -38.0
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
    n = int(round(total * sr)) + 1
    mus = np.zeros((n, 2), np.float32); m = min(n, len(y)); mus[:m] = y[:m]
    l = lufs(eq_wav, 0.0, total)
    mus *= np.float32(10 ** ((LEVEL_LUFS - l) / 20))
    fi = int(FADE_IN * sr); mus[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(FADE_OUT * sr); mus[n - fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    sf.write(os.path.join(ROOT, "assets", "audio", "music-bed.wav"), mus, sr)
    json.dump({"track": "Serene View (Arulo, Mixkit)", "starts_at": 0.0, "fade_from": round(total - FADE_OUT, 3), "total": total},
              open(os.path.join(ROOT, "audio.json"), "w"), indent=1)
    print(f"bed {n / sr:.2f}s  «Serene View» from 0, {l:.1f} → {LEVEL_LUFS} LUFS")


if __name__ == "__main__":
    main()
