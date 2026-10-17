#!/usr/bin/env python3
"""Edit decision list → edit.json (UGC #2, «Si tienes un ordenador…»).

Two takes of the same script: take 1 = UGC.POV1, facing camera (with two hook takes and a laptop); take 2 =
UGC.POV2, the side camera (interview look: she talks towards the front camera — until the call to action, where she
turns to the side camera, points and talks into it). The ad is the front camera from start to finish (the client
prefers her talking to us); the side camera comes in only for the ending, where she looks into it: «rellena el
formulario» · «y una persona de nuestro equipo te atenderá» (jump cut over her pause).
The first hook take is used (the second one stops for three seconds in the middle). Every cut sits in a quiet point
checked on the energy envelope, all at RATE (pitch preserved). The long pause before «¿Estás listo…?» is removed at
the cut back from the last insert, where the jump is hidden.

Word times: Whisper word timestamps of each take (tools/align/whisper_<take>.json), shifted by WHISPER_BIAS (its
onsets land ~0.15 s late on these takes, checked against the energy envelope at every cut).
"""
import json, os, unicodedata, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.06
WHISPER_BIAS = -0.15
# (take, source in, source out) — hand-checked quiet points
SEGMENTS = [
    ("1", 0.55, 5.80),     # front · hook: «Si tienes un ordenador y ganas de aprender neerlandés, ya tienes todo lo que necesitas para empezar.»
    ("1", 15.30, 66.56),   # front · «En cuatro semanas…» → «…como requisito el neerlandés.»
    ("1", 66.94, 70.70),   # front · «¿Estás listo para comenzar? Si es así, haz clic en el botón de aquí abajo,» (no real pause
                           #          before «rellena» in this take: cut in the dip right after «abajo», a longer fade in gen.py)
    ("2", 70.84, 72.25),   # side, looking into it: «rellena el formulario»
    ("2", 74.50, 76.70),   # side, looking into it: «y una persona de nuestro equipo te atenderá» (her 2 s pause cut); the ad
                           #          ends a breath after her last word
]
FACE = {"1": (540, 720), "2": (450, 690)}   # face centre in each take (zoom origin)
# cuts already inside the takes (the creator's own edit between sentences), source second of the first new frame —
# found by a frame-difference scan, timed on the decoded frames' own timestamps. When one falls just after a graphic
# ends or just before one starts, the graphic covers it (no flash of the old picture before the jump); one well inside
# a girl section becomes a shot boundary with a reframe in gen.py, so it reads as a jump cut.
CUT_PRE, CUT_POST = 0.05, 0.005
JUMPS = {"1": [21.0, 28.3, 32.6, 37.9, 41.6, 43.933, 51.133, 53.6, 56.5, 58.0, 59.5, 61.8, 66.6, 70.8],   # exact frame pts
         "2": []}
SPEECH_END = 76.50     # «…atenderá» ends here in take 2; the shot runs on a breath (to 76.70) and the ad ends
TAIL = 0.0             # no held frame after the take: the ad ends when she stops talking (v7)
LEAD = 0.06            # an insert cuts in this long before its first word (source seconds)
# (insert id, ground, first words, first words of what comes after)
INSERTS = [
    ("ins-01", "blue",  "ya puedes presentarte", "vivimos en un"),
    ("ins-02", "paper", "el ingles te saca", "el principal error"),
    ("ins-03", "blue",  "cuando te lo explican", "en nawar practicas"),
    ("ins-04", "blue",  "con situaciones que", "aprendes con lecciones"),
    ("ins-05", "blue",  "por un equipo", "para estudiar cuando"),
    ("ins-06", "blue",  "ejercicios", "y cada semana"),
    ("ins-07", "blue",  "clase en directo", "ademas mientras las"),
    ("ins-08", "paper", "nueve de cada", "estas listo para"),
]
OUTRO = "haz clic en"  # the «haz clic» button pops under her face from here to the end (she stays on screen)

FIX = {"nerlandés,": "neerlandés,", "nerlandés": "neerlandés", "elnerlandés": "el neerlandés", "nirlandés.": "neerlandés.",
       "our": "Nawar", "NowHard": "Nawar", "colecciones": "con lecciones", "teoria": "teoría", "10": "diez", "9": "nueve",
       "ofertes": "ofertas", "nerlandes": "neerlandés"}


def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", t)


def words_of(take):
    """Whisper words of a take as [{text, punct, start}], misheard words fixed, glued words split."""
    out = []
    for a, b, t in json.load(open(os.path.join(ROOT, "tools", "align", f"whisper_{take}.json"))):
        t = t.strip(); m = re.match(r"^([¿¡]?)(.*?)([.,:;?!]*)$", t); pre, core, punct = m.group(1), m.group(2), m.group(3)
        fixed = FIX.get(core + punct, FIX.get(core, core)).rstrip(".,")
        parts = fixed.split(" ")
        for k, p in enumerate(parts):
            out.append({"text": (pre if k == 0 else "") + p, "punct": punct if k == len(parts) - 1 else "",
                        "start": round(a + WHISPER_BIAS + k * 0.12, 3)})
    return out


