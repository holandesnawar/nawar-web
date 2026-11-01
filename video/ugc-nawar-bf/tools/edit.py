#!/usr/bin/env python3
"""Edit decision list → edit.json (UGC Black Friday, «Si vives en Países Bajos…» · the 1 € book).

Two files of the same girl, same room and framing: take g = «intro gancho» (three hook variants; this version uses the
one from second 15, «Si vives en Países Bajos y para cualquier trámite necesitas que alguien te acompañe, este Black
Friday te interesa» — its full second take, at 17.6 s; the first one is half-said with the mic down), take p = «Estado
de pedido» (the body, already cut by the creator, with two takes of the opening line). The opening is the first take
up to «la cambias» (it says «ir contigo», so «acompañar» isn't said twice after the hook) and the second take from
«algo que en tu país lo hacías solo y ni lo pensabas» (richer ending), then the body to the end. Every cut sits in a
quiet point checked on the energy envelope, all at RATE (pitch preserved).

Word times: tools/align/whisper_<take>.json, Whisper words fixed and re-timed by tools/align_fix.py.
"""
import json, os, unicodedata, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.06
WHISPER_BIAS = 0.0         # align_fix.py already moved the words onto the voice
# (take, source in, source out) — hand-checked quiet points
SEGMENTS = [
    ("g", 17.60, 23.92),   # hook: «Si vives en Países Bajos y para cualquier trámite necesitas que alguien te acompañe, este Black
                           #        Friday te interesa.»
    ("p", 0.95, 5.62),     # «Antes de pedir cita, miras quién puede ir contigo, y si ese día no puede nadie, la cambias.»
    ("p", 12.905, 49.80),  # «Algo que en tu país lo hacías solo y ni lo pensabas.» → «…nuestra lista prioritaria del Black Friday.»
]
FACE = {"g": (570, 660), "p": (560, 720)}   # face centre in each take (zoom origin)
# cuts already inside the takes (the creator's own edit), source second of the first new frame (frame-difference scan
# on the decoded frames). Next to a graphic's edge the graphic covers it; well inside a girl section it becomes a shot
# boundary with a reframe in gen.py, so it reads as a jump cut.
CUT_PRE, CUT_POST = 0.05, 0.005
CUT_PRE_AT = {("p", 15.6): 0.02}   # «pensabas»: its /s/ fades right up to the take's own cut — stop closer to it
JUMPS = {"g": [16.633], "p": [3.567, 7.567, 12.9, 15.6, 20.0, 24.5, 36.7, 39.767, 44.7]}
SPEECH_END = 49.74     # «…del Black Friday.» ends here in take p; the ad ends a breath later
TAIL = 0.0
LEAD = 0.06            # an insert cuts in this long before its first word (source seconds)
# (insert id, ground, first words, first words of what comes after) — full-screen graphics while she explains
INSERTS = [
    ("ins-01", "dark", "miras quien puede", "algo que en"),
    ("ins-02", "dark", "cada vez que", "practicar por tu"),
    ("ins-03", "dark", "porque casi todo", "por eso hemos"),
    ("ins-04", "dark", "este libro", "entero por un"),
]
HOOK_BF = "black friday te"    # the «BLACK FRIDAY» sticker slams in on the hook
OFFER = "entero por un"        # the price stickers over her, from here to the call to action
OUTRO = "consigue el tuyo"     # the button under her face, from here to the end

FIX = {}
# the script as she says it, with its punctuation and capitals (Whisper's words carry almost none): one token per word
SCRIPT = ("Si vives en Países Bajos y para cualquier trámite necesitas que alguien te acompañe, este Black Friday te interesa. "
          "Antes de pedir cita, miras quién puede ir contigo, y si ese día no puede nadie, la cambias. "
          "Algo que en tu país lo hacías solo y ni lo pensabas. "
          "Eso no se arregla con los años. Cada vez que alguien habla por ti, tú te quedas sin practicar. "
          "Practicar por tu cuenta tampoco es fácil, porque casi todo lo que encuentras está en inglés. "
          "Por eso hemos creado este libro: 70 páginas en español, para imprimir, con vocabulario, gramática, ejercicios prácticos, "
          "cómo pronunciar los sonidos por los que te cambian en inglés cuando abres la boca. "
          "Entero por un euro, solo hasta el 30 de noviembre. Esta es una de nuestras ofertas del Black Friday. "
          "Consigue el tuyo en el enlace abajo, y al conseguirlo entras directamente en nuestra lista prioritaria del Black Friday.").split()


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
        tos = [j - CUT_PRE_AT.get((tk, j), CUT_PRE) for j in cuts] + [b]
        segs += list(zip([tk] * len(froms), froms, tos))
    # pass 2, the final pieces
    shots, words, t = layout(AL, segs)
    if len(SCRIPT) != len(words):
        raise SystemExit(f"SCRIPT has {len(SCRIPT)} words, the edit {len(words)}: " + " ".join(w["text"] for w in words))
    for w, tok in zip(words, SCRIPT):                  # same words, now with the script's punctuation and capitals
        m = re.match(r"^([¿¡]?)(.*?)([.,:;?!]*)$", tok)
        if norm(m.group(2)) != norm(w["text"]):
            raise SystemExit(f"SCRIPT «{tok}» ≠ edit «{w['text']}» at {w['t']}")
        w["text"], w["punct"] = m.group(1) + m.group(2), m.group(3)
    clip_end = t; total = round(clip_end + TAIL, 3)
    last = shots[-1]; speech_end = round(last["start"] + (SPEECH_END - last["media_start"]) / RATE, 3)
    cover = [edit_time(shots, tk, j) for (tk, j) in jumps if (tk, j) not in split]
    inserts, find_t = place_inserts(shots, words, total, [c for c in cover if c is not None])
    girl = girl_of(inserts, total)
    lead = LEAD / RATE
    outro = round(find_t(OUTRO) - lead, 3)
    hook_bf = find_t(HOOK_BF); offer = round(find_t(OFFER) - lead, 3)
    json.dump({"rate": RATE, "clip_end": clip_end, "total": total, "speech_end": speech_end, "outro": outro,
               "hook_bf": hook_bf, "offer": offer,
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
    print("hook BF at", hook_bf, "· offer from", offer, "· outro from", outro, "· clip end", clip_end, "· total", total,
          "· speech end", speech_end)


if __name__ == "__main__":
    main()
