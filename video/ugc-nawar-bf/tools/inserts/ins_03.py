"""ins-03 · «porque casi todo lo que encuentras está en inglés.» — a search bar card pops in, centred in the frame, and
«aprender neerlandés» types itself on «porque casi»; the blue search button is pressed and the bar slides up to the
top; on «todo lo que encuentras» four result cards drop in under it one after another, all in English (Learn Dutch
in 30 days · Dutch grammar explained · Dutch for beginners · 100 Dutch words you need), each with a small UK-flag «EN»
badge; on «en inglés» the four EN badges turn red one after another with a pulse ring, and a big red «CASI TODO
EN INGLÉS» tag slams (she says «casi todo») in under the list (the list gives a small shake). Dark ground, white cards, Nawar blue for you
(your search), red for what goes wrong."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

QUERY = "aprender neerlandés"
RESULTS = [("Learn Dutch in 30 days", "Video · 18 min", "play", "dark"),
           ("Dutch grammar explained", "Article · 7 min read", "book", "light"),
           ("Dutch for beginners", "Online course", "pen", "dark"),
           ("100 Dutch words you need", "Vocabulary list", "trans", "light")]
TOP0, RH, GAP = 396, 140, 16          # first result card top, card height, gap
SEARCH = ('<svg viewBox="0 0 48 48"><circle cx="21" cy="21" r="12.5" fill="none" stroke="currentColor" stroke-width="5"/>'
          '<path d="M30.5 30.5 L41 41" stroke="currentColor" stroke-width="5.4" stroke-linecap="round"/></svg>')


def build():
    iid, P = "ins-03", "i3"; d = INS[iid]["duration"]
    c = dict(POR=cue(iid, "porque"), CAS=cue(iid, "casi"), TOD=cue(iid, "todo"), ENC=cue(iid, "encuentras"),
             EST=cue(iid, "esta"), EN=cue(iid, "en"), ING=cue(iid, "ingles"))
    t_type0, t_type1 = 0.08, round(c["TOD"] - 0.05, 3)                 # «porque casi»: the query types itself
    t_btn = t_type1 + 0.02                                              # the search button is pressed
    t_up = t_btn + 0.03                                                 # the bar slides up to the top
    t_res = [round(t_up + 0.17 + 0.13 * k, 3) for k in range(4)]        # «todo lo que encuentras»: the cascade
    t_red = [round(c["EN"] - 0.03 + 0.05 * k, 3) for k in range(4)]     # «en inglés»: the EN badges turn red
    t_tag = round(c["ING"] - 0.05, 3)                                   # «inglés»: the tag lands
    c.update(T_BTN=t_btn, T_UP=t_up, T_TAG=t_tag, LIFT=330)
    css = """
    #i3-bar { left: 90px; top: 236px; width: 900px; height: 124px; border-radius: 62px; }
    #i3-mag { position: absolute; left: 38px; top: 38px; width: 48px; height: 48px; color: «GREY»; }
    #i3-mag svg { display: block; width: 48px; height: 48px; }
    #i3-q { position: absolute; left: 108px; top: 0; height: 124px; display: flex; align-items: center; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 46px; line-height: 1; letter-spacing: -0.01em; color: «INK»; }
    #i3-caret { display: block; width: 4px; height: 56px; margin-left: 4px; border-radius: 2px; background: «BLUE»; }
    #i3-btn { position: absolute; right: 16px; top: 16px; width: 92px; height: 92px; border-radius: 50%; background: «BLUE»; color: #FFFFFF;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 20px rgba(11,109,240,0.35); }
    #i3-btn svg { display: block; width: 46px; height: 46px; }
    #i3-list { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .i3-res { left: 90px; width: 900px; height: «RH»px; border-radius: 30px;
      box-shadow: 0 26px 56px rgba(0,0,0,0.50), 0 6px 16px rgba(0,0,0,0.35); }   /* stacked: a shorter shadow, no grey on the card above */
    .i3-th { position: absolute; left: 21px; top: 21px; width: 98px; height: 98px; border-radius: 22px;
      display: flex; align-items: center; justify-content: center; }
    .i3-th svg { display: block; width: 52px; height: 52px; }
    .i3-th-dark { background: #1C1D33; color: #FFFFFF; }
    .i3-th-dark svg { width: 58px; height: 58px; }
    .i3-th-light { background: #E8ECF7; color: «INK2»; }
    .i3-tt { position: absolute; left: 145px; top: 27px; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 40px; line-height: 1.1; letter-spacing: -0.015em; color: «INK»; }
    .i3-ts { position: absolute; left: 145px; top: 84px; white-space: nowrap;
      font-family: "Inter", sans-serif; font-weight: 600; font-size: 28px; line-height: 1; color: «MUTED»; }
    .i3-en { position: absolute; right: 26px; top: 40px; width: 124px; height: 60px; }
    .i3-enb, .i3-enr { position: absolute; left: 0; top: 0; width: 124px; height: 60px; border-radius: 999px; box-sizing: border-box;
      display: flex; align-items: center; justify-content: center; gap: 10px;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 27px; line-height: 1; letter-spacing: 0.06em; }
    .i3-enb { background: #EEF1F8; color: «INK2»; }
    .i3-enr { background: «RED»; color: #FFFFFF; box-shadow: 0 8px 20px rgba(224,45,60,0.40); }
    .i3-enb .i3-flag, .i3-enr .i3-flag { width: 38px; height: 26px; flex: 0 0 38px; }
    .i3-enb .i3-flag svg, .i3-enr .i3-flag svg { width: 38px; height: 26px; }
    .i3-ring { position: absolute; left: -6px; top: -6px; width: 136px; height: 72px; border-radius: 999px; border: 4px solid «RED»;
      box-sizing: border-box; opacity: 0; }
    #i3-tagrow { top: 1052px; height: 136px; }
    #i3-tag { display: flex; align-items: center; height: 136px; padding: 4px 52px 0; box-sizing: border-box; border-radius: 26px;
      background: «RED»; color: #FFFFFF; white-space: nowrap; box-shadow: 0 0 0 6px #FFFFFF, 0 40px 90px rgba(0,0,0,0.60), 0 8px 24px rgba(0,0,0,0.40);
      font-family: "Poppins", sans-serif; font-weight: 900; font-size: 70px; line-height: 1; letter-spacing: -0.01em; }
"""
    css = css.replace("«RH»", str(RH))
    cards = []
    for k, (tt, ts, ic, th) in enumerate(RESULTS):
        badge = f'<span class="i3-flag i3-flagd">{FLAG_EN}</span><span>EN</span>'
        cards.append(f"""      <div id="i3-r{k}" class="i3-card i3-on-dark i3-res" style="top:{TOP0 + k * (RH + GAP)}px;">
        <div class="i3-th i3-th-{th}">{icon(ic)}</div>
        <div class="i3-tt">{tt}</div>
        <div class="i3-ts">{ts}</div>
        <div class="i3-en"><div id="i3-g{k}" class="i3-ring"></div><div id="i3-b{k}" class="i3-enb">{badge}</div><div id="i3-e{k}" class="i3-enr">{badge.replace('i3-flagd', '')}</div></div>
      </div>""")
    body = "\n".join([ground(P, "dark"), f"""    <div id="i3-bar" class="i3-card i3-on-dark">
      <div id="i3-mag">{SEARCH}</div>
      <div id="i3-q"><span id="i3-typed">{QUERY}</span><span id="i3-caret"></span></div>
      <div id="i3-btn">{SEARCH}</div>
    </div>
    <div id="i3-list">
{chr(10).join(cards)}
    </div>
    <div id="i3-tagrow" class="i3-row"><div id="i3-tag">CASI TODO EN INGLÉS</div></div>"""])
    js = """
      tl.fromTo(q("bar"), { opacity: 0, y: «LIFT» + 60, scale: 1 }, { opacity: 1, y: «LIFT», scale: 1.06, duration: 0.3, ease: "power3.out" }, 0);
      tl.fromTo(q("bar"), { y: «LIFT», scale: 1.06 }, { y: 0, scale: 1, duration: 0.26, ease: "power3.inOut", immediateRender: false }, «T_UP»);
""" + typing_js("typed", QUERY, t_type0, t_type1) + """
      tl.set(q("caret"), { opacity: 1 }, 0);
""" + blink_js("caret", t_type1 + 0.25, d - 0.01) + """
      tl.fromTo(q("btn"), { scale: 1 }, { keyframes: [{ scale: 0.86, duration: 0.07, ease: "power2.out" }, { scale: 1, duration: 0.22, ease: "back.out(2.6)" }] }, «T_BTN»);
"""
    for k in range(4):
        js += (f'      tl.fromTo(q("r{k}"), {{ opacity: 0, y: -14, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(2)" }}, {t_res[k]});\n')
    js += "      // «en inglés»: every EN badge turns red with a pulse ring, then the tag slams onto the list\n"
    for k in range(4):
        js += (f'      tl.fromTo(q("e{k}"), {{ opacity: 0, scale: 1 }}, {{ keyframes: [{{ opacity: 1, scale: 1.2, duration: 0.07, ease: "power2.out" }}, '
               f'{{ scale: 1, duration: 0.18, ease: "power2.inOut" }}] }}, {t_red[k]});\n'
               f'      tl.fromTo(q("b{k}"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.01 }}, {round(t_red[k] + 0.07, 3)});\n'   # the grey one goes under the red
               f'      tl.fromTo(q("g{k}"), {{ opacity: 0, scale: 1 }}, {{ keyframes: [{{ opacity: 0.9, duration: 0.02 }}, '
               f'{{ opacity: 0, scale: 1.45, duration: 0.38, ease: "power2.out" }}] }}, {t_red[k]});\n')
    js += """      tl.fromTo(q("tag"), { opacity: 0, scale: 1.9, rotation: -11 }, { opacity: 1, scale: 1, rotation: -3, duration: 0.26, ease: "back.out(1.5)" }, «T_TAG»);
      tl.to(q("list"), { keyframes: [{ x: -10, duration: 0.05 }, { x: 9, duration: 0.05 }, { x: -6, duration: 0.05 }, { x: 0, duration: 0.05 }] }, «T_TAG» + 0.16);
"""
    sfx = [(t_type0, "typing", 0.12, round(t_type1 - t_type0 + 0.05, 3)), (t_btn, "click-soft", 0.18)]
    sfx += [(t, "pop", 0.12 if k == 0 else 0.1) for k, t in enumerate(t_res)]
    sfx += [(t_up, "whoosh-short", 0.06), (t_red[0], "ping", 0.07), (t_tag + 0.12, "error", 0.3)]
    sfx.sort(key=lambda x: x[0])
    return comp(iid, d, P, css, body, js, c), sfx
