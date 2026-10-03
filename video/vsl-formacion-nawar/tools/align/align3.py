"""Two-stage anchored forced alignment (script known, voice take given).

Stage A: global DTW gives rough boundary times; long pauses (>=0.15 s) are
matched to punctuated boundaries within 1.5 s and become anchors; every
stretch between anchors is re-aligned with a local DTW.
Stage B: short pauses (0.06-0.15 s) become extra anchors only when the
stage-A boundary time for a punctuated boundary lands within 0.3 s of them.
Then the local DTW runs again with the full anchor set.

Usage: python3 align3.py script.txt voice.wav out.json
"""
import json, re, sys
import numpy as np, librosa
from align import synth, SR
from align2 import mfcc, dtw_map, pauses_of, HOP

def local_align(A, B, syn_starts, syn_dur, n, anchors, first_on, last_off):
    segs, prev_k, prev_t = [], -1, first_on
    for k, a, b in anchors:
        segs.append((prev_k + 1, k, prev_t, a)); prev_k, prev_t = k, b
    segs.append((prev_k + 1, n - 1, prev_t, last_off))
    starts, ends = np.zeros(n), np.zeros(n)
    for lo, hi, t0, t1 in segs:
        s0 = syn_starts[lo]
        s1 = syn_starts[hi + 1] if hi + 1 < n else syn_dur
        a0, a1 = int(s0 / HOP), max(int(s1 / HOP), int(s0 / HOP) + 2)
        b0, b1 = int(t0 / HOP), max(int(t1 / HOP), int(t0 / HOP) + 2)
        sub = dtw_map(A[:, a0:a1], B[:, b0:b1])
        ii = np.arange(len(sub)); ok = ~np.isnan(sub)
        sub = np.interp(ii, ii[ok], sub[ok])
        for w in range(lo, hi + 1):
            if w == lo:
                starts[w] = t0
            else:
                i = min(max(int(round(syn_starts[w] / HOP)) - a0, 0), len(sub) - 1)
                starts[w] = (b0 + sub[i]) * HOP
        for w in range(lo, hi + 1):
            ends[w] = (starts[w + 1] - 0.02) if w < hi else t1
    return starts, ends

def match(pauses, bound_t, cand, win, existing):
    """Monotonic greedy match of pauses to candidate boundaries, respecting existing anchors."""
    fixed = {k for k, _, _ in existing}
    out = list(existing)
    for a, b in pauses:
        mid = (a + b) / 2
        lo_k = max([k for k, aa, bb in out if bb <= a] or [-1])
        hi_k = min([k for k, aa, bb in out if aa >= b] or [10 ** 9])
        best = [k for k in cand if lo_k < k < hi_k and k not in fixed and abs(bound_t[k] - mid) < win]
        if best:
            k = min(best, key=lambda k: abs(bound_t[k] - mid))
            out.append((k, a, b)); fixed.add(k)
    return sorted(out)

def main():
    txt, wav, outp = sys.argv[1:4]
    text = open(txt, encoding="utf-8").read().strip().replace("\n", " ")
    toks = list(re.finditer(r"[\wÀ-ÿ'’]+", text))
    n = len(toks)
    punct = [text[m.end():(toks[k + 1].start() if k + 1 < n else len(text))].strip() for k, m in enumerate(toks)]
    syn, ssr, ev = synth(text, 175)
    assert len(ev) == n
    syn = librosa.resample(syn, orig_sr=ssr, target_sr=SR)
    real, _ = librosa.load(wav, sr=SR, mono=True)
    syn_starts = np.array([e[2] for e in ev]); syn_dur = len(syn) / SR
    A, B = mfcc(syn), mfcc(real)
    m1 = dtw_map(A[:, ::2], B[:, ::2])
    idx = np.arange(len(m1)); ok = ~np.isnan(m1)
    m1 = np.interp(idx, idx[ok], m1[ok]) * 2 * HOP
    bound0 = [float(m1[min(int(syn_starts[k + 1] / (2 * HOP)), len(m1) - 1)]) for k in range(n - 1)]
    cand = [k for k in range(n - 1) if punct[k] and any(c in punct[k] for c in ",.;:?!…")]
    rp, db = pauses_of(real, min_len=0.06, thr=-42)
    first_on = float(np.argmax(db > -40) * 0.01)
    last_off = float((len(db) - np.argmax((db > -40)[::-1])) * 0.01)
    long_p = [p for p in rp if p[1] - p[0] >= 0.15]
    short_p = [p for p in rp if p[1] - p[0] < 0.15]
    anchors = match(long_p, bound0, cand, 1.5, [])
    st, en = local_align(A, B, syn_starts, syn_dur, n, anchors, first_on, last_off)
    bound1 = [float((en[k] + st[k + 1]) / 2) for k in range(n - 1)]
    anchors2 = match(short_p, bound1, cand, 0.3, anchors)
    st, en = local_align(A, B, syn_starts, syn_dur, n, anchors2, first_on, last_off)
    words = [{"id": f"w{k}", "text": toks[k].group(0), "start": round(float(st[k]), 3), "end": round(float(max(en[k], st[k] + 0.06)), 3), "punct": punct[k]} for k in range(n)]
    json.dump({"voice": wav, "duration": round(len(real) / SR, 3), "anchors_long": len(anchors), "anchors_total": len(anchors2), "words": words}, open(outp, "w"), ensure_ascii=False, indent=1)
    print(f"{wav}: words={n} long_pauses={len(long_p)} anchors_long={len(anchors)} short_pauses={len(short_p)} anchors_total={len(anchors2)}")

if __name__ == "__main__":
    main()
