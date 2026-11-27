#!/usr/bin/env python3
"""Procedural music bed for the Nawar VSL (placeholder until the owner supplies a track).

Arc (PAS → minor-to-major): section A 0–52.15 s in A minor, sparse and tense (pad, soft plucks,
sub, ticking hats that build, a thin-out + riser into the turn); section B 52.15–115.44 s in
C major, bright and driving (four-on-the-floor kick, clap, hats, octave bass, pluck arps, bell
motif, sidechain pump); end card 115.44–121.64 s: a held Cadd9 with a bell arpeggio and a long tail.
Bar grids are fitted so the turn and the end card land exactly on downbeats.
Writes assets/audio/music_raw.wav (stereo 44.1 kHz). Deterministic (seeded noise).
"""
import json, os
import numpy as np
from scipy import signal
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
rng = np.random.default_rng(7)

timing = json.load(open(os.path.join(ROOT, "timing.json")))
TOTAL = timing["total"]
TURN = next(f["start"] for f in timing["frames"] if f["id"] == "11-nawar-nace")
END = next(f["start"] for f in timing["frames"] if f["id"] == "25-end-card")
BARS_A = 22
BAR_A = TURN / BARS_A
BARS_B = int(round((END - TURN) / BAR_A))
BAR_B = (END - TURN) / BARS_B
N = int(TOTAL * SR) + SR
L = np.zeros(N); R = np.zeros(N)

def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def env_adsr(n, a, d, s, r, sr=SR):
    a_n, d_n, r_n = int(a * sr), int(d * sr), int(r * sr)
    e = np.ones(n) * s
    if a_n: e[:min(a_n, n)] = np.linspace(0, 1, a_n)[:min(a_n, n)]
    if d_n and a_n < n:
        seg = np.linspace(1, s, d_n)[:max(0, min(d_n, n - a_n))]
        e[a_n:a_n + len(seg)] = seg
    if r_n:
        e[-min(r_n, n):] *= np.linspace(1, 0, min(r_n, n))
    return e

def polyblep_saw(f, n, phase0=0.0):
    t = np.arange(n)
    dt = f / SR
    ph = (phase0 + dt * t) % 1.0
    y = 2 * ph - 1
    m1 = ph < dt
    x = ph[m1] / dt
    y[m1] -= x + x - x * x - 1
    m2 = ph > 1 - dt
    x = (ph[m2] - 1) / dt
    y[m2] -= x * x + x + x + 1
    return y

def lowpass(x, fc, order=2):
    b, a = signal.butter(order, min(fc, SR * 0.45) / (SR / 2), "low")
    return signal.lfilter(b, a, x)

def highpass(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), "high")
    return signal.lfilter(b, a, x)

def bandpass(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), min(hi, SR * 0.45) / (SR / 2)], "band")
    return signal.lfilter(b, a, x)

def add(buf_l, buf_r, x, t0, pan=0.0, gain=1.0):
    i0 = int(t0 * SR)
    if i0 >= N: return
    x = x[: N - i0] * gain
    gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf_l[i0:i0 + len(x)] += x * gl * 1.414
    buf_r[i0:i0 + len(x)] += x * gr * 1.414

def pad_chord(notes, t0, dur, cutoff, gain):
    n = int((dur + 1.2) * SR)
    for k, m in enumerate(notes):
        f = mtof(m)
        for det, pan in ((-0.07, -0.6), (0.0, 0.0), (0.07, 0.6)):
            ff = f * 2 ** (det / 12)
            x = polyblep_saw(ff, n, phase0=(k * 0.37 + det) % 1)
            x = lowpass(x, cutoff, 2)
            x *= env_adsr(n, 0.5, 0.4, 0.85, 1.2)
            add(PL, PR, x, t0, pan=pan * 0.8, gain=gain / (len(notes) * 1.7))

def fm_pluck(f, dur, ratio=2.0, index=2.6, decay=6.0, bright=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    I = index * bright * np.exp(-t * 14)
    y = np.sin(2 * np.pi * f * t + I * np.sin(2 * np.pi * f * ratio * t))
    e = np.exp(-t * decay) * np.minimum(1, t / 0.004)
    return y * e

def sub_note(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(4 * np.pi * f * t)
    return y * env_adsr(n, 0.02, 0.2, 0.8, 0.25)

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 48 + (150 - 48) * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t * 8.5)
    click = highpass(rng.standard_normal(n), 3000) * np.exp(-t * 400) * 0.25
    return y + click

def clap():
    n = int(0.35 * SR); t = np.arange(n) / SR
    noise = bandpass(rng.standard_normal(n), 900, 5200)
    e = np.zeros(n)
    for off in (0.0, 0.011, 0.022):
        k = int(off * SR)
        e[k:] += np.exp(-(t[: n - k]) * 26)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.4
    return (noise * e * 0.6 + body) * 0.8

def hat(open_=False):
    n = int((0.25 if open_ else 0.07) * SR); t = np.arange(n) / SR
    y = highpass(rng.standard_normal(n), 7500, 3)
    return y * np.exp(-t * (14 if open_ else 70))

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    seg = int(0.05 * SR)
    for i in range(0, n, seg):
        frac = i / n
        lo = 400 + 5000 * frac ** 2
        out[i:i + seg] = bandpass(noise[i:i + seg + 400], lo, lo * 1.8)[:len(out[i:i + seg])]
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / dur) ** 2) / SR) * 0.15
    return (out + sweep) * (t / dur) ** 2.2

