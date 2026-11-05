"""ins-02 · «(En la pausa del trabajo,) alguien dice algo, todos se ríen y tú sonríes sin saber de qué.» — on Nawar blue,
the coffee break: the «Pausa del trabajo» pill (cup icon) on top; on «dice algo» Mark's white bubble says, in quick,
idiomatic Dutch, «En toen stond hij met z'n mond vol tanden!» (and then he was left speechless — an idiom a beginner
doesn't catch); on «todos se ríen» the three colleagues laugh (a «Hahaha» pill bounces over each); on «tú sonríes» you
come in under them — your blue avatar with an awkward smile — and on «sin saber de qué» a thought cloud with a big «?»
floats up beside you. Dutch checked with the Dutch content checker (native idiom, informal «z'n»)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

MATES = [("Mark", "#7C5CFF", 110), ("Sanne", "#15A3A3", 410), ("Joost", "#D9487A", 710)]
CUP = ('<svg viewBox="0 0 48 48"><g fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="M8 18 H34 V30 A10 10 0 0 1 24 40 H18 A10 10 0 0 1 8 30 Z"/><path d="M34 22 H38 A5 5 0 0 1 38 32 H34"/>'
       '<path d="M16 6 C14 9 18 10 16 13 M24 6 C22 9 26 10 24 13"/></g></svg>')


def face(bg, mood):
    """a round avatar face: «laugh» (closed eyes, open laughing mouth) or «awk» (open eyes, a small tight smile)."""
    if mood == "laugh":
        f = ('<path d="M30 40 Q36 34 42 40" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
             '<path d="M54 40 Q60 34 66 40" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
             '<path d="M28 54 H68 Q66 74 48 74 Q30 74 28 54 Z" fill="#FFFFFF"/>')
    else:
        f = ('<circle cx="35" cy="40" r="5" fill="#FFFFFF"/><circle cx="61" cy="40" r="5" fill="#FFFFFF"/>'
             '<path d="M34 60 Q48 66 62 58" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
             '<path d="M70 22 Q74 30 70 34 Q66 30 70 22 Z" fill="#9FD4FF"/>')
    return f'<svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="48" fill="{bg}"/>{f}</svg>'


def build():
    iid, P = "ins-02", "i2"; d = INS[iid]["duration"]
    c = dict(DICE=cue(iid, "dice"), TODOS=cue(iid, "todos"), RIEN=cue(iid, "rien"), TU=cue(iid, "tu"), SON=cue(iid, "sonries"),
             SIN=cue(iid, "sin"), QUE=cue(iid, "que"))
    css = """
    #i2-krow { top: 170px; }
    #i2-kick { height: 68px; padding: 0 30px 0 22px; font-size: 27px; }
    #i2-kick svg { width: 34px; height: 34px; }
    #i2-say { left: 100px; top: 290px; font-size: 48px; transform-origin: 0% 100%; }
    #i2-say b { font-weight: 700; color: «INDIGO»; }
    .i2-mate { position: absolute; top: 570px; width: 260px; height: 300px; }
    .i2-av { position: absolute; left: 50px; top: 76px; width: 160px; height: 160px; border-radius: 50%; overflow: hidden;
      box-shadow: 0 0 0 7px rgba(255,255,255,0.9); }
    .i2-av svg { display: block; width: 160px; height: 160px; }
    .i2-name { position: absolute; left: 0; top: 262px; width: 260px; text-align: center; font-family: "Inter", sans-serif; font-weight: 700;
      font-size: 28px; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(255,255,255,0.85); }
    .i2-ha { position: absolute; left: 35px; top: -6px; width: 190px; height: 64px; border-radius: 999px; background: #FFFFFF; color: «INDIGO»;
      display: flex; align-items: center; justify-content: center; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 32px;
      transform-origin: 50% 100%; }
    #i2-me { position: absolute; left: 270px; top: 920px; width: 560px; height: 260px; }
    #i2-meav { position: absolute; left: 0; top: 0; width: 190px; height: 190px; border-radius: 50%; overflow: hidden;
      box-shadow: 0 0 0 8px #FFFFFF; }
    #i2-meav svg { display: block; width: 190px; height: 190px; }
    #i2-mename { position: absolute; left: 55px; top: 212px; }
    #i2-cloud { position: absolute; left: 250px; top: -36px; width: 270px; height: 200px; transform-origin: 0% 100%; }
    #i2-cloud svg { position: absolute; left: 0; top: 0; width: 270px; height: 200px; }
    #i2-qm { position: absolute; left: 0; top: 10px; width: 270px; height: 140px; text-align: center; font-family: "Poppins", sans-serif;
      font-weight: 900; font-size: 112px; line-height: 140px; color: «INDIGO»; }
