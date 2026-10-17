"""ins-08 · «(mientras las ofertas de trabajo bajan,) nueve de cada diez siguen pidiendo como requisito el neerlandés»
— on paper: a big «9 de cada 10 · ofertas de trabajo» (the 9 on «nueve», the 10 on «diez»), then a calm grid of ten
job-offer cards (briefcase + skeleton title/company + a grey tag slot) that land on «siguen»; on «requisito» nine
of them get a blue «Nederlands vereist» tag with the NL flag and the tenth is left plain and dimmed; on
«neerlandés» the nine tagged offers light up with a thin indigo outline. Then it holds."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

# briefcase: simple bold line icon (48 box, stroke 4), coloured by currentColor
CASE = ('<svg viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="6" y="14" width="36" height="26" rx="5"/><path d="M17 14 V10 A3 3 0 0 1 20 7 H28 A3 3 0 0 1 31 10 V14"/>'
        '<path d="M6 25 H42"/></g></svg>')

GX = (86, 554)            # two columns, 440 wide, 28 apart (86 px side margins)
GY0, CH, GAP = 476, 116, 22
TW = (214, 186, 236, 198, 222, 180, 206, 230, 194, 218)    # skeleton title widths (a bit of variety, like real listings)
CW = (132, 150, 110, 142, 120, 156, 126, 104, 146, 128)    # skeleton company widths
NL_ROUND = ('<svg viewBox="0 0 24 24"><rect width="24" height="8" fill="#AE1C27"/><rect y="8" width="24" height="8" fill="#FFFFFF"/>'
            '<rect y="16" width="24" height="8" fill="#21468C"/></svg>')
LAST = 9                  # the tenth offer: no tag
# headline row offsets (row-local px; the row is shown at 1.2×) that centre «9» alone, then «9 de cada»,
# measured from the rendered glyph extents of the final centred row
X1, X2 = 222, 86


def build():
    iid, P = "ins-08", "i8"; d = INS[iid]["duration"]
    c = dict(NUE=cue(iid, "nueve"), DE=cue(iid, "de"), DIEZ=cue(iid, "diez"), SIG=cue(iid, "siguen"),
             REQ=cue(iid, "requisito"), NEER=cue(iid, "neerlandes"))
    c["T9"] = round(max(0.0, c["NUE"] - 0.06), 3)
    c["MOVE"] = round(c["DIEZ"] + 0.24, 3)        # the headline, big and centred, glides up to make room for the offers
    c["CARDS"] = round(c["SIG"] - 0.02, 3)
    c["TAGS"] = round(c["REQ"] - 0.08, 3)
    c["DIM"] = round(c["TAGS"] + 8 * 0.06 + 0.04, 3)
    c["GLOW"] = round(c["NEER"] - 0.06, 3)

    css = """
    #i8-head { position: absolute; left: 0; top: 0; width: 1080px; height: 470px; transform-origin: 50% 321px; }
    #i8-hrow { top: 214px; height: 150px; align-items: baseline; gap: 26px; }
    .i8-num { display: block; font-weight: 900; font-size: 148px; line-height: 1; letter-spacing: -0.045em; color: «INDIGO»;
      white-space: nowrap; transform-origin: 50% 80%; }
    #i8-dc { display: block; font-weight: 800; font-size: 64px; line-height: 1; letter-spacing: -0.03em; color: «INK»; white-space: nowrap; }
    #i8-sub { top: 384px; height: 44px; }
    #i8-subt { display: block; font-family: "Inter", sans-serif; font-weight: 600; font-size: 34px; line-height: 1; letter-spacing: -0.01em;
      color: «MUTED»; white-space: nowrap; }

    .i8-job { position: absolute; width: 440px; height: «CH»px; border-radius: 18px; background: #FFFFFF;
      box-shadow: 0 14px 34px rgba(18,0,129,0.09), 0 2px 8px rgba(18,0,129,0.05); }
    .i8-ol { position: absolute; left: 0; top: 0; width: 440px; height: «CH»px; border-radius: 18px; box-sizing: border-box;
      border: 2px solid «INDIGO»; box-shadow: 0 0 0 5px rgba(29,0,132,0.07), 0 16px 38px rgba(29,0,132,0.16); opacity: 0; }
    .i8-ic { position: absolute; left: 22px; top: 26px; width: 64px; height: 64px; border-radius: 16px; background: #ECEFFB; color: «INDIGO»; }
    .i8-ic svg { position: absolute; left: 14px; top: 14px; width: 36px; height: 36px; display: block; }
    .i8-l1 { position: absolute; left: 106px; top: 25px; height: 15px; border-radius: 8px; background: #D6DDEE; }
    .i8-l2 { position: absolute; left: 106px; top: 50px; height: 11px; border-radius: 6px; background: #E7ECF6; }
    .i8-slot { position: absolute; left: 106px; top: 70px; width: 124px; height: 34px; border-radius: 999px; background: #F0F2F9; }
    .i8-tag { position: absolute; left: 106px; top: 70px; height: 34px; display: flex; align-items: center; gap: 8px; padding: 0 14px 0 5px;
      border-radius: 999px; background: «INDIGO»; color: #FFFFFF; white-space: nowrap; box-sizing: border-box; transform-origin: 0% 50%;
      box-shadow: 0 6px 14px rgba(29,0,132,0.22);
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 22px; line-height: 1; letter-spacing: -0.005em; }
    .i8-fl { display: block; width: 30px; height: 20px; border-radius: 4px; overflow: hidden; flex: 0 0 30px; margin-left: 6px;
      box-shadow: 0 0 0 2px rgba(255,255,255,0.85); }
    .i8-fl svg { display: block; width: 30px; height: 20px; }
"""

    def job(k):
        x, y = GX[k % 2], GY0 + (k // 2) * (CH + GAP)
        tag = "" if k == LAST else (f'<div id="i8-tg{k}" class="i8-tag"><span class="i8-fl">{FLAG_NL}</span>'
                                    f'<span>Nederlands vereist</span></div>')
        ol = "" if k == LAST else f'<div id="i8-ol{k}" class="i8-ol"></div>'
        return (f'    <div id="i8-c{k}" class="i8-job" style="left:{x}px; top:{y}px;" data-layout-allow-overflow>{ol}'
                f'<div class="i8-ic">{CASE}</div><div class="i8-l1" style="width:{TW[k]}px;"></div>'
                f'<div class="i8-l2" style="width:{CW[k]}px;"></div><div class="i8-slot"></div>{tag}</div>')

    body = "\n".join([ground(P, "paper"), """    <div id="i8-head"><div id="i8-hrow" class="i8-row"><span id="i8-n9" class="i8-num">9</span><span id="i8-dc">de cada</span><span id="i8-n10" class="i8-num">10</span></div>
    <div id="i8-sub" class="i8-row"><span id="i8-subt">ofertas de trabajo</span></div></div>"""] + [job(k) for k in range(10)])

    js = """
      // «nueve de cada diez»: the two numbers land on their words, «de cada» in between; the row re-centres
      // itself at each step (the slots are the final centred ones, so the lone «9» starts shifted to the middle)
      tl.fromTo(q("hrow"), { x: «X1» }, { x: «X2», duration: 0.3, ease: "power3.out" }, «DE» - 0.06);
      tl.to(q("hrow"), { x: 0, duration: 0.3, ease: "power3.out" }, «DIEZ» - 0.06);
      tl.fromTo(q("n9"), { opacity: 0, scale: 0.55, y: 24 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «T9»);
      tl.fromTo(q("dc"), { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.28, ease: "power3.out" }, «DE» - 0.06);
      tl.fromTo(q("n10"), { opacity: 0, scale: 0.55, y: 24 }, { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(1.8)" }, «DIEZ» - 0.06);
      tl.fromTo(q("subt"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }, «DIEZ» + 0.02);
      // «siguen»: the headline glides up to the top and ten offers land under it, row by row
      tl.fromTo(q("head"), { y: 330, scale: 1.2 }, { y: 0, scale: 1, duration: 0.42, ease: "power3.inOut" }, «MOVE»);
"""
    for k in range(10):
        js += (f'      tl.fromTo(q("c{k}"), {{ opacity: 0, y: 34, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.32, '
               f'ease: "power3.out" }}, «CARDS» + {k * 0.04:.2f});\n')
    js += "      // «requisito»: nine get the tag, the tenth stays plain and steps back\n"
    for n, k in enumerate(k for k in range(10) if k != LAST):
        js += (f'      tl.fromTo(q("tg{k}"), {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.28, '
               f'ease: "back.out(1.9)" }}, «TAGS» + {n * 0.06:.2f});\n')
    js += f'      tl.to(q("c{LAST}"), {{ opacity: 0.65, duration: 0.3, ease: "power2.out" }}, «DIM»);\n'
    js += "      // «neerlandés»: the nine tagged offers light up together\n"
    js += ("      tl.fromTo([" + ", ".join(f'q("ol{k}")' for k in range(10) if k != LAST) +
           '], { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, «GLOW»);\n')

    sfx = [(c["T9"], "pop", 0.2), (c["TAGS"], "click-soft", 0.22), (c["GLOW"], "ping", 0.18)]
    return comp(iid, d, P, css, body, js, dict(c, CH=CH, X1=X1, X2=X2)), sfx
