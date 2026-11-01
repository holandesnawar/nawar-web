#!/usr/bin/env python3
"""assets/sfx/impact.mp3 — the hit under each Black Friday backdrop (v5): a short click, a thump at ~170 Hz (what a phone
speaker plays) and a sub sweep 120 → 38 Hz underneath, softly saturated, peak −1 dBFS. Synthesised, no samples."""
import os, subprocess
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000


def main():
    t = np.arange(int(0.9 * SR)) / SR
    f = 38 + (120 - 38) * np.exp(-t / 0.08)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28)
    thump = np.sin(2 * np.pi * 170 * t) * np.exp(-t / 0.05)
    rng = np.random.default_rng(7); n = rng.standard_normal(len(t))
    n = n - np.convolve(n, np.ones(24) / 24, mode="same")          # crude high-pass: the click
    click = n * np.exp(-t / 0.012)
    x = np.tanh(1.6 * (0.9 * body + 0.45 * thump + 0.22 * click))
    x *= 10 ** (-1 / 20) / np.abs(x).max()
    fade = int(0.05 * SR); x[-fade:] *= np.linspace(1, 0, fade)
    wav = os.path.join(ROOT, ".raw", "impact.wav"); sf.write(wav, np.stack([x, x], 1).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k",
                    os.path.join(ROOT, "assets", "sfx", "impact.mp3")], check=True)
    print("assets/sfx/impact.mp3")


if __name__ == "__main__":
    main()
