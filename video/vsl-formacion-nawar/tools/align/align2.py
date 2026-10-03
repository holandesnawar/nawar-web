"""Anchor-constrained forced alignment.

Pass 1: global MFCC-DTW between espeak-ng synthesis of the script and the
take gives a rough time for every word boundary.
Pass 2: real pauses in the take are matched (monotonically) to punctuated
word boundaries near their pass-1 time; those become hard anchors.
Pass 3: each stretch between anchors is re-aligned with its own local DTW,
so drift cannot accumulate across the take.

Usage: python3 align2.py script.txt voice.mp3 out.json
"""
import json, re, sys
import numpy as np, librosa
from align import synth, SR

HOP = 0.01

def mfcc(y):
    m = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=14, n_fft=1024, hop_length=int(SR * HOP))[1:]
    return (m - m.mean(axis=1, keepdims=True)) / (m.std(axis=1, keepdims=True) + 1e-6)

def dtw_map(A, B):
    """Return array mapping each column of A to a (fractional) column of B."""
    _, wp = librosa.sequence.dtw(X=A, Y=B, metric="euclidean", backtrack=True)
    wp = wp[::-1]
    nA = A.shape[1]
    acc = [[] for _ in range(nA)]
    for i, j in wp:
        acc[i].append(j)
    return np.array([np.median(a) if a else np.nan for a in acc])

def pauses_of(y, min_len=0.16, thr=-40):
    rms = librosa.feature.rms(y=y, frame_length=882, hop_length=220)[0]
    db = librosa.amplitude_to_db(rms, ref=np.max)
    v = db > thr
    out, s = [], None
    for i, x in enumerate(v):
        if not x and s is None:
            s = i
        if x and s is not None:
            if (i - s) * 0.01 >= min_len:
                out.append((s * 0.01, i * 0.01))
            s = None
    return out, db

def main():
    txt, wav, outp = sys.argv[1:4]
    text = open(txt, encoding="utf-8").read().strip().replace("\n", " ")
    toks = list(re.finditer(r"[\wÀ-ÿ'’]+", text))
    punct = [text[m.end():(toks[k + 1].start() if k + 1 < len(toks) else len(text))].strip() for k, m in enumerate(toks)]
    syn, ssr, ev = synth(text, 175)
    assert len(ev) == len(toks), (len(ev), len(toks))
    syn = librosa.resample(syn, orig_sr=ssr, target_sr=SR)
    real, _ = librosa.load(wav, sr=SR, mono=True)
    syn_starts = np.array([e[2] for e in ev])
    syn_dur = len(syn) / SR
    A, B = mfcc(syn), mfcc(real)

    # pass 1 at 20 ms for memory, mapped back to 10 ms units
    A2, B2 = A[:, ::2], B[:, ::2]
    m1 = dtw_map(A2, B2)
    idx = np.arange(len(m1)); ok = ~np.isnan(m1)
    m1 = np.interp(idx, idx[ok], m1[ok]) * 2 * HOP
    def p1(t):
        return float(m1[min(int(t / (2 * HOP)), len(m1) - 1)])
    n = len(toks)
    bound_t = [p1(syn_starts[k + 1]) for k in range(n - 1)]  # rough real time of boundary after word k

    # pass 2: anchors
    rp, db = pauses_of(real, min_len=0.06, thr=-42)
    cand = [k for k in range(n - 1) if punct[k] and any(c in punct[k] for c in ",.;:?!…")]
    anchors, last_k = [], -1
    for a, b in rp:
        mid = (a + b) / 2
        win = 1.5 if (b - a) >= 0.15 else 0.6
        best = [k for k in cand if k > last_k and abs(bound_t[k] - mid) < win]
        if not best:
            continue
        k = min(best, key=lambda k: abs(bound_t[k] - mid))
        anchors.append((k, a, b)); last_k = k

    # pass 3: local DTW between anchors
    first_on = float(np.argmax(db > -40) * 0.01)
    last_off = float((len(db) - np.argmax((db > -40)[::-1])) * 0.01)
    segs = []  # (word_lo, word_hi_inclusive, real_t0, real_t1)
    prev_k, prev_t = -1, first_on
    for k, a, b in anchors:
        segs.append((prev_k + 1, k, prev_t, a)); prev_k, prev_t = k, b
    segs.append((prev_k + 1, n - 1, prev_t, last_off))
    starts = np.zeros(n); ends = np.zeros(n)
    for lo, hi, t0, t1 in segs:
        s0 = syn_starts[lo]
        s1 = syn_starts[hi + 1] if hi + 1 < n else syn_dur
        a0, a1 = int(s0 / HOP), max(int(s1 / HOP), int(s0 / HOP) + 2)
        b0, b1 = int(t0 / HOP), max(int(t1 / HOP), int(t0 / HOP) + 2)
        sub = dtw_map(A[:, a0:a1], B[:, b0:b1])
        ii = np.arange(len(sub)); okk = ~np.isnan(sub)
        sub = np.interp(ii, ii[okk], sub[okk])
        def loc(t):
            i = min(max(int(round(t / HOP)) - a0, 0), len(sub) - 1)
            return (b0 + sub[i]) * HOP
        for w in range(lo, hi + 1):
            starts[w] = t0 if w == lo else loc(syn_starts[w])
        for w in range(lo, hi + 1):
            ends[w] = (starts[w + 1] - 0.02) if w < hi else t1
    words = [{"id": f"w{k}", "text": toks[k].group(0), "start": round(float(starts[k]), 3), "end": round(float(max(ends[k], starts[k] + 0.06)), 3), "punct": punct[k]} for k in range(n)]
    json.dump({"voice": wav, "duration": round(len(real) / SR, 3), "anchors": len(anchors), "real_pauses": len(rp), "words": words}, open(outp, "w"), ensure_ascii=False, indent=1)
    print(f"{wav}: words={n} real_pauses={len(rp)} anchors={len(anchors)} speech={first_on:.2f}-{last_off:.2f}")

if __name__ == "__main__":
    main()
