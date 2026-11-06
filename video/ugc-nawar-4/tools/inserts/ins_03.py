"""ins-03 · «(Te dices que en enero empiezas,) pero llega enero, luego febrero,» — v2 (the client: the v1 wall calendar
«se ve algo IA»): a real-looking phone lock screen on paper. «viernes, 1 de enero», 9:00, and the reminder «Empezar
neerlandés» (Recordatorios, ahora) with its «Posponer» button. On «enero» the button is tapped, the notification goes,
the date turns to «lunes, 1 de febrero» and the reminder comes back («Pospuesto 1 vez»); on «febrero» the same, to «lunes,
1 de marzo» («Pospuesto 2 veces»). Weekdays are 2027's."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

DAYS = ["viernes, 1 de enero", "lunes, 1 de febrero", "lunes, 1 de marzo"]
SUBS = ["Hoy · 9:00", "Pospuesto 1 vez", "Pospuesto 2 veces"]
PW, PH, PL, PT = 660, 1090, 210, 150
BELL = ('<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#0B6DF0"/><path d="M20 9 C14 9 12 13 12 18 V23 L9.5 27 H30.5 L28 23 '
        'V18 C28 13 26 9 20 9 Z M17 29 A3 3 0 0 0 23 29 Z" fill="#FFFFFF"/></svg>')


def build():
    iid, P = "ins-03", "i3"; d = INS[iid]["duration"]
    c = dict(ENE=cue(iid, "enero"), FEB=cue(iid, "febrero"))
    css = PHONE_CSS + """
    #i3-wp { position: absolute; inset: 0; background: linear-gradient(170deg, #3E7BE6 0%, #1F3FA8 55%, #172C7A 100%); }
    .i3-date { position: absolute; left: 0; top: 150px; width: 100%; text-align: center; font-family: "Inter", sans-serif; font-weight: 600;
      font-size: 32px; color: rgba(255,255,255,0.92); }
    #i3-clock { position: absolute; left: 0; top: 206px; width: 100%; text-align: center; font-family: "Inter", sans-serif; font-weight: 700;
      font-size: 168px; line-height: 1; letter-spacing: -0.02em; color: #FFFFFF; }
    #i3-nf { position: absolute; left: 26px; right: 26px; top: 560px; height: 210px; border-radius: 34px; background: rgba(245,246,250,0.94); }
    #i3-ic { position: absolute; left: 26px; top: 26px; width: 52px; height: 52px; }
    #i3-ic svg { display: block; width: 52px; height: 52px; }
    #i3-app { position: absolute; left: 96px; top: 30px; font-family: "Inter", sans-serif; font-weight: 600; font-size: 24px; color: «MUTED»;
      letter-spacing: 0.02em; }
    #i3-now { position: absolute; right: 30px; top: 30px; font-family: "Inter", sans-serif; font-weight: 500; font-size: 24px; color: «MUTED»; }
    #i3-tt { position: absolute; left: 96px; top: 68px; font-family: "Inter", sans-serif; font-weight: 700; font-size: 38px; color: «INK»; }
    .i3-sub { position: absolute; left: 96px; top: 118px; font-family: "Inter", sans-serif; font-weight: 500; font-size: 28px; color: «INK2»; }
    #i3-btn { position: absolute; right: 26px; bottom: 24px; height: 58px; padding: 0 28px; border-radius: 29px; background: #E3E6EE;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; line-height: 58px; color: «INK»; transform-origin: 50% 50%; }
"""
    dates = "".join(f'<div id="i3-dt{k}" class="i3-date">{t}</div>' for k, t in enumerate(DAYS))
    subs = "".join(f'<div id="i3-s{k}" class="i3-sub">{t}</div>' for k, t in enumerate(SUBS))
    screen = (f'<div id="i3-wp"></div>{dates}<div id="i3-clock">9:00</div>'
              f'<div id="i3-nf"><div id="i3-ic">{BELL}</div><div id="i3-app">RECORDATORIOS</div><div id="i3-now">ahora</div>'
              f'<div id="i3-tt">Empezar neerlandés</div>{subs}<div id="i3-btn">Posponer</div></div>')
    body = "\n".join([ground(P, "paper"), "    " + phone(P, "phone", PL, PT, PW, PH, screen, sb_dark=False, time="9:00")])
    js = """
      tl.fromTo(q("phone"), { opacity: 0.4, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0);   // there from the cut
      tl.set([q("dt1"), q("dt2"), q("s1"), q("s2")], { opacity: 0 }, 0);
"""
    for k, t in enumerate((round(c["ENE"] - 0.06, 3), round(c["FEB"] - 0.06, 3))):
        js += f"""      tl.to(q("btn"), {{ keyframes: [{{ scale: 0.9, backgroundColor: "#C9CEDA", duration: 0.07 }}, {{ scale: 1, backgroundColor: "#E3E6EE", duration: 0.1 }}] }}, {t});
      tl.to(q("nf"), {{ x: -700, opacity: 0.6, duration: 0.2, ease: "power2.in" }}, {round(t + 0.14, 3)});
      tl.set(q("dt{k}"), {{ opacity: 0 }}, {round(t + 0.3, 3)}); tl.set(q("dt{k + 1}"), {{ opacity: 1 }}, {round(t + 0.3, 3)});
      tl.set(q("s{k}"), {{ opacity: 0 }}, {round(t + 0.3, 3)}); tl.set(q("s{k + 1}"), {{ opacity: 1 }}, {round(t + 0.3, 3)});
      tl.fromTo(q("nf"), {{ x: 0, y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.24, ease: "back.out(1.5)", immediateRender: false }}, {round(t + 0.36, 3)});
"""
    sfx = []
    for t in (c["ENE"] - 0.06, c["FEB"] - 0.06):
        sfx += [(t, "click-soft", 0.3), (t + 0.36, "notification", 0.14)]
    return comp(iid, d, P, css, body, js, c), sfx