def layout(AL, segs):
    """shots and timed words for a list of (take, from, to) pieces played back to back."""
    shots, words, t, taken = [], [], 0.0, set()
    for k, (tk, a, b) in enumerate(segs):
        W = AL[tk]; a = round(a, 3); b = round(b, 3); dur = round((b - a) / RATE, 3)
        shots.append({"n": k + 1, "take": tk, "start": round(t, 3), "duration": dur, "media_start": a, "media_end": b,
                      "face": FACE[tk]})
        inside = [i for i, w in enumerate(W) if a - 0.12 <= w["start"] < b - 0.06 and (tk, i) not in taken]
        taken.update((tk, i) for i in inside)          # a word at a cut inside a take belongs to one shot only
        for i in inside:
            w = W[i]; nxt = W[i + 1]["start"] if i + 1 < len(W) else b
            end = min(nxt, b, SPEECH_END if k == len(segs) - 1 else b)
            words.append({"shot": k + 1, "text": w["text"], "punct": w["punct"],
                          "t": round(t + max(0.0, w["start"] - a) / RATE, 3), "end": round(t + (end - a) / RATE, 3)})
        t = round(t + dur, 3)
    return shots, words, t


def edit_time(shots, tk, m):
    """edit time where source second m of take tk is on screen (None if that moment is not in the edit)."""
    for sh in shots:
        if sh["take"] == tk and sh["media_start"] - 1e-6 <= m <= sh["media_end"] + 1e-6:
            return round(sh["start"] + (m - sh["media_start"]) / RATE, 3)
    return None


def place_inserts(shots, words, total, cover):
    """insert windows from their phrases; an edge leans on a boundary between pieces (≤0.25 s away), and a cut inside
    a take (`cover`, edit times) that falls just after an insert ends or just before one starts is covered by the
    insert, one frame past it — the girl never shows the last frames of one clip and then jumps."""
    lead = LEAD / RATE
    def find_t(phrase, after=0.0):
        toks = phrase.split(); n = [norm(w["text"]) for w in words]
        for i in range(len(n) - len(toks) + 1):
            if words[i]["t"] >= after and n[i:i + len(toks)] == toks:
                return words[i]["t"]
        raise SystemExit(f"not found: {phrase}")
    starts = [s["start"] for s in shots[1:]]
    inserts = []
    for iid, ground, p0, p1 in INSERTS:
        a0 = find_t(p0); start = round(a0 - lead, 3)
        end = round(find_t(p1, a0) - lead, 3) if p1 else total
        near = [x for x in starts if end - 0.25 <= x <= end + 0.25]
        if near:
            end = min(near, key=lambda x: abs(x - end))
        prev_end = inserts[-1]["start"] + inserts[-1]["duration"] if inserts else 0.0
        for c in cover:
            if end - 0.1 <= c <= end + 0.35:
                end = round(c + 1 / 30, 3)
            if start - 0.35 <= c < start + 0.05 and c - 1 / 30 > prev_end + 0.5:
                start = round(c - 1 / 30, 3)
        inserts.append({"id": iid, "ground": ground, "start": start, "duration": round(end - start, 3)})
    return inserts, find_t


def girl_of(inserts, total):
    girl, g = [], 0.0
    for ins in inserts:
        if ins["start"] > g + 1e-3:
            girl.append({"start": round(g, 3), "end": ins["start"]})
        g = round(ins["start"] + ins["duration"], 3)
    girl.append({"start": g, "end": total})
    return girl


def main():
    AL = {t: words_of(t) for t in {sg[0] for sg in SEGMENTS}}
    # pass 1, the takes as cut: where do the takes' own cuts fall?
    shots, words, t = layout(AL, SEGMENTS)
    jumps = [(tk, j) for tk, a, b in SEGMENTS for j in JUMPS.get(tk, []) if a + 0.1 < j < b - 0.1]
    at = {jk: edit_time(shots, *jk) for jk in jumps}
    inserts, _ = place_inserts(shots, words, round(t + TAIL, 3), [at[jk] for jk in jumps])
    girl = girl_of(inserts, round(t + TAIL, 3))
    # a cut well inside a girl section stays visible: split there and reframe (gen.py). The piece before stops CUT_PRE
    # short of it and the next one reads from just past it — the renderer can land a frame either side of a boundary,
    # so this keeps the new picture and its new framing on the same frame (those cuts sit in pauses: nothing is lost)
    split = {jk for jk in jumps if any(g["start"] + 0.3 < at[jk] < g["end"] - 0.3 for g in girl)}
    segs = []
    for tk, a, b in SEGMENTS:
        cuts = sorted(j for (k, j) in split if k == tk and a < j < b)
        froms = [a] + [j + CUT_POST for j in cuts]
        tos = [j - CUT_PRE for j in cuts] + [b]
        segs += list(zip([tk] * len(froms), froms, tos))
    # pass 2, the final pieces
    shots, words, t = layout(AL, segs)
    clip_end = t; total = round(clip_end + TAIL, 3)
    last = shots[-1]; speech_end = round(last["start"] + (SPEECH_END - last["media_start"]) / RATE, 3)
    cover = [edit_time(shots, tk, j) for (tk, j) in jumps if (tk, j) not in split]
    inserts, find_t = place_inserts(shots, words, total, [c for c in cover if c is not None])
    girl = girl_of(inserts, total)
    lead = LEAD / RATE
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
    print("outro from", outro, "· clip end", clip_end, "· total", total, "· speech end", speech_end)


if __name__ == "__main__":
    main()
