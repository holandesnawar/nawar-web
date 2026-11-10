#!/usr/bin/env python3
"""Edit decision list → edit.json (v2.3).

The girl talks to camera: take B (facing camera) carries the ad, and for one sentence, «En Nawar te enseñamos
neerlandés», the picture AND sound switch to take A (the side angle) — the camera change the client liked in v1.
Each segment is cut in a quiet point checked on the energy envelope, all at RATE (pitch preserved). The explaining
happens in full-screen inserts (cut-aways): the picture cuts to a VSL-style motion graphic while her voice carries
on, then cuts back to her. Each insert window starts a hair before its first word.

Word times come from forced alignment of each take (tools/align/align_<take>.json); where the aligner drifts more
than 0.25 s from word-level Whisper (tools/align/whisper_<take>.json, bias-corrected) the Whisper time wins.
"""
import json, os, unicodedata, re, difflib, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.05
# (take, source in, source out) — hand-checked quiet points; B → A («En Nawar te enseñamos neerlandés») → B
SEGMENTS = [("b", 0.00, 17.76), ("a", 15.06, 16.90), ("b", 19.72, 50.90)]
FACE = {"a": (500, 880), "b": (545, 900)}   # face centre per take (zoom origin)
SPEECH_END = 50.58     # «…atenderá» fades out here in take B (energy envelope); the take ends on her smile
TAIL = 1.4             # hold on her last frame (she smiles) under the enrolment block
LEAD = 0.06            # an insert cuts in this long before its first word
# (insert id, ground, first words, first words of what comes after — None = runs to the end)
INSERTS = [
    ("ins-01", "paper", "practicas la frase", "y le pides"),
    ("ins-02", "paper", "porque aqui siempre", "en nawar te"),
    ("ins-03", "blue",  "con un equipo", "con ejercicios de"),
    ("ins-04", "blue",  "para leer", "y ademas cada"),
    ("ins-05", "blue",  "clase en directo", "en dieciseis semanas"),
    ("ins-06", "blue",  "eres tu el", "sin tener que"),
]
OUTRO = "haz clic en"     # the enrolment block slides up over her from here to the end (she stays on screen)

def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", t)

def find(words, phrase, start=0):
    toks = phrase.split(); n = [norm(w["text"]) for w in words]
    for i in range(start, len(n) - len(toks) + 1):
        if n[i:i + len(toks)] == toks:
            return i
    raise SystemExit(f"not found: {phrase}")

def checked(take):
    W = json.load(open(os.path.join(ROOT, "tools", "align", f"align_{take}.json")))["words"]
    H = json.load(open(os.path.join(ROOT, "tools", "align", f"whisper_{take}.json")))
    sm = difflib.SequenceMatcher(a=[norm(w["text"]).replace(" ", "") for w in W], b=[norm(h[2]).replace(" ", "") for h in H], autojunk=False)
    pairs = [(m.a + k, m.b + k) for m in sm.get_matching_blocks() for k in range(m.size)]
    bias = statistics.median(W[i]["start"] - H[j][0] for i, j in pairs)
    fixed = 0
    for i, j in pairs:
        wt = H[j][0] + bias
        if abs(W[i]["start"] - wt) > 0.25:
            W[i] = dict(W[i], start=round(wt, 3)); fixed += 1
    for k in range(1, len(W)):                      # keep the order monotonic
        if W[k]["start"] <= W[k - 1]["start"]:
            W[k] = dict(W[k], start=round(W[k - 1]["start"] + 0.04, 3))
    print(f"take {take}: {fixed} word(s) moved to Whisper timing (bias {bias:+.3f})")
    return W

def main():
    AL = {t: checked(t) for t in {sg[0] for sg in SEGMENTS}}
    shots, words, t = [], [], 0.0
    for k, (tk, a, b) in enumerate(SEGMENTS):
        W = AL[tk]; dur = round((b - a) / RATE, 3)
        shots.append({"n": k + 1, "take": tk, "start": round(t, 3), "duration": dur, "media_start": a, "media_end": b,
                      "face": FACE[tk]})
        inside = [i for i, w in enumerate(W) if a - 0.12 <= w["start"] < b - 0.06]   # words audible in this segment
        for i in inside:
            w = W[i]; nxt = W[i + 1]["start"] if i + 1 < len(W) else b
            end = min(nxt, b, SPEECH_END if (k == len(SEGMENTS) - 1) else b)
            words.append({"shot": k + 1, "text": w["text"], "punct": w.get("punct", ""),
                          "t": round(t + max(0.0, w["start"] - a) / RATE, 3), "end": round(t + (end - a) / RATE, 3)})
        t = round(t + dur, 3)
    clip_end = t; total = round(clip_end + TAIL, 3)
    last = shots[-1]; speech_end = round(last["start"] + (SPEECH_END - last["media_start"]) / RATE, 3)
    lead = LEAD / RATE
    def find_t(phrase, after=0.0):
        toks = phrase.split(); n = [norm(w["text"]) for w in words]
        for i in range(len(n) - len(toks) + 1):
            if words[i]["t"] >= after and n[i:i + len(toks)] == toks:
                return words[i]["t"]
        raise SystemExit(f"not found: {phrase}")
    inserts = []
    for iid, ground, p0, p1 in INSERTS:
        a0 = find_t(p0); start = round(a0 - lead, 3)
        end = round(find_t(p1, a0) - lead, 3) if p1 else total
        inserts.append({"id": iid, "ground": ground, "start": start, "duration": round(end - start, 3)})
    girl, g = [], 0.0
    for ins in inserts:
        if ins["start"] > g + 1e-3:
            girl.append({"start": round(g, 3), "end": ins["start"]})
        g = round(ins["start"] + ins["duration"], 3)
    girl.append({"start": g, "end": total})
    outro = round(find_t(OUTRO) - lead, 3)
    json.dump({"rate": RATE, "clip_end": clip_end, "total": total, "speech_end": speech_end, "outro": outro,
               "hold": {"start": clip_end, "duration": TAIL}, "shots": shots, "inserts": inserts, "girl": girl, "words": words},
              open(os.path.join(ROOT, "edit.json"), "w"), ensure_ascii=False, indent=1)
    for sh in shots:
        print(f"  shot {sh['n']} take {sh['take']}  {sh['start']:6.2f}–{sh['start'] + sh['duration']:6.2f}  (source {sh['media_start']}–{sh['media_end']})")
    for gg in girl:
        print(f"  girl   {gg['start']:6.2f}–{gg['end']:6.2f}  " + " ".join(w["text"] for w in words if gg["start"] <= w["t"] < gg["end"]))
    for ins in inserts:
        a0, b0 = ins["start"], ins["start"] + ins["duration"]
        print(f"  {ins['id']} {a0:6.2f}–{b0:6.2f} ({ins['duration']:.2f}s, {ins['ground']})  " +
              " ".join(f"{w['text']}@{w['t'] - a0:.2f}" for w in words if a0 <= w["t"] < b0))
    print("outro block from", outro, "· clip end", clip_end, "· total", total, "· speech end", speech_end)

if __name__ == "__main__":
    main()