# buses
PL, PR = np.zeros(N), np.zeros(N)   # pads (reverb heavy, pumped in B)
ML, MR = np.zeros(N), np.zeros(N)   # plucks / bells (reverb)
BL, BR = np.zeros(N), np.zeros(N)   # bass (pumped in B)
DL, DR = np.zeros(N), np.zeros(N)   # drums

# ---- section A: A minor, sparse ----
A_PROG = [  # (pad notes, bass midi)
    ([57, 60, 64, 67], 45),  # Am7
    ([53, 57, 60, 64], 41),  # Fmaj7
    ([55, 60, 62, 64], 48),  # Cadd9
    ([55, 59, 62, 64], 43),  # G6
]
for b in range(BARS_A):
    t0 = b * BAR_A
    notes, bass = A_PROG[b % 4]
    thin = b >= BARS_A - 2
    pad_chord(notes, t0, BAR_A, 700 if b < 8 else 1000, 0.30)
    add(BL, BR, sub_note(mtof(bass - 12 if bass > 40 else bass), BAR_A * 0.98), t0, gain=0.55)
    if not thin and b >= 2:
        # soft 8th-note pluck arpeggio, darker filter
        pat = [0, 2, 1, 3, 2, 1, 3, 2]
        for i, idx in enumerate(pat):
            m = notes[idx] + 12
            y = lowpass(fm_pluck(mtof(m), 0.6, index=1.6, decay=7, bright=0.8), 2400)
            add(ML, MR, y, t0 + i * BAR_A / 8, pan=(-0.35 if i % 2 else 0.35), gain=0.16 + 0.04 * (b >= 8))
    if b >= 10 and not thin:
        for i in range(16):
            if i % 2 == 1:
                add(DL, DR, hat(), t0 + i * BAR_A / 16, pan=0.3, gain=0.05 + 0.03 * (b >= 14))
    if b >= 14 and not thin:
        add(DL, DR, kick() * 0.5, t0, gain=0.35)
        add(DL, DR, kick() * 0.5, t0 + BAR_A / 2, gain=0.3)
# riser into the turn (last bar of A)
add(ML, MR, riser(BAR_A * 1.0), TURN - BAR_A, gain=0.22)

# ---- section B: C major, driving ----
B_PROG = [
    ([60, 64, 67, 71], 36),  # Cmaj7
    ([59, 62, 67, 69], 43),  # G(add9)
    ([60, 64, 67, 69], 45),  # Am7
    ([60, 65, 69, 72], 41),  # F
]
MOTIF = [  # bell motif (beat offset, scale degree index into chord + octave)
    (0.0, 3), (1.5, 2), (2.5, 1), (3.0, 2),
]
beat_times = []
for b in range(BARS_B):
    t0 = TURN + b * BAR_B
    notes, bass = B_PROG[b % 4]
    beat = BAR_B / 4
    layer = 1 if b < 2 else (2 if b < 4 else 3)
    pad_chord(notes, t0, BAR_B, 1300, 0.30)
    # octave bass 8ths
    for i in range(8):
        m = bass if i % 2 == 0 else bass + 12
        add(BL, BR, lowpass(sub_note(mtof(m), beat * 0.48), 900), t0 + i * beat / 2, gain=0.42 if layer > 1 else 0.3)
    for i in range(4):
        add(DL, DR, kick(), t0 + i * beat, gain=0.62)
        beat_times.append(t0 + i * beat)
        if layer >= 2 and i in (1, 3):
            add(DL, DR, clap(), t0 + i * beat, pan=0.05, gain=0.26)
        if layer >= 2:
            add(DL, DR, hat(), t0 + i * beat + beat / 2, pan=0.35, gain=0.12)
        if layer >= 3:
            add(DL, DR, hat(), t0 + i * beat + beat / 4, pan=-0.3, gain=0.05)
            add(DL, DR, hat(), t0 + i * beat + 3 * beat / 4, pan=-0.3, gain=0.05)
    # bright arpeggio 8ths
    if layer >= 2:
        pat = [0, 1, 2, 3, 2, 1, 2, 3]
        for i, idx in enumerate(pat):
            m = notes[idx] + 12
            y = lowpass(fm_pluck(mtof(m), 0.5, index=2.4, decay=8), 5200)
            add(ML, MR, y, t0 + i * beat / 2, pan=(-0.45 if i % 2 else 0.45), gain=0.15)
    if layer >= 3 and b % 2 == 0:
        for off, idx in MOTIF:
            m = notes[idx] + 24
            y = fm_pluck(mtof(m), 1.4, ratio=3.5, index=1.8, decay=2.6)
            add(ML, MR, y, t0 + off * beat, pan=0.1, gain=0.075)
    if b == BARS_B - 1:  # fill into the end card
        add(ML, MR, riser(BAR_B * 0.9), t0 + BAR_B * 0.1, gain=0.14)

