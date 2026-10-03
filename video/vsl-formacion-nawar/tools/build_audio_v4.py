#!/usr/bin/env python3
"""v4 soundtrack (≤ 2:58): voice take «Voz en off VSL Escuela (4)» at 1.065× + the owner's track, as v3.

v4 = v3 with the new take (script without «sacas adelante a tu familia» / «el colegio de tus hijos»). Of the three
takes it needs the least speed-up to keep the v3 structure (drop → 32 bars → re-drop on «Completa») under 2:58.

Same dramaturgy as v2 — music STOPS after "…uno a uno.", «Vale, ¿y qué hay dentro? Te lo enseño.» over
silence, the DROP opens the Mac, breakdown from «Al terminar», riser + tension under «…probado. Ahora toca
hablar», RE-DROP on «Completa tu matrícula», final hit on «…cuando lo HABLAS» — but calmer: the bed sits 3 dB
lower when nobody speaks, a high shelf softens the hats, the duck holds through short gaps (no pumping) and
section joins let the previous bar's tail ring out.

Outputs: assets/audio/voiceover.wav (file time = master − VO_OFFSET), music_raw.wav, music.wav, audio_v4.json.
Run with --plan to print the timing plan only (no audio written).
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, ".raw", "voz-v4-4.wav")           # take (4), loudnorm −16 LUFS, 48 kHz mono
MUSIC = os.path.join(ROOT, ".raw", "music_v2.wav")           # owner's track, 44.1 kHz stereo
ALIGN = os.path.join(ROOT, "tools", "align", "a3-v4-4.json")
SPEED = 1.065
VO_OFFSET = 0.40
BAR, BAR0 = 2.4, 0.041
GAP_MAX = 0.32            # sped-up pauses longer than this are tightened to it

# words re-timed by hand (word-level Whisper + the take's energy envelope), voice-file seconds before the speed-up:
# the aligner squeezed «El algún día · ya lo has probado. · Ahora toca hablar» (this take pauses after «día»)
FIX = {541: (171.34, 171.70), 542: (171.80, 172.30), 543: (172.52, 172.62), 544: (172.64, 172.72), 545: (172.74, 172.86),
       546: (172.88, 173.34), 547: (173.70, 174.10), 548: (174.22, 174.42), 549: (174.46, 174.86)}

# v4.1: [3] = a lead-in bar (only its tail plays) so the music still starts at 0 with the slower hook
PRE = [3] + [0, 4, 1, 2, 3, 4, 5, 6, 7] + list(range(8, 16)) + [16, 17, 18, 20, 21] + [8, 9, 10, 11, 12, 14, 15] + list(range(16, 24))
POST = list(range(24, 48)) + list(range(16, 24))      # 32 bars: drop → re-drop
REDROP = [24, 25, 47]                                  # 3 bars: re-drop → final hit
FINAL = 48
MUSIC_RMS_DB = -21.0      # bed level with no voice on top (v2: −18)
DUCK_DB = -11.0           # extra attenuation under the voice → ≈ −32 dBFS RMS under speech (as v2)
PAUSE_LEAD = 0.30         # v4: 20-pausa opens this long before the stop — the cursor clicks pause ON the stop
TAIL = 1.9                # seconds of the final hit's ring-out (faded) after the hit (shortened if needed for MAX_TOTAL)
MAX_TOTAL = 177.95        # keep the film under 2:58
# v4.1 (owner: «el inicio va algo rápido»): the hook — up to «…en menos de tres minutos.» (frames 01–03) — plays at
# the take's natural speed with its own pauses, plus a little air after two sentences; the speed-up starts after it
INTRO_LAST = "minutos"
INTRO_AIR = {"funcionar": 0.18, "idiomas": 0.15}

def intro_cut():
    """(index of the hook's last word, cut time in the raw take: the middle of the pause after it)."""
    W = json.load(open(ALIGN))["words"]
    i = next(k for k, w in enumerate(W) if w["text"].lower().strip("¿?,.…") == INTRO_LAST)
    return i, (W[i]["end"] + W[i + 1]["start"]) / 2

def to_fast(t, cut):
    """raw take time → processed voice time (natural speed up to the cut, SPEED after it)."""
    return t if t <= cut else cut + (t - cut) / SPEED

def words():
    W = json.load(open(ALIGN))["words"]
    _, cut = intro_cut()
    out = []
    for i, w in enumerate(W):
        s, e = FIX.get(i, (w["start"], w["end"])); e = max(e, s + 0.05)
        out.append({"i": i, "text": w["text"], "punct": w.get("punct", ""), "start": to_fast(s, cut), "end": to_fast(e, cut)})
    for a, b in zip(out, out[1:]):                        # keep order after fixes
        if a["end"] > b["start"]: a["end"] = b["start"]
    return out

def find(W, phrase, start=0):
    toks = phrase.lower().split()
    norm = lambda s: s.lower().strip("¿?,.…:¡!")
    for i in range(start, len(W)):
        if all(norm(W[i + k]["text"]) == toks[k] for k in range(len(toks))):
            return i
    raise SystemExit(f"not found: {phrase}")

def bars_to_audio(seq, y, sr, xin=0.012, xout=0.15):
    """Whole bars; contiguous runs copied straight; at joins the previous run's tail rings out (xout) under the next downbeat."""
    n = int(round(BAR * sr)); a_in = int(xin * sr); a_out = int(xout * sr)
    out = np.zeros((n * len(seq) + a_out, y.shape[1]), dtype=np.float32)
    k = 0
    while k < len(seq):
        j = k
        while j + 1 < len(seq) and seq[j + 1] == seq[j] + 1:
            j += 1
        a = int(round((BAR0 + BAR * seq[k]) * sr)); L = n * (j - k + 1)
        chunk = y[a:a + L + a_out].copy()
        if chunk.shape[0] < L + a_out:
            chunk = np.pad(chunk, ((0, L + a_out - chunk.shape[0]), (0, 0)))
        if k > 0:
            chunk[:a_in] *= np.sin(np.linspace(0, np.pi / 2, a_in))[:, None]
        chunk[L:] *= (np.cos(np.linspace(0, np.pi / 2, a_out)) ** 2)[:, None]
        out[n * k:n * k + L + a_out] += chunk
        k = j + 1
    return out[: n * len(seq)]

def duck(mus, sr, vo, vsr, total, relief=()):
    hop = int(0.01 * sr); n = len(mus) // hop + 1
    t = (np.arange(n) * hop) / sr - VO_OFFSET
    vi = (t * vsr).astype(int); w = int(0.02 * vsr)
    act = np.zeros(n)
    for k in range(n):
        if 0 <= vi[k] < len(vo) - w:
            act[k] = 1.0 if np.sqrt(np.mean(vo[vi[k]:vi[k] + w] ** 2)) > 10 ** (-40 / 20) else 0.0
    hold = 45                                                 # hold through gaps < 0.45 s (no pumping between phrases)
    held = act.copy()
    for k in range(n):
        if act[k]:
            held[k:k + hold] = 1.0
    env = np.zeros(n); e = 0.0
    a_up, a_dn = 1 - np.exp(-1 / 5.0), 1 - np.exp(-1 / 70.0)  # 50 ms attack, 700 ms release
    for k in range(n):
        e += (held[k] - e) * (a_up if held[k] > e else a_dn); env[k] = e
    env = np.maximum(env, np.concatenate([env[8:], np.zeros(8)]))   # 80 ms look-ahead
    tm = np.arange(n) * hop / sr
    for t0, t1, cap in relief:
        sel = (tm >= t0) & (tm < t1); env[sel] = np.minimum(env[sel], cap)
    g = np.interp(np.arange(len(mus)), np.arange(n) * hop, 10 ** ((DUCK_DB * env) / 20))
    rms = np.sqrt(np.mean(mus[: int(total * sr)] ** 2)) + 1e-9
    out = mus * (10 ** (MUSIC_RMS_DB / 20) / rms * g)[:, None]
    pk = np.abs(out).max()
    if pk > 0.89: out *= 0.89 / pk
    return out.astype(np.float32)

def main():
    tmp = os.path.join(ROOT, ".raw"); os.makedirs(tmp, exist_ok=True)
    fast = os.path.join(tmp, "voz-v4-fast.wav")
    plan_only = "--plan" in sys.argv
    i_last, cut = intro_cut()
    raw, vsr = sf.read(VOICE, dtype="float32")
    k = int(round(cut * vsr))
    if plan_only:
        v = np.zeros(k + int((len(raw) - k) / SPEED), dtype=np.float32)
    else:
        rest = os.path.join(tmp, "voz-v4-rest.wav"); sf.write(rest, raw[k:], vsr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", rest, "-af",
                        f"rubberband=tempo={SPEED}:pitch=1:formant=preserved:transients=crisp:detector=compound:phase=laminar:window=standard",
                        "-ar", str(vsr), "-ac", "1", fast], check=True)
        sped, _ = sf.read(fast, dtype="float32")
        v = np.concatenate([raw[:k], sped])           # the cut sits in a pause: a plain join is silent
    W = words()
    # ---- tighten long pauses (keep GAP_MAX of silence, centred) → keep-intervals + time map
    keep, removed = [], 0.0
    cur = 0.0
    shifts = []                                   # (time in fast voice, cumulative removed before it)
    air = {}
    for name, sec in INTRO_AIR.items():
        air[next(w["i"] for w in W if w["text"].lower().strip("¿?,.…") == name)] = sec
    for a, b in zip(W, W[1:]):
        g = b["start"] - a["end"]
        if b["i"] <= i_last:                       # inside the hook: natural pauses, plus the extra air
            if a["i"] in air:
                c = (a["end"] + b["start"]) / 2
                keep.append((cur, c)); keep.append(("air", air[a["i"]])); cur = c; removed -= air[a["i"]]
        elif g > GAP_MAX:
            c0 = a["end"] + GAP_MAX / 2; c1 = b["start"] - GAP_MAX / 2
            keep.append((cur, c0)); cur = c1; removed += c1 - c0
        shifts.append((b["start"], removed))
    keep.append((cur, len(v) / vsr))
    def tc(t):
        r = 0.0
        for ts, rem in shifts:
            if ts <= t + 1e-9: r = rem
            else: break
        return t - r
    for w in W:
        w["start"], w["end"] = tc(w["start"]), tc(w["end"])
    f = int(0.008 * vsr); pieces = []
    for a, b in keep:
        if a == "air":
            pieces.append(np.zeros(int(round(b * vsr)), dtype=np.float32)); continue
        s = v[int(a * vsr):int(b * vsr)].copy()
        if len(s) > 2 * f:
            s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
        pieces.append(s)
    vc = np.concatenate(pieces)
    # ---- story points
    i_uno = find(W, "uno a uno") + 2; i_vale = find(W, "vale", i_uno); i_ens = find(W, "enseño", i_vale)
    i_dieci = i_ens + 1; i_comp = find(W, "completa tu", i_dieci); i_form = find(W, "formación nawar", i_comp)
    i_hab = len(W) - 1
    cut1 = (W[i_uno]["end"] + W[i_vale]["start"]) / 2; cut2 = (W[i_ens]["end"] + W[i_dieci]["start"]) / 2
    S = W[i_uno]["end"] + VO_OFFSET + 0.12 + PAUSE_LEAD         # music stop (master) = the click on pause
    shift2 = S + 0.50 - W[i_vale]["start"]                      # "Vale" 0.5 s into the silence
    D = W[i_ens]["end"] + shift2 + 0.30                         # the drop
    redrop = D + BAR * len(POST)
    shift3 = redrop - 0.03 - W[i_comp]["start"]                 # "Completa" lands on the re-drop
    G = W[i_dieci]["start"] + shift3 - D
    final_hit = redrop + BAR * len(REDROP)
    # "HAblas" onset on the final hit: open the breath before «Formación Nawar» by the difference
    extra = final_hit - (W[i_hab]["start"] + shift3)
    assert -0.05 < extra < 0.9, f"final-hit gap {extra:.2f}s out of range"
    cut3 = (W[i_form - 1]["end"] + W[i_form]["start"]) / 2
    shift4 = shift3 + max(0.0, extra)
    tail_s = round(min(TAIL, MAX_TOTAL - final_hit), 3)
    total = round(final_hit + tail_s, 3)
    pre_bar0 = S - BAR * len(PRE)
    i_at = find(W, "al terminar", i_dieci); i_ah = find(W, "ahora toca", i_at)
    rel = {"S": S, "D": D, "G": G, "redrop": redrop, "final_hit": final_hit, "total": total, "pre_bar0": pre_bar0, "extra": extra,
           "breakdown_vs_al_terminar": D + BAR * 24 - (W[i_at]["start"] + shift3), "tension_vs_ahora": D + BAR * 31 - (W[i_ah]["start"] + shift3)}
    print("plan:", "  ".join("%s %.3f" % kv for kv in rel.items()))
    if plan_only:
        return
    # ---- voice placement
    vo_len = total - VO_OFFSET
    vo = np.zeros(int(round(vo_len * vsr)) + 1, dtype=np.float32)
    segs = [(0, cut1, VO_OFFSET), (cut1, cut2, shift2), (cut2, cut3, shift3), (cut3, len(vc) / vsr, shift4)]
    for a, b, sh in segs:
        s = vc[int(a * vsr):int(b * vsr)].copy(); ff = int(0.01 * vsr)
        s[:ff] *= np.linspace(0, 1, ff); s[-ff:] *= np.linspace(1, 0, ff)
        o = int(round((a + sh - VO_OFFSET) * vsr)); s = s[: max(0, len(vo) - o)]
        vo[o:o + len(s)] += s
    sf.write(os.path.join(ROOT, "assets", "audio", "voiceover.wav"), vo, vsr)
    # ---- music
    y, sr = sf.read(MUSIC, dtype="float32")
    pre = bars_to_audio(PRE, y, sr); post = bars_to_audio(POST + REDROP, y, sr)
    a = int(round((BAR0 + BAR * FINAL) * sr)); tail = y[a:a + int((tail_s + 0.3) * sr)].copy()
    fo = np.ones(len(tail)); k0 = int(0.6 * sr); fo[k0:] = np.linspace(1, 0, len(tail) - k0) ** 2; fo[int(tail_s * sr):] = 0
    tail *= fo[:, None]
    mus = np.zeros((int(round(total * sr)) + 1, 2), dtype=np.float32)
    skip = int(round(max(0.0, -pre_bar0) * sr)); off = int(round(max(0.0, pre_bar0) * sr))
    pre = pre[skip:]
    fi = int(0.03 * sr); pre[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo2 = int(0.04 * sr); pre[-fo2:] *= np.linspace(1, 0, fo2)[:, None]        # the stop — firm but not a click
    mus[off:off + len(pre)] += pre[: len(mus) - off]
    d = int(round(D * sr)); post_all = np.concatenate([post, tail])
    mus[d:d + len(post_all)] += post_all[: len(mus) - d]
    raw = os.path.join(ROOT, "assets", "audio", "music_raw.wav"); sf.write(raw, mus, sr)
    soft = os.path.join(tmp, "music_soft.wav")                  # gentle high shelf: hats less fizzy
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "highshelf=f=6500:g=-3.5,lowshelf=f=60:g=-1.5", soft], check=True)
    ms, _ = sf.read(soft, dtype="float32")
    relief = [(D - 0.05, D + G - 0.12, 0.0), (redrop - 0.03, redrop + 0.18, 0.6), (final_hit - 0.03, total, 0.35)]
    sf.write(os.path.join(ROOT, "assets", "audio", "music.wav"), duck(ms, sr, vo, vsr, total, relief), sr)
    # ---- transcript (voice-file time = master − VO_OFFSET)
    def place(t):
        for a, b, sh in segs:
            if a - 1e-6 <= t < b + 1e-6: return t + sh - VO_OFFSET
        return t + segs[-1][2] - VO_OFFSET
    tr = []
    for w in W:
        p = w["punct"].replace("¿", "").replace("¡", "").strip()
        tr.append({"id": f"w{w['i']}", "text": w["text"], "start": round(place(w["start"]), 3),
                   "end": round(place(w["end"]), 3), "punct": p[:1] if p else ""})
    json.dump(tr, open(os.path.join(ROOT, "transcript.json"), "w"), ensure_ascii=False, indent=1)
    plan = {"vo_offset": VO_OFFSET, "speed": SPEED, "total": total, "stop": round(S, 3), "pause_cut": round(S - PAUSE_LEAD, 3), "drop": round(D, 3),
            "voice_back_after_drop": round(G, 3), "redrop": round(redrop, 3), "final_hit": round(final_hit, 3),
            "breakdown": round(D + BAR * 24, 3), "riser": round(D + BAR * 30, 3), "tension": round(D + BAR * 31, 3),
            "pre_bar0": round(pre_bar0, 3), "bar": BAR, "removed_pause_s": round(removed, 3), "formacion_gap_extra": round(extra, 3)}
    json.dump(plan, open(os.path.join(ROOT, "audio_v4.json"), "w"), indent=1)
    print(json.dumps(plan, indent=1))

if __name__ == "__main__":
    main()
