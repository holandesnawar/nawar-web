#!/usr/bin/env python3
"""Edit decision list → edit.json (UGC #4, «Nuestro Black Friday empieza hoy» · the 1 € book and the priority list).

One file, take p = «Estado de pedido FO4233» (4 nov): the whole ad, with retakes the creator left in. The best of each:
  · the hook three times — the first one (her air-quote hands on the very first frame, the liveliest: SEGMENTS[0]);
  · «…y no es falta de ganas…» twice — the second one (higher and livelier: median pitch 254 Hz against 208, a wider
    range; it carries one of the creator's own jump cuts, at 38.8, which becomes a cut with a new framing);
  · «Si empiezas ya, en Navidad…» twice — the second one («…cosas que antes se te escapaban», the better line, also the
    livelier one) — not «…que antes ni sabías»;
  · «Quien lo consiga entra en nuestra lista prioritaria…» — the last, whole one (the two before it stop half-way);
  · «Solo hasta el 30 de noviembre» twice — the first one (her hand at her mouth, as if telling a secret; the widest
    pitch range of the two).
Every cut sits in a quiet point checked on the energy envelope (or on one of the creator's own cuts), all at RATE (pitch
preserved). Word times: tools/align/whisper_p.json (Scribe words, tools/align_fix.py).
"""
import json, os, unicodedata, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 1.06
WHISPER_BIAS = 0.0         # align_fix.py already moved the words onto the voice
# (take, source in, source out) — hand-checked quiet points
SEGMENTS = [
    ("p", 0.44, 4.86),     # hook: «Nuestro Black Friday empieza hoy. Sí, antes de tiempo.» (take 1 of 3)
    ("p", 15.02, 19.86),   # «¿Por qué tan pronto? Porque cada mes que esperas es otro mes pidiendo que te traduzcan.»
    ("p", 21.56, 26.70),   # «En la pausa del trabajo, alguien dice algo, todos se ríen y tú sonríes sin saber de qué.»
    ("p", 26.98, 31.04),   # «Te dices que en enero empiezas, pero llega enero, luego febrero,» (up to the creator's cut at 31.067)
    ("p", 37.12, 41.445),  # «y no es falta de ganas, es que siempre hay un motivo para que empieces el mes que viene.» (2nd take)
    ("p", 41.78, 43.36),   # «Por eso lo abrimos ahora.»
    ("p", 50.96, 55.28),   # «Si empiezas ya, en Navidad vas a entender cosas que antes se te escapaban.» (2nd take)
    ("p", 55.40, 61.88),   # «La primera oferta: nuestro libro en neerlandés para principiantes, explicado en español, por solo un euro.»
    ("p", 65.92, 72.88),   # «Quien lo consiga entra en nuestra lista prioritaria y sabrá lo que estaremos preparando…antes que nadie.»
    ("p", 72.93, 76.96),   # «Apúntate en el enlace de abajo y llévate el libro por solo un euro.»
    ("p", 78.64, 80.62),   # «Solo hasta el 30 de noviembre.» (1st take)
]
FACE = {"p": (560, 660)}   # her face centre (zoom origin)
# cuts already inside the take (the creator's own edit), source second of the first new frame (frame-difference scan
# on the decoded frames). Next to a graphic's edge the graphic covers it; well inside a girl section it becomes a shot
# boundary with a reframe in gen.py, so it reads as a jump cut.
CUT_PRE, CUT_POST = 0.05, 0.005
CUT_PRE_AT = {}
JUMPS = {"p": [14.533, 21.3, 31.067, 38.8, 41.467, 44.133, 55.3, 61.9, 72.9]}
# tighter: every pause between two words longer than TIGHT (her voice under LOUD_DB, measured on the take's own sound)
# is cut down to KEEP_TAIL after the last word + KEEP_HEAD before the next; a take's own cut that sits in such a silence
# becomes a cut of the edit there too (and inside a girl section, a jump cut with a new framing).
TIGHT, KEEP_TAIL, KEEP_HEAD, LOUD_DB = 0.18, 0.05, 0.04, -30.0
PAUSE = {}
TAIL_AT = {}
NO_TIGHT = {0}         # (segment index) the hook stays one continuous shot (her opening zoom and its beat after «hoy»)
CUT_POST_AT = {}
SPEECH_END = 80.57     # «…30 de noviembre.» ends here in take p
TAIL = 0.30            # her last frame held under the button (gen.py), the music fades on it
LEAD = 0.06            # an insert cuts in this long before its first word (source seconds)
# (insert id, ground, first words, first words of what comes after) — full-screen graphics while she explains
INSERTS = [
    ("ins-01", "paper", "porque cada mes", "en la pausa"),          # another month asking to be translated for
    ("ins-02", "blue", "alguien dice algo", "te dices que"),        # the break at work: everyone laughs, you smile
    ("ins-03", "paper", "pero llega enero", "y no es"),              # the calendar: «empezar neerlandés» moves on and on
    ("ins-04", "paper", "en navidad vas", "la primera oferta"),      # by Christmas you understand
    ("ins-05", "blue", "nuestro libro en", "quien lo consiga"),      # the ebook, 1 €
    ("ins-06", "paper", "lista prioritaria y", "apuntate en el"),    # the priority list: first to know
]
HOOK_BF = "black friday empieza"   # the opening line (a light «Black Friday» tag on the hook)
TURN = "por que tan"               # the music's groove comes in here, right after the hook
OFFER = "la primera oferta"        # the offer part starts here
OUTRO = "apuntate en el"           # the button under her face, from here to the end

