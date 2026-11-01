"""ins-03 · «porque casi todo lo que encuentras está en inglés.» — on paper: a search bar types «aprender neerlandés»
on «porque casi»; three results drop in on «todo lo que encuentras», all in English, each with a grey «EN» badge (UK
flag); on «en inglés» the badges turn red one after another and the line «Casi todo, en inglés» lands under them
(«en inglés» in a red chip). Same family as UGC #2 ins-02/ins-08 (paper, white cards, indigo type, a chip headline)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

RESULTS = [("play", "Learn Dutch in 30 days", "Video · 18 min"),
           ("book", "Dutch grammar explained", "Article · 7 min read"),
           ("pen", "Dutch for beginners", "Online course")]


def build():
    iid, P = "ins-03", "i3"; d = INS[iid]["duration"]
    c = dict(POR=cue(iid, "porque"), TODO=cue(iid, "todo"), ENC=cue(iid, "encuentras"), ING=cue(iid, "ingles"))
    c["T0"] = round(c["POR"] + 0.02, 3); c["T1"] = round(c["TODO"] - 0.04, 3)
    css = """
    #i3-bar { left: 90px; top: 250px; width: 900px; height: 112px; border-radius: 56px; display: flex; align-items: center; }
    #i3-mag { position: absolute; left: 36px; top: 36px; width: 40px; height: 40px; }
    #i3-q { position: absolute; left: 96px; top: 0; height: 112px; line-height: 112px; font-family: "Inter", sans-serif; font-weight: 600;
      font-size: 40px; color: «INK»; white-space: nowrap; }
    #i3-go { position: absolute; right: 14px; top: 14px; width: 84px; height: 84px; border-radius: 50%; background: «BLUE»; }
    #i3-go svg { position: absolute; left: 22px; top: 22px; width: 40px; height: 40px; }
    .i3-res { left: 90px; width: 900px; height: 116px; border-radius: 26px; }
    .i3-ic { position: absolute; left: 22px; top: 22px; width: 72px; height: 72px; border-radius: 18px; background: #EEF1FB; color: «INDIGO»;
      display: flex; align-items: center; justify-content: center; }
    .i3-ic svg { display: block; width: 40px; height: 40px; }
    .i3-t { position: absolute; left: 118px; top: 24px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 36px; line-height: 1.1;
      color: «INK»; white-space: nowrap; }
    .i3-s { position: absolute; left: 118px; top: 70px; font-family: "Inter", sans-serif; font-weight: 500; font-size: 26px; line-height: 1;
      color: «MUTED»; white-space: nowrap; }
    .i3-en { position: absolute; right: 24px; top: 32px; width: 124px; height: 52px; }
    .i3-enb, .i3-enr { position: absolute; left: 0; top: 0; width: 124px; height: 52px; border-radius: 999px; box-sizing: border-box;
      display: flex; align-items: center; justify-content: center; gap: 10px;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 25px; letter-spacing: 0.08em; }
    .i3-enb { background: #EEF1F8; color: «INK2»; }
    .i3-enr { background: «RED»; color: #FFFFFF; }
    .i3-en .i3-flag { width: 36px; height: 24px; flex: 0 0 36px; box-shadow: none; border-radius: 4px; }
    .i3-en .i3-flag svg { width: 36px; height: 24px; }
    #i3-r0 { top: 412px; } #i3-r1 { top: 546px; } #i3-r2 { top: 680px; }
    #i3-h { top: 884px; color: «INDIGO»; font-size: 76px; }
    #i3-chip { background: «RED»; color: #FFFFFF; }
"""
    mag = '<svg viewBox="0 0 40 40"><circle cx="17" cy="17" r="11" fill="none" stroke="«MUTED»" stroke-width="4"/><path d="M25 25 L34 34" stroke="«MUTED»" stroke-width="4" stroke-linecap="round"/></svg>'
    magw = '<svg viewBox="0 0 40 40"><circle cx="17" cy="17" r="11" fill="none" stroke="#FFFFFF" stroke-width="4"/><path d="M25 25 L34 34" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/></svg>'
    badge = f'<span class="i3-flag">{FLAG_EN}</span><span>EN</span>'
    rows = "\n".join(f"""    <div id="i3-r{k}" class="i3-card i3-res i3-on-paper"><div class="i3-ic">{icon(ic)}</div><div class="i3-t">{t}</div><div class="i3-s">{s}</div>
      <div class="i3-en"><div id="i3-b{k}" class="i3-enb">{badge}</div><div id="i3-e{k}" class="i3-enr">{badge}</div></div></div>"""
                     for k, (ic, t, s) in enumerate(RESULTS))
    body = "\n".join([ground(P, "paper"), f"""    <div id="i3-bar" class="i3-card i3-on-paper"><div id="i3-mag">{sub(mag, {})}</div><div id="i3-q"></div><div id="i3-go">{magw}</div></div>
{rows}
    <div id="i3-h" class="i3-h1"><span class="i3-w">Casi todo,</span> <span id="i3-chip" class="i3-chip">en inglés</span></div>"""])
    js = """
      tl.fromTo(q("bar"), { opacity: 0, y: 40, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "power3.out" }, 0);
""" + typing_js("q", "aprender neerlandés", c["T0"], c["T1"]) + """
      tl.to(q("go"), { keyframes: [{ scale: 0.88, duration: 0.06 }, { scale: 1, duration: 0.16, ease: "back.out(2)" }] }, «T1»);
"""
    starts = [c["TODO"], round(c["ENC"] - 0.12, 3), round(c["ENC"] + 0.14, 3)]
    for k, t in enumerate(starts):
        js += f'      tl.fromTo(q("r{k}"), {{ opacity: 0, y: -18, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(1.6)" }}, {t});\n'
    for k in range(3):
        js += f'      tl.fromTo(q("e{k}"), {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "back.out(2)" }}, {round(c["ING"] - 0.1 + 0.07 * k, 3)});\n'
        js += f'      tl.fromTo(q("b{k}"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.01 }}, {round(c["ING"] - 0.1 + 0.07 * k + 0.1, 3)});\n'   # the grey one goes under the red
    js += """      tl.fromTo(q("h"), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, «ING» - 0.06);
      tl.fromTo(q("chip"), { scale: 0.7 }, { scale: 1, duration: 0.3, ease: "back.out(1.8)" }, «ING» + 0.02);
"""
    sfx = [(c["T0"], "typing", 0.12, round(c["T1"] - c["T0"], 3)), (c["T1"], "click-soft", 0.2)] + \
          [(t, "pop", 0.12) for t in starts] + [(c["ING"] - 0.06, "click-soft", 0.22)]
    return comp(iid, d, P, css, body, js, c), sfx
