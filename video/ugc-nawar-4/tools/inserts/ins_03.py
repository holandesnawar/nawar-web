"""ins-03 · «(Te dices que en enero empiezas,) pero llega enero, luego febrero,» — on paper: a big wall calendar, its blue
header reading ENERO, with your note «Empezar neerlandés» (an empty checkbox) stuck on the 1st. On «enero» a red
«Pospuesto» tag lands on the note and it slides off to the right; the page flips to FEBRERO and the note comes back on
its 1st; on «febrero» the same again, to MARZO. Under it, «El mes que viene…» with the redo arrow. Fast (≈2 s): the
point is the note that never gets done."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

MONTHS = ["ENERO", "FEBRERO", "MARZO"]
FIRST = [4, 0, 0]          # weekday column of the 1st (Mon = 0) in 2027: 1 enero is a Friday, 1 febrero and 1 marzo Mondays
NDAYS = [31, 28, 31]
CAL_L, CAL_T, CAL_W = 120, 300, 840
CELL = 120


def grid(first, ndays):
    cells = []
    for k in range(35):
        day = k - first + 1
        txt = str(day) if 1 <= day <= ndays else ""
        cells.append(f'<div class="i3-d" data-layout-allow-overlap>{txt}</div>')   # (the note and the next page cover them on purpose)
    return "".join(cells)


def build():
    iid, P = "ins-03", "i3"; d = INS[iid]["duration"]
    c = dict(LLE=cue(iid, "llega"), ENE=cue(iid, "enero"), LUE=cue(iid, "luego"), FEB=cue(iid, "febrero"))
    css = """
    #i3-cal { left: «CL»px; top: «CT»px; width: «CW»px; height: 760px; overflow: hidden; }
    .i3-hd { position: absolute; left: 0; top: 0; width: «CW»px; height: 150px; background: «BLUE»; color: #FFFFFF; text-align: center;
      font-weight: 800; font-size: 76px; line-height: 150px; letter-spacing: 0.04em; }
    .i3-rings { position: absolute; left: 0; top: -20px; width: «CW»px; height: 40px; display: flex; justify-content: space-around; padding: 0 140px; }
    .i3-rings i { display: block; width: 22px; height: 46px; border-radius: 11px; background: «INDIGO»; }
    .i3-wk { position: absolute; left: 0; top: 166px; width: «CW»px; display: grid; grid-template-columns: repeat(7, 1fr);
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; color: «MUTED»; text-align: center; }
    .i3-g { position: absolute; left: 0; top: 212px; width: «CW»px; display: grid; grid-template-columns: repeat(7, 1fr); grid-auto-rows: 104px; }
    .i3-d { border-top: 2px solid «LINE»; font-family: "Inter", sans-serif; font-weight: 600; font-size: 30px; color: «INK2»;
      padding: 10px 0 0 14px; }
    .i3-page { position: absolute; left: 0; top: 0; width: «CW»px; height: 760px; background: #FFFFFF; }
    #i3-note { position: absolute; left: 150px; top: 560px; width: 660px; height: 150px; border-radius: 24px; background: #EAF3FF;
      box-shadow: inset 0 0 0 3px «SKY»; display: flex; align-items: center; gap: 22px; padding: 0 30px; transform-origin: 50% 50%; }
    #i3-box { width: 58px; height: 58px; flex: 0 0 58px; border-radius: 14px; box-shadow: inset 0 0 0 5px «INDIGO»; background: #FFFFFF; }
    #i3-nt { font-weight: 800; font-size: 44px; line-height: 1.05; color: «INDIGO»; white-space: nowrap; }
    #i3-tag { position: absolute; right: -16px; top: -30px; height: 58px; padding: 0 22px; border-radius: 999px; background: «RED»;
      color: #FFFFFF; display: flex; align-items: center; gap: 10px; font-family: "Inter", sans-serif; font-weight: 800; font-size: 26px;
      letter-spacing: 0.08em; text-transform: uppercase; }
    #i3-tag svg { display: block; width: 30px; height: 30px; }
    #i3-h { top: 1110px; color: «INDIGO»; font-size: 72px; display: flex; justify-content: center; align-items: center; gap: 18px; }
    #i3-h svg { display: block; width: 72px; height: 72px; color: «RED»; }
"""
    wk = "".join(f'<span data-layout-allow-overlap>{x}</span>' for x in "LMXJVSD")
    pages = "".join(f"""      <div id="i3-p{k}" class="i3-page" data-layout-allow-occlusion><div class="i3-hd" data-layout-allow-overlap>{m}</div>
        <div class="i3-wk">{wk}</div>
        <div class="i3-g">{grid(FIRST[k], NDAYS[k])}</div></div>
""" for k, m in enumerate(MONTHS))
    body = "\n".join([ground(P, "paper"), f"""    <div id="i3-cal" class="i3-card i3-on-paper">
{pages}      <div id="i3-note" data-layout-allow-occlusion><div id="i3-box"></div><div id="i3-nt" data-layout-allow-overlap>Empezar neerlandés</div>
        <div id="i3-tag" data-layout-allow-occlusion>{icon('redo')}<span data-layout-allow-overlap>Pospuesto</span></div></div>
    </div>
    <div class="i3-rings" style="position: absolute; left: «CL»px; top: 282px;"><i></i><i></i><i></i><i></i></div>
    <div id="i3-h" class="i3-h1">{icon('redo')}<span>El mes que viene…</span></div>"""])
    # timings: the note is on ENERO from the cut; out on «enero» → FEBRERO → back; out on «febrero» → MARZO → back
    o1 = round(c["ENE"] + 0.02, 3); o2 = round(c["FEB"] + 0.02, 3)
    js = """
      tl.fromTo(q("cal"), { opacity: 0.4, y: 30, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      tl.set(q("p1"), { opacity: 0 }, 0); tl.set(q("p2"), { opacity: 0 }, 0);
      tl.set(q("tag"), { opacity: 0 }, 0);
      tl.fromTo(q("h"), { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.12);
"""
    for k, t in enumerate((o1, o2)):
        js += f"""      tl.fromTo(q("tag"), {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "back.out(2.2)", immediateRender: false }}, {round(t - 0.2, 3)});
      tl.to(q("note"), {{ x: 760, rotation: 10, duration: 0.22, ease: "power2.in" }}, {t});
      tl.set(q("p{k + 1}"), {{ opacity: 1 }}, {round(t + 0.2, 3)});
      tl.fromTo(q("p{k + 1}"), {{ rotationX: -70, transformOrigin: "50% 0%" }}, {{ rotationX: 0, duration: 0.2, ease: "power2.out", immediateRender: false }}, {round(t + 0.2, 3)});
      tl.set(q("tag"), {{ opacity: 0 }}, {round(t + 0.22, 3)});
      tl.set(q("p{k}"), {{ opacity: 0 }}, {round(t + 0.42, 3)});   // the page under it, gone once it has turned
      tl.fromTo(q("note"), {{ x: -760, rotation: -8 }}, {{ x: 0, rotation: 0, duration: 0.24, ease: "power3.out", immediateRender: false }}, {round(t + 0.3, 3)});
"""
    sfx = [(o1 - 0.2, "error", 0.1), (o1, "whoosh-short", 0.12), (o1 + 0.2, "page", 0.22),
           (o2 - 0.2, "error", 0.1), (o2, "whoosh-short", 0.12), (o2 + 0.2, "page", 0.22)]
    return comp(iid, d, P, css, body, js, dict(c, CL=CAL_L, CT=CAL_T, CW=CAL_W)), sfx