# ---- end card: held Cadd9 + bell arpeggio ----
END_NOTES = [48, 55, 60, 64, 67, 74]
pad_chord(END_NOTES, END, TOTAL - END + 0.2, 1500, 0.42)
add(BL, BR, sub_note(mtof(36), TOTAL - END), END, gain=0.5)
add(DL, DR, kick(), END, gain=0.6)
for i, m in enumerate([72, 76, 79, 84, 86]):
    add(ML, MR, fm_pluck(mtof(m), 2.5, ratio=3.5, index=1.6, decay=1.6), END + 0.15 + i * 0.22, pan=-0.4 + 0.2 * i, gain=0.1)

# ---- sidechain pump on pads + bass in section B ----
pump = np.ones(N)
tt = np.arange(N) / SR
for bt in beat_times:
    i0 = int(bt * SR); i1 = min(N, i0 + int(0.35 * SR))
    pump[i0:i1] = np.minimum(pump[i0:i1], 1 - 0.38 * np.exp(-(tt[i0:i1] - bt) / 0.11))
PL *= pump; PR *= pump; BL *= pump; BR *= pump

# ---- reverb (convolution with a synthetic stereo IR) ----
def ir(seconds, seed):
    r = np.random.default_rng(seed)
    n = int(seconds * SR); t = np.arange(n) / SR
    x = r.standard_normal(n) * np.exp(-t * 3.2)
    return lowpass(x, 6000) * 0.06

IRL, IRR = ir(2.6, 11), ir(2.6, 12)
def verb(l, r, wet):
    wl = signal.fftconvolve(l, IRL)[:N]; wr = signal.fftconvolve(r, IRR)[:N]
    return l + wet * wl, r + wet * wr

PL, PR = verb(PL, PR, 0.6)
ML, MR = verb(ML, MR, 0.7)
DL2, DR2 = verb(DL, DR, 0.12)

mixL = PL * 0.9 + ML + BL + DL2
mixR = PR * 0.9 + MR + BR + DR2
# section-A dynamics: start restrained, build toward the turn, thin out in the last 2 bars
dyn = np.ones(N)
iA = int(TURN * SR)
ramp = np.linspace(10 ** (-9 / 20), 10 ** (-3 / 20), int((TURN - 2 * BAR_A) * SR))
dyn[:len(ramp)] = ramp
dyn[len(ramp):iA] = 10 ** (-6 / 20)
mixL *= dyn; mixR *= dyn
mixL = highpass(mixL, 28); mixR = highpass(mixR, 28)
# fade in / out
fade_in = int(1.2 * SR)
mixL[:fade_in] *= np.linspace(0, 1, fade_in); mixR[:fade_in] *= np.linspace(0, 1, fade_in)
end_i = int(TOTAL * SR)
fo = int(3.2 * SR)
mixL[end_i - fo:end_i] *= np.linspace(1, 0, fo) ** 1.5; mixR[end_i - fo:end_i] *= np.linspace(1, 0, fo) ** 1.5
mixL[end_i:] = 0; mixR[end_i:] = 0
out = np.stack([mixL[:end_i], mixR[:end_i]], axis=1)
out = out / (np.max(np.abs(out)) + 1e-9) * 0.89
sf.write(os.path.join(ROOT, "assets", "audio", "music_raw.wav"), out.astype(np.float32), SR)
print(f"music_raw.wav {TOTAL:.2f}s · A: {BARS_A} bars × {BAR_A:.3f}s ({240 / BAR_A:.1f} BPM) · B: {BARS_B} bars × {BAR_B:.3f}s ({240 / BAR_B:.1f} BPM) · turn {TURN} · end {END}")
