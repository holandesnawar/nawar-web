"""ins-04 · «este libro: 70 páginas en español, para imprimir, con vocabulario, gramática, ejercicios prácticos, cómo
pronunciar los sonidos por los que te cambian en inglés cuando abres la boca.» — THE PRODUCT, the client's own ebook
(«Holandés sin miedo», from «Animación Libro Interactivo»), big on Nawar blue like the recorded lesson in UGC #2 ins-05:
  · the cover, then the book opens on «imprimir» and its pages turn to «De nummers | Hebben en zijn» on «gramática»
    (assets/video/libro-ins04.mp4, cut to her words by tools/libro_clip.py), the camera pushing in on the grammar table;
  · on «ejercicios» it moves to the «¡Repasemos lo aprendido!» box; on «cómo pronunciar» the page is «Klanken
    (Sonidos)» (a still), pushing in to the end;
  · under the book: «70 páginas», «En español» (ES flag) and «Para imprimir» (printer) land on their words, then a ticked
    row per word: Vocabulario, Gramática, Ejercicios, Pronunciación (UGC #2 ins-06's ticked pills).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

SRC_W = 1280                     # the clip and stills are 1280×720; the frame shows them 1000 wide
K = 1000 / SRC_W
TABLE, REPASO, KLANKEN = (812, 272), (817, 482), (820, 375)   # zoom targets (source px)


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(SET=cue(iid, "70"), ESP=cue(iid, "espanol"), IMP=cue(iid, "imprimir"), VOC=cue(iid, "vocabulario"),
             GRA=cue(iid, "gramatica"), EJE=cue(iid, "ejercicios"), COMO=cue(iid, "como"))
    t_still = round(c["GRA"] + 0.05, 3)            # the clip ends on «De nummers | Hebben en zijn» here
    t_kl = round(c["COMO"] - 0.1, 3)               # cut to «Klanken (Sonidos)»
    c.update(TS=t_still, TK=t_kl, VD=t_still + 0.04,
             TX=round(TABLE[0] * K, 1), TY=round(TABLE[1] * K, 1), RX=round(REPASO[0] * K, 1), RY=round(REPASO[1] * K, 1),
             KX=round(KLANKEN[0] * K, 1), KY=round(KLANKEN[1] * K, 1))
    css = """
    #i4-lrow { top: 206px; }
    #i4-frame { position: absolute; left: 40px; top: 296px; width: 1000px; height: 562.5px; border-radius: 30px; overflow: hidden;
      background: #F1ECE4; box-shadow: 0 0 0 6px rgba(255,255,255,0.9), 0 40px 110px rgba(4,0,40,0.45), 0 8px 24px rgba(4,0,40,0.25); }
    .i4-z { position: absolute; left: 0; top: 0; width: 1000px; height: 562.5px; }
    .i4-z video, .i4-z img { position: absolute; left: 0; top: 0; width: 1000px; height: 562.5px; object-fit: cover; display: block; }
    #i4-zc { transform-origin: 50% 50%; }
    #i4-zn { transform-origin: «TX»px «TY»px; }
    #i4-zk { transform-origin: «KX»px «KY»px; }
    #i4-prow { top: 926px; gap: 16px; }
    .i4-wpill { gap: 12px; height: 76px; padding: 0 30px 0 18px; font-size: 33px; }
    .i4-wpill svg { display: block; width: 40px; height: 40px; color: «INDIGO»; }
    .i4-wpill .i4-flag svg { width: 40px; height: 27px; }
    #i4-crow { top: 1040px; gap: 14px; flex-wrap: wrap; width: 960px; left: 60px; row-gap: 14px; }
    .i4-ck { display: flex; align-items: center; gap: 10px; height: 64px; padding: 0 26px 0 12px; border-radius: 999px;
      background: rgba(255,255,255,0.14); border: 1px solid rgba(255,255,255,0.30); color: #FFFFFF; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 30px; line-height: 1; }
    .i4-ck svg { display: block; width: 40px; height: 40px; }
"""
    pills = [("p0", icon("book"), "70 páginas"), ("p1", f'<span class="i4-flag i4-flagd">{FLAG_ES}</span>', "En español"),
             ("p2", icon("print"), "Para imprimir")]
    checks = ["Vocabulario", "Gramática", "Ejercicios", "Pronunciación"]
    body = "\n".join([ground(P, "blue"), f"""    <div id="i4-lrow" class="i4-row"><div id="i4-lab" class="i4-pill">{icon('book').replace('currentColor', '#FFFFFF')}<span>Ebook · Holandés sin miedo</span></div></div>
    <div id="i4-frame">
      <div id="i4-zc" class="i4-z"><video id="i4-v" class="clip" src="assets/video/libro-ins04.mp4" muted playsinline data-start="0" data-duration="«VD»" data-track-index="1"></video></div>
      <div id="i4-zn" class="i4-z"><img src="assets/img/libro-nummers.png" alt="" /></div>
      <div id="i4-zk" class="i4-z"><img src="assets/img/libro-klanken.png" alt="" /></div>
    </div>
    <div id="i4-prow" class="i4-row">{"".join(f'<div id="i4-{pid}" class="i4-wpill">{ic}<span>{t}</span></div>' for pid, ic, t in pills)}</div>
    <div id="i4-crow" class="i4-row">{"".join(f'<div id="i4-c{k}" class="i4-ck">{icon("check")}<span>{t}</span></div>' for k, t in enumerate(checks))}</div>"""])
    js = """
      tl.fromTo(q("lab"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("frame"), { opacity: 0, y: 90, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out" }, 0);
      // the cover drifts in while she names it, the book opens and turns its pages (the clip)
      tl.fromTo(q("zc"), { scale: 1.3 }, { scale: 1.45, duration: «IMP» - 0.06, ease: "power1.inOut" }, 0);
      tl.fromTo(q("zc"), { scale: 1.45 }, { scale: 1.0, duration: 0.55, ease: "power2.inOut", immediateRender: false }, «IMP» - 0.05);
      // «gramática»: the spread holds (still), the camera pushes in on the table; «ejercicios»: over to the review box
      tl.set(q("zn"), { opacity: 0 }, 0);
      tl.set(q("zn"), { opacity: 1 }, «TS»);
      tl.fromTo(q("zn"), { scale: 1, x: 0, y: 0 }, { scale: 1.45, x: 500 - «TX», y: 281 - «TY», duration: 0.6, ease: "power2.inOut", immediateRender: false }, «TS»);
      tl.fromTo(q("zn"), { x: 500 - «TX», y: 281 - «TY» }, { x: 500 - «TX» - («RX» - «TX») * 1.45, y: 281 - «TY» - («RY» - «TY») * 1.45, duration: 0.55,
        ease: "power2.inOut", immediateRender: false }, «EJE» - 0.08);
      // «cómo pronunciar los sonidos»: the «Klanken (Sonidos)» page, pushing in to the end
      tl.set(q("zk"), { opacity: 0 }, 0);
      tl.set(q("zk"), { opacity: 1 }, «TK»);
      tl.fromTo(q("zk"), { scale: 1.4, x: 500 - «KX», y: 281 - «KY» }, { scale: 1.6, x: 500 - «KX», y: 281 - «KY», duration: «D» - «TK», ease: "power1.out",
        immediateRender: false }, «TK»);
"""
    for (pid, _, _), key in zip(pills, ("SET", "ESP", "IMP")):
        js += f'      tl.fromTo(q("{pid}"), {{ opacity: 0, y: 24, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.7)" }}, «{key}» - 0.06);\n'
    for k, key in enumerate(("VOC", "GRA", "EJE", "COMO")):
        js += f'      tl.fromTo(q("c{k}"), {{ opacity: 0, y: 18, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "back.out(1.7)" }}, «{key}» - 0.05);\n'
    sfx = [(c["SET"] - 0.06, "pop", 0.16), (c["ESP"] - 0.06, "pop", 0.16), (c["IMP"] - 0.06, "pop", 0.2)] + \
          [(c[k] - 0.05, "click-soft", 0.18) for k in ("VOC", "GRA", "EJE", "COMO")]
    return comp(iid, d, P, css, body, js, c), sfx