"""
    mates = "\n".join(f"""    <div id="i2-m{k}" class="i2-mate" style="left: {x}px;"><div class="i2-av">{face(col, 'laugh')}</div>
      <div class="i2-name">{n}</div><div id="i2-ha{k}" class="i2-ha">Hahaha</div></div>""" for k, (n, col, x) in enumerate(MATES))
    cloud = ('<svg viewBox="0 0 230 170"><g fill="#FFFFFF"><circle cx="70" cy="70" r="52"/><circle cx="130" cy="56" r="56"/>'
             '<circle cx="178" cy="84" r="44"/><circle cx="110" cy="100" r="50"/><circle cx="40" cy="132" r="13"/><circle cx="18" cy="156" r="8"/></g></svg>')
    body = "\n".join([ground(P, "blue"), f"""    <div id="i2-krow" class="i2-row"><div id="i2-kick" class="i2-pill">{CUP}<span>Pausa del trabajo</span></div></div>
    <div id="i2-say" class="i2-bub i2-bub-w i2-bl"><b>Mark</b><br/>En toen stond hij met z'n<br/>mond vol tanden!</div>
{mates}
    <div id="i2-me"><div id="i2-meav">{face('«BLUE»', 'awk')}</div><div id="i2-mename" class="i2-ipill" style="position: absolute;">TÚ</div>
      <div id="i2-cloud">{cloud}<div id="i2-qm">?</div></div></div>"""])
    js = """
      tl.fromTo(q("kick"), { opacity: 0.4, y: -10 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      tl.fromTo(q("m0"), { opacity: 0.4, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("m1"), { opacity: 0.4, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.04);
      tl.fromTo(q("m2"), { opacity: 0.4, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.08);
      tl.fromTo(q("say"), { opacity: 0, scale: 0.8, y: 18 }, { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, «DICE» - 0.1);
"""
    for k in range(3):
        t = round(c["TODOS"] + 0.06 + 0.12 * k, 3)
        js += f'      tl.fromTo(q("ha{k}"), {{ opacity: 0, scale: 0.5, y: 10 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.24, ease: "back.out(2.2)" }}, {t});\n'
        js += (f'      tl.fromTo(q("ha{k}"), {{ rotation: 0 }}, {{ keyframes: [{{ rotation: -6, duration: 0.12 }}, {{ rotation: 5, duration: 0.14 }}, '
               f'{{ rotation: -3, duration: 0.14 }}, {{ rotation: 0, duration: 0.12 }}], immediateRender: false }}, {round(t + 0.24, 3)});\n')
    js += """      tl.fromTo(q("me"), { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }, «TU» - 0.06);
      tl.fromTo(q("cloud"), { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.32, ease: "back.out(1.8)" }, «SIN» - 0.04);
      tl.fromTo(q("qm"), { rotation: 0 }, { keyframes: [{ rotation: -10, duration: 0.12 }, { rotation: 8, duration: 0.14 }, { rotation: 0, duration: 0.12 }],
        immediateRender: false }, «SIN» + 0.3);
"""
    sfx = [(c["DICE"] - 0.1, "notification", 0.14), (c["TODOS"] + 0.06, "pop", 0.12), (c["TODOS"] + 0.18, "pop", 0.12),
           (c["TODOS"] + 0.30, "pop", 0.12), (c["TU"] - 0.06, "whoosh-short", 0.08), (c["SIN"] - 0.04, "click-soft", 0.2)]
    return comp(iid, d, P, css, body, js, c), sfx
