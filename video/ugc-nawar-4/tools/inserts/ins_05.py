"""ins-05 · «(La primera oferta:) nuestro libro en neerlandés para principiantes, explicado en español, por solo un euro.»
— THE PRODUCT, the client's own ebook animation («Animación Libro», tools/libro_clip.py), the book lifted off its black
and floating on Nawar blue (no black, no frame, no shadow), as in the Black Friday ad: it opens on «nuestro libro»,
turns its pages (a soft page sound on each) and closes on its cover just before «un euro». On top the label «Primera
oferta · Black Friday» (opaque, the pages pass behind it); under the book two white pills land on their words — «Para
principiantes» (a sprout), «Explicado en español» (ES flag) —; on «un euro» the page's white seal lands on the cover's
corner: «BLACK FRIDAY · 1 € · 12,50 €» (struck in red), the «1 €» with a quick pulse."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

K = 1.3                        # display scale of the 1280×720 animation (the open spread, 766 px → ~1000 px)
BOOK_CX, BOOK_CY = 640, 367.5  # centre of the open book in the animation (1280×720 px)
CY = 610                       # where the book's centre sits in the frame
VW, VH = round(1280 * K, 1), round(720 * K, 1)
VL, VT = round(540 - BOOK_CX * K, 1), round(CY - BOOK_CY * K, 1)
PAGES = [(0.50, 0.2), (1.50, 0.13), (2.45, 0.13), (3.40, 0.13), (4.40, 0.13), (5.70, 0.18)]   # cover open, page turns, cover close
SPROUT = ('<svg viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M24 42 V22"/><path d="M24 26 C24 16 16 12 8 12 C8 22 15 26 24 26 Z"/><path d="M24 22 C24 13 31 8 40 8 C40 18 33 22 24 22 Z"/></g></svg>')


def build():
    iid, P = "ins-05", "i5"; d = INS[iid]["duration"]
    c = dict(LIB=cue(iid, "libro"), PRI=cue(iid, "principiantes"), ESP=cue(iid, "espanol"), UN=cue(iid, "un"), EUR=cue(iid, "euro"),
             VW=VW, VH=VH, VL=VL, VT=VT)
    sp = json.load(open(os.path.join(ROOT, "assets", "video", "libro-ins05.json")))["speed"]
    css = """
    #i5-vw { position: absolute; left: «VL»px; top: «VT»px; width: «VW»px; height: «VH»px; }
    #i5-vw video { position: absolute; left: 0; top: 0; width: «VW»px; height: «VH»px; display: block; }
    #i5-lrow { top: 168px; }
    #i5-lab { background: «INDIGO»; border: 2px solid rgba(255,255,255,0.85); height: 68px; padding: 0 30px 0 22px; font-size: 27px; }   /* opaque: the turning pages pass behind it */
    #i5-lab svg { width: 32px; height: 32px; }
    #i5-prow { top: 1010px; gap: 18px; }
    .i5-wpill { gap: 12px; height: 80px; padding: 0 32px 0 20px; font-size: 35px; }
    .i5-wpill svg { display: block; width: 42px; height: 42px; color: «GREEN»; }
    .i5-wpill .i5-flag { width: 42px; height: 28px; flex: 0 0 42px; }
    .i5-wpill .i5-flag svg { width: 42px; height: 28px; }
    #i5-seal { position: absolute; left: 600px; top: 500px; transform-origin: 20% 50%; }
    .i5-seal { position: relative; padding: 24px 34px 26px; border-radius: 30px; background: #FFFFFF; }
    .i5-seal .k { font-family: "Inter", sans-serif; font-weight: 800; font-size: 24px; letter-spacing: 0.14em; color: «RED»; line-height: 1; }
    .i5-seal .p { display: flex; align-items: flex-end; gap: 26px; margin-top: 30px; }   /* (the 116 px price keeps its own line box clear of the label) */
    #i5-eur { display: inline-block; font-weight: 900; font-size: 116px; line-height: 1; letter-spacing: -0.03em; color: «INDIGO»;
      transform-origin: 40% 60%; }
    .i5-e { margin-left: 0.16em; }
    .i5-seal s { font-weight: 600; font-size: 40px; color: «MUTED»; line-height: 1; padding-bottom: 6px;
      text-decoration-color: «RED»; text-decoration-thickness: 4px; }
"""
    pills = [("p0", SPROUT, "Para principiantes"), ("p1", f'<span class="i5-flag i5-flagd">{FLAG_ES}</span>', "Explicado en español")]
    body = "\n".join([ground(P, "blue"), f"""    <div id="i5-vw"><video id="i5-v" class="clip" src="assets/video/libro-ins05.webm" muted playsinline data-start="0" data-duration="«D»" data-track-index="1"></video></div>
    <div id="i5-lrow" class="i5-row"><div id="i5-lab" class="i5-pill">{icon('book').replace('currentColor', '#FFFFFF')}<span>Primera oferta · Black Friday</span></div></div>
    <div id="i5-prow" class="i5-row">{"".join(f'<div id="i5-{pid}" class="i5-wpill">{ic}<span>{t}</span></div>' for pid, ic, t in pills)}</div>
    <div id="i5-seal"><div class="i5-seal"><div class="k">BLACK FRIDAY</div><div class="p"><span id="i5-eur">1<span class="i5-e">€</span></span><s>12,50&nbsp;€</s></div></div></div>"""])
    js = """
      tl.fromTo(q("lab"), { opacity: 0.4, y: -12 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      tl.fromTo(q("p0"), { opacity: 0, y: 24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.7)" }, «PRI» - 0.06);
      tl.fromTo(q("p1"), { opacity: 0, y: 24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.7)" }, «ESP» - 0.06);
      tl.fromTo(q("seal"), { opacity: 0, scale: 0.4, rotation: -14 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.36, ease: "back.out(1.9)" }, «UN» - 0.08);
      tl.fromTo(q("eur"), { scale: 1 }, { keyframes: [{ scale: 1.14, duration: 0.12, ease: "power2.out" }, { scale: 1, duration: 0.2, ease: "power2.inOut" }],
        immediateRender: false }, «EUR» + 0.02);
"""
    sfx = [   # (v3: no page-turn sounds — the client)
           (c["PRI"] - 0.06, "pop", 0.16), (c["ESP"] - 0.06, "pop", 0.16), (c["UN"] - 0.08, "sparkle", 0.16)]
    return comp(iid, d, P, css, body, js, c), sfx
