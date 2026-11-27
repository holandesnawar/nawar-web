#!/usr/bin/env python3
"""Synthesised sounds of the Black Friday ad (v5), no samples:
  · assets/sfx/impact.mp3 — the hit under each Black Friday backdrop. Built for a phone speaker (≈40 % of its energy
    above 300 Hz): a short sub sweep 120 → 45 Hz, a body 260 → 150 Hz with its 2nd and 3rd harmonics, a 1–6 kHz snap
    and a 300–2500 Hz «room» tail, softly saturated, peak −3 dBFS (MP3 overshoots, so not −1).
  · assets/sfx/page.mp3 — one page of the ebook turning: band-passed noise (2–7 kHz), a quick rise and ~0.18 s fall,
    with a lighter flutter in the middle.
"""
import os, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000


def write(name, x):
    wav = os.path.join(ROOT, ".raw", f"{name}.wav"); sf.write(wav, np.stack([x, x], 1).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k",
                    os.path.join(ROOT, "assets", "sfx", f"{name}.mp3")], check=True)
    print(f"assets/sfx/{name}.mp3")


def bp(lo, hi, x):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)


def impact():
    t = np.arange(int(0.9 * SR)) / SR; rng = np.random.default_rng(7)
    f = 45 + (120 - 45) * np.exp(-t / 0.06); sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    fb = 150 + (260 - 150) * np.exp(-t / 0.03); ph = 2 * np.pi * np.cumsum(fb) / SR
    body = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)) * np.exp(-t / 0.10)
    snap = bp(1000, 6000, rng.standard_normal(len(t))) * np.exp(-t / 0.025)
    room = bp(300, 2500, rng.standard_normal(len(t))) * np.exp(-t / 0.25)
    x = np.tanh(1.4 * (0.45 * sub + 0.8 * body + 2.2 * snap + 0.9 * room)); x *= 10 ** (-3 / 20) / np.abs(x).max()
    fd = int(0.05 * SR); x[-fd:] *= np.linspace(1, 0, fd)
    return x


def page():
    t = np.arange(int(0.32 * SR)) / SR; rng = np.random.default_rng(11)
    env = (1 - np.exp(-t / 0.018)) * np.exp(-t / 0.075)
    env += 0.35 * np.exp(-((t - 0.12) / 0.03) ** 2)                 # the flutter as the page passes
    x = bp(2000, 7000, rng.standard_normal(len(t))) * env + 0.25 * bp(600, 2000, rng.standard_normal(len(t))) * env
    x *= 10 ** (-6 / 20) / np.abs(x).max()
    fd = int(0.04 * SR); x[-fd:] *= np.linspace(1, 0, fd)
    return x


def main():
    write("impact", impact()); write("page", page())


if __name__ == "__main__":
    main()
