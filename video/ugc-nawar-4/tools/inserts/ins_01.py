"""ins-01 · «Porque cada mes que esperas es otro mes pidiendo que te traduzcan.» — v2 (the client: v1 «se ve algo IA»;
«no es la gemeente sino el gemeente»; phrases with more pain): a real-looking phone on paper, your chat with Laura.
Under a date chip per month, one message of yours each time — 12 sept «¿Puedes llamar tú al casero?», 3 oct «¿Me
acompañas a la cita del dentista?», 7 nov «¿Vienes conmigo al gemeente?» — and, on «otro mes», today's: «¿Me traduces
esta carta?». Plain chat UI (header with her name, light wallpaper, time and read ticks), no headline, no badges."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

MSGS = [("12 sept", "¿Puedes llamar tú al casero?", "19:42"), ("3 oct", "¿Me acompañas a la cita<br/>del dentista?", "08:15"),
        ("7 nov", "¿Vienes conmigo al gemeente?", "13:06"), ("Hoy", "¿Me traduces esta carta?", "10:21")]
PW, PH, PL, PT = 660, 1090, 210, 150
TICKS = ('<svg viewBox="0 0 34 20"><path d="M2 11 L7 16 L17 4 M13 13 L16 16 L28 3" fill="none" stroke="#3B82F6" stroke-width="3" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def build():
    iid, P = "ins-01", "i1"; d = INS[iid]["duration"]
    c = dict(MES=cue(iid, "mes"), ESP=cue(iid, "esperas"), OTRO=cue(iid, "otro"), TRA=cue(iid, "traduzcan"))
    css = PHONE_CSS + """
    #i1-hd { position: absolute; left: 0; top: 96px; width: 100%; height: 116px; background: #F7F7F9; box-shadow: inset 0 -2px 0 #E4E6EC;
      display: flex; align-items: center; gap: 20px; padding: 0 30px; box-sizing: border-box; }
    #i1-hd svg { display: block; width: 26px; height: 40px; }
    #i1-av { width: 74px; height: 74px; border-radius: 50%; background: #15A3A3; color: #FFFFFF; display: flex; align-items: center;
      justify-content: center; font-family: "Inter", sans-serif; font-weight: 700; font-size: 34px; }
    #i1-nm { font-family: "Inter", sans-serif; font-weight: 700; font-size: 34px; color: «INK»; line-height: 1.1; }
    #i1-st { font-family: "Inter", sans-serif; font-weight: 500; font-size: 24px; color: «MUTED»; }
    #i1-wall { position: absolute; left: 0; top: 212px; width: 100%; bottom: 0; background: #EEF1F6; overflow: hidden; }
    .i1-day { position: absolute; left: 0; width: 100%; display: flex; justify-content: center; }
    .i1-day span { padding: 8px 20px; border-radius: 14px; background: #FFFFFF; font-family: "Inter", sans-serif; font-weight: 600;
      font-size: 22px; color: «MUTED»; box-shadow: 0 1px 0 #DADFE8; }
    #i1-list { position: absolute; left: 0; top: 0; width: 100%; height: 1200px; }
    .i1-m { position: absolute; right: 26px; white-space: nowrap; padding: 18px 24px 14px; border-radius: 28px 28px 8px 28px; background: #DCEBFF;
      font-family: "Inter", sans-serif; font-weight: 500; font-size: 33px; line-height: 1.24; color: «INK»; transform-origin: 100% 100%; }
    .i1-meta { display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-top: 6px; font-size: 20px; color: «MUTED»; }
    .i1-meta svg { display: block; width: 30px; height: 18px; }
    #i1-bar { position: absolute; left: 0; bottom: 0; width: 100%; height: 118px; background: #F7F7F9; box-shadow: inset 0 2px 0 #E4E6EC; }
    #i1-in { position: absolute; left: 28px; right: 110px; top: 22px; height: 62px; border-radius: 31px; background: #FFFFFF;
      box-shadow: inset 0 0 0 2px #E1E4EA; font-family: "Inter", sans-serif; font-size: 26px; color: #A0A6B6; line-height: 62px; padding-left: 26px; }
    #i1-send { position: absolute; right: 26px; top: 20px; width: 66px; height: 66px; border-radius: 50%; background: «BLUE»; }
"""
    back = '<svg viewBox="0 0 26 40"><path d="M20 4 L6 20 L20 36" fill="none" stroke="«BLUE»" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    rows, top = [], 28                                   # (wall px; it shows 728 px between the header and the input bar)
    for k, (day, txt, hh) in enumerate(MSGS):
        rows.append(f'<div id="i1-d{k}" class="i1-day" style="top: {top}px;"><span>{day}</span></div>')
        top += 56
        lines = txt.count("<br/>") + 1
        rows.append(f'<div id="i1-m{k}" class="i1-m" style="top: {top}px;">{txt}<div class="i1-meta"><span>{hh}</span>{TICKS}</div></div>')
        top += 62 + 41 * lines + 24
    shift = max(0, top + 16 - 728)                       # the chat scrolls up as the last message comes in
    screen = (f'<div id="i1-hd">{sub(back, {})}<div id="i1-av">L</div><div><div id="i1-nm">Laura</div><div id="i1-st">en línea</div></div></div>'
              f'<div id="i1-wall"><div id="i1-list">' + "".join(rows) + '</div></div>'
              f'<div id="i1-bar"><div id="i1-in">Mensaje</div><div id="i1-send"></div></div>')
    body = "\n".join([ground(P, "paper"), "    " + phone(P, "phone", PL, PT, PW, PH, screen)])
    starts = [0.0, round(c["MES"] - 0.04, 3), round(c["ESP"] + 0.16, 3), round(c["OTRO"] - 0.06, 3)]
    js = """
      tl.fromTo(q("phone"), { opacity: 0.4, y: 40 }, { opacity: 1, y: 0, duration: 0.32, ease: "power3.out" }, 0);   // there from the cut
"""
    for k, t in enumerate(starts):
        if k:
            js += f'      tl.fromTo(q("d{k}"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.16 }}, {t});\n'
            js += f'      tl.fromTo(q("m{k}"), {{ opacity: 0, y: 30, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(1.5)" }}, {round(t + 0.06, 3)});\n'
    js += f'      tl.to(q("list"), {{ y: -{shift}, duration: 0.26, ease: "power2.out" }}, {round(starts[3] - 0.02, 3)});\n' if shift else ""
    sfx = [(starts[k] + 0.06, "pop", 0.1) for k in (1, 2, 3)]
    return comp(iid, d, P, css, body, js, c), sfx