FIX = {}
# the script as she says it, with its punctuation and capitals (Whisper's words carry almost none): one token per word
SCRIPT = ("Nuestro Black Friday empieza hoy. Sí, antes de tiempo. ¿Por qué tan pronto? Porque cada mes que esperas es otro mes "
          "pidiendo que te traduzcan. En la pausa del trabajo, alguien dice algo, todos se ríen y tú sonríes sin saber de qué. "
          "Te dices que en enero empiezas, pero llega enero, luego febrero, y no es falta de ganas, es que siempre hay un motivo "
          "para que empieces el mes que viene. Por eso lo abrimos ahora. Si empiezas ya, en Navidad vas a entender cosas que "
          "antes se te escapaban. La primera oferta: nuestro libro en neerlandés para principiantes, explicado en español, por "
          "solo un euro. Quien lo consiga entra en nuestra lista prioritaria y sabrá lo que estaremos preparando para este Black "
          "Friday antes que nadie. Apúntate en el enlace de abajo y llévate el libro por solo un euro. Solo hasta el 30 de "
          "noviembre.").split()


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


def envelope(tk, _cache={}):
    """loudness of take tk's sound every 10 ms (dB RMS)."""
    if tk not in _cache:
        import subprocess, numpy as np
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, "assets", "video", f"take-{tk}.mp4"), "-ac", "1",
                              "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32); n = len(x) // 160
        _cache[tk] = 20 * np.log10(np.sqrt(np.mean(x[:n * 160].reshape(n, 160) ** 2, 1)) + 1e-9)
    return _cache[tk]


def tighten(tk, a, b, k=None):
    """(take, from, to) → pieces (take, from, to, pause before) with the long pauses cut out (see TIGHT); also returns the
    take's own cuts that became cuts of the edit."""
    import numpy as np
    if k in NO_TIGHT:
        return [(tk, a, b, 0.0)], set()
    db = envelope(tk)
    W = [w for w in json.load(open(os.path.join(ROOT, "tools", "align", f"whisper_{tk}.json"))) if a - 0.05 <= w[0] < b]
    cuts, used = [], set()
    for w0, w1 in zip(W, W[1:]):
        i0, i1 = int(w0[0] * 100), int(w1[0] * 100)
        loud = np.flatnonzero(db[i0:i1] > LOUD_DB)
        tail = (i0 + loud[-1] + 1) / 100 if len(loud) else w0[0]
        onset = w1[0]
        js = [j for j in JUMPS.get(tk, []) if tail - 0.02 <= j <= onset]
        if onset - tail < TIGHT and not js:
            continue
        e, s = tail + KEEP_TAIL, onset - KEEP_HEAD
        e = min(max(e, TAIL_AT.get((tk, round(w0[0], 3)), 0.0)), s)
        if js:
            e, s = min(e, js[0] - CUT_PRE_AT.get((tk, js[0]), 0.02)), max(s, js[0] + CUT_POST_AT.get((tk, js[0]), CUT_POST))
            used.add((tk, js[0]))
        pause = (PAUSE.get((tk, js[0]), 0.0) if js else 0.0) or PAUSE.get((tk, round(w0[0], 3)), 0.0)   # at a take's cut, or
        cuts.append((round(e, 3), round(s, 3), pause))                                               # after a given word
    pieces, x, pause = [], a, 0.0
    for e, s, p in cuts:
        pieces.append((tk, round(x, 3), e, pause)); x, pause = s, p
    pieces.append((tk, round(x, 3), b, pause))
    return pieces, used


def layout(AL, segs):
    """shots and timed words for a list of (take, from, to[, pause before]) pieces played back to back."""
    shots, words, t, taken = [], [], 0.0, set()
    for k, seg in enumerate(segs):
        tk, a, b = seg[:3]; t = round(t + (seg[3] if len(seg) > 3 else 0.0), 3)
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
    # the long pauses out; the takes' own cuts that sit in a pause become cuts of the edit
    segs0, cut_at = [], set()
    for k, (tk, a, b) in enumerate(SEGMENTS):
        pieces, used = tighten(tk, a, b, k); segs0 += pieces; cut_at |= used
    # pass 1, the takes as cut: where do the takes' own cuts fall?
    shots, words, t = layout(AL, segs0)
    jumps = [(tk, j) for tk, a, b in SEGMENTS for j in JUMPS.get(tk, []) if a + 0.1 < j < b - 0.1 and (tk, j) not in cut_at]
    at = {jk: edit_time(shots, *jk) for jk in jumps}
    inserts, _ = place_inserts(shots, words, round(t + TAIL, 3), [at[jk] for jk in jumps])
    girl = girl_of(inserts, round(t + TAIL, 3))
    # a cut well inside a girl section stays visible: split there and reframe (gen.py). The piece before stops CUT_PRE
    # short of it and the next one reads from just past it — the renderer can land a frame either side of a boundary,
    # so this keeps the new picture and its new framing on the same frame (those cuts sit in pauses: nothing is lost)
    split = {jk for jk in jumps if any(g["start"] + 0.3 < at[jk] < g["end"] - 0.3 for g in girl)}
    segs = []
    for tk, a, b, pause in segs0:
        cuts = sorted(j for (k, j) in split if k == tk and a < j < b)
        froms = [a] + [j + CUT_POST for j in cuts]
        tos = [j - CUT_PRE_AT.get((tk, j), CUT_PRE) for j in cuts] + [b]
        segs += [(tk, f, e, pause if n == 0 else 0.0) for n, (f, e) in enumerate(zip(froms, tos))]
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
    hook_bf = find_t(HOOK_BF); offer = round(find_t(OFFER) - lead, 3); turn = find_t(TURN)
    json.dump({"rate": RATE, "clip_end": clip_end, "total": total, "speech_end": speech_end, "outro": outro,
               "hook_bf": hook_bf, "offer": offer, "turn": turn,
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
