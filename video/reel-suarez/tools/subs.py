#!/usr/bin/env python3
"""The subtitles: what is said, in short phrases (Dutch as said, Spanish under it), timed word by word from ElevenLabs
Scribe's transcript of the ad (.raw/scribe.json, word timestamps). The Dutch text is checked by ear against the client's
transcript (.raw/suarez.txt) and two Scribe passes; Suárez's own broken Dutch is kept as he says it («Suárez nooit zitten
op de bank»). The Spanish keeps the ad's puns: «fluiten» = to whistle → «pitar» (the referees whistle at him),
«bank» = sofa / the substitutes' bench → «banco / banquillo», «kaartje» = business card → «tarjeta» (yellow and red ones).
  python3 tools/subs.py      → subs.json (reel times: source time − T0)
"""
import difflib, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T0 = 135 / 25            # the reel starts at source frame 135 (Suárez walking in, after the ad's brand intro)
END = 40.08              # …and ends before the brand voice-over («Alleen bij …», 40.20)

# (who, Dutch, Spanish): m = the shop assistant, s = Suárez
PHRASES = [
    ("m", "Ah, een sportman", "Ah, un deportista"),
    ("m", "van Ajax.", "del Ajax."),
    ("m", "Ja, beroemde club.", "Sí, un club famoso."),
    ("m", "Cruijff, Keizer,", "Cruijff, Keizer,"),
    ("m", "Abe Lenstra.", "Abe Lenstra."),
    ("m", "Wat kan ik", "¿Qué puedo"),
    ("m", "voor u oplossen?", "hacer por usted?"),
    ("s", "Ja, ik hoorde iets", "Sí, oí algo"),
    ("s", "over één", "sobre un"),
    ("s", "anti-fluitregeling.", "control anti-pitidos."),
    ("m", "Ah, u bedoelt", "Ah, se refiere a"),
    ("m", "ons hoortoestel", "nuestro audífono"),
    ("m", "met geavanceerde", "con un avanzado"),
    ("m", "anti-fluitregeling.", "control anti-pitidos."),
    ("m", "Voorkomt dat u", "Evita que usted"),
    ("m", "irritante fluittonen hoort.", "oiga pitidos molestos."),
    ("s", "Ja, heel irritant.", "Sí, muy molesto."),
    ("s", "Zij fluiten", "Ellos pitan"),
    ("s", "veel te vaak", "demasiadas veces"),
    ("s", "tegen mij.", "contra mí."),
    ("m", "Oh, maar dan is", "Oh, pero entonces"),
    ("m", "dit model niks voor u.", "este modelo no es para usted."),
    ("m", "Gaan wij naar ons", "Vamos a nuestra"),
    ("m", "oordopjesgamma.", "gama de tapones."),
    ("m", "Neemt u maar even", "Siéntese un momento"),
    ("m", "op de bank plaats.", "en el banco."),
    ("s", "Hè?", "¿Eh?"),
    ("s", "Suárez nooit", "Suárez nunca"),
    ("s", "zitten op de bank.", "se sienta en el banquillo."),
    ("m", "Nou, veel succes ermee.", "Bueno, mucha suerte."),
    ("m", "En mocht u nog", "Y si vuelve a"),
    ("m", "een fluitje horen,", "oír un pitido,"),
    ("m", "gewoon even langskomen.", "pásese por aquí."),
    ("m", "Kaartje?", "¿Una tarjeta?"),
    ("s", "Nee, nee,", "No, no,"),
    ("s", "ik heb kaartjes genoeg.", "tengo tarjetas de sobra."),
]


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def main():
    sc = [w for w in json.load(open(os.path.join(ROOT, ".raw", "scribe.json")))["words"]
          if w.get("type") == "word" and T0 - 0.2 <= w["start"] < END]
    A = [(p, w) for p, (_, nl, _) in enumerate(PHRASES) for w in nl.split()]
    a, b = [norm(w) for _, w in A], [norm(w["text"]) for w in sc]
    times = [None] * len(A)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (sc[j1 + k]["start"], sc[j1 + k]["end"])
        elif tag == "replace":                                   # same span, other spelling: share its time out
            s0, s1 = sc[j1]["start"], sc[j2 - 1]["end"]
            n = i2 - i1
            for k in range(n):
                times[i1 + k] = (s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n)
    for k in range(len(times)):                                  # a word Scribe did not hear: between its neighbours
        if times[k] is None:
            prev = next((times[j][1] for j in range(k - 1, -1, -1) if times[j]), T0)
            nxt = next((times[j][0] for j in range(k + 1, len(times)) if times[j]), prev + 0.3)
            times[k] = (prev, max(prev + 0.08, min(nxt, prev + 0.3)))
    out = []
    for p, (who, nl, es) in enumerate(PHRASES):
        ws = [(w, times[k]) for k, (pp, w) in enumerate(A) if pp == p]
        out.append({"who": who, "es": es, "words": [{"text": w, "t": round(t[0] - T0, 3), "end": round(t[1] - T0, 3)} for w, t in ws]})
    unheard = [A[k][1] for k in range(len(A)) if not any(abs(times[k][0] - w["start"]) < 1e-6 for w in sc)]
    json.dump({"t0": T0, "end": END, "phrases": out}, open(os.path.join(ROOT, "subs.json"), "w"), ensure_ascii=False, indent=1)
    print(f"subs.json: {len(out)} phrases, {len(A)} words; respelled/unheard (timed from neighbours): {unheard}")


if __name__ == "__main__":
    main()
