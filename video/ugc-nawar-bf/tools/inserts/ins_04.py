"""ins-04 · «este libro: 70 páginas en español, para imprimir, con vocabulario, gramática, ejercicios prácticos, cómo
pronunciar los sonidos por los que te cambian en inglés cuando abres la boca.» — THE PRODUCT.
Phase 1 (the reveal): on «este libro» the printable workbook (Nawar-blue spiral-bound cover over a stack of printed A4
sheets: logo badge, «Neerlandés para el día a día», «Cuaderno práctico», a «Hoi!» bubble and a yellow BLACK FRIDAY corner
ribbon) turns in in 3D, centred, with a yellow halo, three sparkles and a sheen across the cover; on «70» it glides left
and the yellow «70 páginas» pill pops on the right (the 70 counts up); «En español» (ES flag) on «en español»; «Para
imprimir» (printer) on «imprimir», and the printed sheets behind the cover spread out.
Phase 2 (the contents): on «con» the book shrinks into a header at the top with the three pills stacked beside it, and
the white «Qué incluye» card rises under it; one row lands per word, each with its blue icon tile, a green tick and a
step of the blue progress bar, a soft highlight following the active row: «Vocabulario», «Gramática», «Ejercicios
prácticos» («prácticos» on its own word), «Pronunciación» (on «cómo pronunciar»); on «sonidos» the hard Dutch sounds
g · ui · ij · eu pop as chips under it; on «te cambian» a small English bubble «Sorry, do you speak English?» pops beside
them and on «inglés» it is struck out in red (red ✕, shake). From there a gentle push-in to the end; on «boca» the
sound chips give a little wave and the tick pulses. Dark ground, white card, Nawar blue for you (the book), yellow for
the offer facts, red only for what you avoid."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403

# the book (cover 440×622, A4) — phase 1 centred at BX0, then shifted; phase 2 scaled into the header
BX0, BY0, BW, BH = 320, 390, 440, 622
SHIFT = -214                                   # «70»: the book glides left
S2, BX2, BY2 = 0.55, 236, 246                  # phase 2: scale and top-left of the small book
PX0, PY0, PSTEP = 600, 541, 118                # phase-1 pill column (left, first top, spacing)
PS2, PX2, PY2, PSTEP2 = 0.9, 534, 284, 96      # phase-2 pills (scale, left, first top, spacing)
CARD_TOP, ROW0, RH = 618, 86, 96               # the contents card, first row top, row height
ROWS = [("trans", "Vocabulario"), ("book", "Gramática"), ("pen", "Ejercicios"), ("mic", "Pronunciación")]
SOUNDS = ["g", "ui", "ij", "eu"]
SPARK = '<svg viewBox="0 0 24 24"><path d="M12 0 C13 7.5 16.5 11 24 12 C16.5 13 13 16.5 12 24 C11 16.5 7.5 13 0 12 C7.5 11 11 7.5 12 0 Z" fill="«YEL»"/></svg>'


def build():
    iid, P = "ins-04", "i4"; d = INS[iid]["duration"]
    c = dict(LIB=cue(iid, "libro"), SET=cue(iid, "70"), EN1=cue(iid, "en", 0), IMP=cue(iid, "imprimir"), CON=cue(iid, "con"),
             VOC=cue(iid, "vocabulario"), GRA=cue(iid, "gramatica"), EJE=cue(iid, "ejercicios"), PRA=cue(iid, "practicos"),
             COM=cue(iid, "como"), PRO=cue(iid, "pronunciar"), SON=cue(iid, "sonidos"), TE=cue(iid, "te"),
             ING=cue(iid, "ingles"), BOC=cue(iid, "boca"))
    t2 = round(c["CON"] - 0.1, 3)                                                    # phase 2 starts on «con»
    t_row = [round(c["VOC"] - 0.08, 3), round(c["GRA"] - 0.08, 3), round(c["EJE"] - 0.08, 3), round(c["COM"] - 0.05, 3)]
    t_tick = [round(c["VOC"] + 0.2, 3), round(c["GRA"] + 0.2, 3), round(c["PRA"] + 0.14, 3), round(c["PRO"] + 0.2, 3)]
    t_push = round(c["ING"] + 0.12, 3)
    c.update(T2=t2, T_PUSH=t_push, PUSH_D=round(d - t_push, 3), SHIFT=SHIFT, X2=BX2 - BX0, Y2=BY2 - BY0, S2=S2, PS2=PS2)
    css = """
    #i4-stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px 760px; }
    /* ---- the book ---- */
    #i4-bkm { position: absolute; left: «BX0»px; top: «BY0»px; width: «BW»px; height: «BH»px; transform-origin: 0 0; }
    #i4-halo { position: absolute; left: -330px; top: -239px; width: 1100px; height: 1100px; border-radius: 50%;
      background: radial-gradient(circle at 50% 50%, rgba(255,214,10,0.20) 0%, rgba(255,214,10,0.07) 36%, rgba(255,214,10,0) 64%); }
    #i4-spk { position: absolute; left: 0; top: 0; width: «BW»px; height: «BH»px; }
    .i4-spark { position: absolute; }
    .i4-spark svg { display: block; width: 100%; height: 100%; filter: drop-shadow(0 0 14px rgba(255,214,10,0.55)); }
    #i4-bk, #i4-bkf, #i4-bkt { position: absolute; left: 0; top: 0; width: «BW»px; height: «BH»px; }
    #i4-bkt { transform: rotate(-4deg); }
    .i4-sheet { position: absolute; width: «BW»px; height: «BH»px; border-radius: 6px 14px 14px 6px; background: #FFFFFF; overflow: hidden;
      box-shadow: 0 0 0 1px rgba(12,12,30,0.10), 0 12px 28px rgba(0,0,0,0.30); }
    .i4-sheet i { position: absolute; left: 64px; height: 9px; border-radius: 5px; background: #DCE3EF; }
    #i4-s0 { left: 21px; top: 18px; background: #DDE3EE; }
    #i4-s1 { left: 14px; top: 12px; background: #EBEFF6; }
    #i4-s2 { left: 7px; top: 6px; background: #F7F9FC; }
    #i4-cover { position: absolute; left: 0; top: 0; width: «BW»px; height: «BH»px; border-radius: 8px 16px 16px 8px; overflow: hidden;
      background: linear-gradient(155deg, #2b8dff 0%, «BLUE» 34%, #0849c6 68%, «INDIGO» 100%);
      box-shadow: 0 44px 100px rgba(0,0,0,0.60), 0 10px 26px rgba(0,0,0,0.38), inset 0 0 0 2px rgba(255,255,255,0.12); }
    .i4-deco { position: absolute; border-radius: 50%; }
    #i4-d1 { left: 170px; top: 330px; width: 480px; height: 480px; background: rgba(255,255,255,0.07); }
    #i4-d2 { left: 260px; top: 430px; width: 300px; height: 300px; background: rgba(255,255,255,0.07); }
    #i4-d3 { left: 300px; top: -120px; width: 260px; height: 260px; background: rgba(77,163,255,0.22); }
    #i4-spine { position: absolute; left: 0; top: 0; width: 46px; height: «BH»px; background: linear-gradient(90deg, rgba(0,0,40,0.38) 0%, rgba(0,0,40,0.06) 100%); }
    .i4-hole { position: absolute; left: 12px; width: 13px; height: 13px; border-radius: 50%; background: #06103a; box-shadow: inset 0 2px 3px rgba(0,0,0,0.6); }
    #i4-logo { position: absolute; left: 64px; top: 56px; width: 236px; height: 100px; border-radius: 22px; background: #FFFFFF;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 12px 26px rgba(0,0,40,0.28); }
    #i4-logo img { display: block; width: 200px; height: auto; }
    #i4-title { position: absolute; left: 64px; top: 196px; color: #FFFFFF; white-space: nowrap;
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 54px; line-height: 1.02; letter-spacing: -0.025em; }
    #i4-csub { position: absolute; left: 64px; top: 384px; height: 46px; padding: 0 20px; border-radius: 999px; background: #FFFFFF;
      display: flex; align-items: center; white-space: nowrap; color: «BLUE»;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 20px; line-height: 1; letter-spacing: 0.13em; text-transform: uppercase; }
    #i4-hoi { position: absolute; left: 238px; top: 470px; padding: 14px 26px; border-radius: 26px; border-bottom-left-radius: 8px;
      background: «YEL»; color: «DARK»; transform: rotate(-6deg); box-shadow: 0 12px 24px rgba(0,0,40,0.30);
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 40px; line-height: 1; white-space: nowrap; }
    #i4-cflags { position: absolute; left: 64px; top: 548px; display: flex; align-items: center; gap: 12px; }
    #i4-cflags .i4-flag { width: 46px; height: 31px; flex: 0 0 46px; }
    #i4-cflags .i4-flag svg { width: 46px; height: 31px; }
    #i4-cflags b { display: block; width: 18px; height: 3px; border-radius: 2px; background: rgba(255,255,255,0.7); }
    #i4-rib { position: absolute; left: 220px; top: 47px; width: 300px; height: 46px; transform: rotate(45deg); background: «YEL»;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 14px rgba(0,0,0,0.30);
      font-family: "Poppins", sans-serif; font-weight: 900; font-size: 19px; line-height: 1; letter-spacing: 0.03em; color: «DARK»; white-space: nowrap; padding-top: 2px; box-sizing: border-box; }
    #i4-sheen { position: absolute; left: -260px; top: -160px; width: 150px; height: 960px; transform: rotate(18deg);
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.30) 50%, rgba(255,255,255,0) 100%); }
    .i4-ring { position: absolute; left: -19px; width: 43px; height: 14px; border-radius: 7px;
      background: linear-gradient(180deg, #FFFFFF 0%, #D3D8E4 50%, #8C93A8 100%); box-shadow: 0 3px 5px rgba(0,0,0,0.45); }
    /* ---- the spec pills ---- */
    .i4-pw { position: absolute; left: «PX0»px; transform-origin: 0 0; }
    .i4-spec { height: 84px; padding: 0 32px 0 22px; gap: 15px; font-size: 34px; transform-origin: 0% 50%; }
    .i4-spec svg { width: 44px; height: 44px; }
    .i4-num { display: inline-block; min-width: 50px; font-weight: 900; font-size: 42px; letter-spacing: -0.02em; }
    .i4-spec .i4-flag { width: 50px; height: 34px; flex: 0 0 50px; border-radius: 7px; box-shadow: 0 0 0 3px #FFFFFF; }
    .i4-spec .i4-flag svg { width: 50px; height: 34px; }
    /* ---- the contents card ---- */
    #i4-card { left: 90px; top: «CARD_TOP»px; width: 900px; height: 592px; }
    #i4-kick { position: absolute; left: 40px; top: 30px; height: 40px; display: flex; align-items: center; white-space: nowrap; color: «MUTED»;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 26px; line-height: 1; letter-spacing: 0.14em; text-transform: uppercase; }
    #i4-prog { position: absolute; left: 300px; top: 45px; width: 560px; height: 10px; border-radius: 5px; background: #E6EBF5; overflow: hidden; }
    #i4-progf { position: absolute; left: 0; top: 0; width: 560px; height: 10px; border-radius: 5px; background: «BLUE»; transform-origin: 0 50%; }
    #i4-hl { position: absolute; left: 16px; width: 868px; border-radius: 22px; background: #EEF4FF; transform-origin: 50% 0%; }
    .i4-div { position: absolute; left: 40px; width: 820px; height: 2px; background: #EDF1F7; }
    .i4-row { position: absolute; left: 0; width: 900px; height: «RH»px; }
    .i4-tile { position: absolute; left: 40px; top: 16px; width: 64px; height: 64px; border-radius: 18px; background: «BLUE»; color: #FFFFFF;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 18px rgba(11,109,240,0.30); }
    .i4-tile svg { display: block; width: 38px; height: 38px; }
    .i4-lab { position: absolute; left: 128px; top: 0; height: «RH»px; display: flex; align-items: center; gap: 13px; white-space: nowrap; color: «INK»;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 44px; line-height: 1; letter-spacing: -0.015em; }
    .i4-lab span { display: inline-block; }
    .i4-chk { position: absolute; right: 40px; top: 20px; width: 56px; height: 56px; }
    .i4-chk svg { display: block; width: 56px; height: 56px; }
    #i4-snds { position: absolute; left: 128px; top: «SNDS_TOP»px; height: 96px; display: flex; align-items: center; gap: 14px; }
    .i4-snd { width: 84px; height: 76px; border-radius: 18px; background: #FFFFFF; color: «BLUE»; box-sizing: border-box; box-shadow: inset 0 0 0 3px «BLUE»;
      display: flex; align-items: center; justify-content: center; padding-bottom: 4px;
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 40px; line-height: 1; }
    #i4-bub { position: absolute; left: 530px; top: «BUB_TOP»px; width: 330px; height: 92px; transform-origin: 0% 100%; }
    #i4-bubi { position: absolute; left: 0; top: 0; width: 330px; height: 92px; box-sizing: border-box; padding: 0 20px; border-radius: 26px;
      border-bottom-left-radius: 8px; background: #FFFFFF; display: flex; align-items: center; gap: 14px;
      box-shadow: inset 0 0 0 2px «LINE», 0 12px 26px rgba(12,12,30,0.14); }
    #i4-bico { position: relative; width: 44px; height: 44px; flex: 0 0 44px; }
    #i4-bflag { position: absolute; left: 2px; top: 8px; width: 40px; height: 27px; }
    #i4-bx { position: absolute; left: 0; top: 0; width: 44px; height: 44px; }
    #i4-bx svg { display: block; width: 44px; height: 44px; filter: drop-shadow(0 4px 8px rgba(224,45,60,0.40)); }
    #i4-bubt { font-family: "Inter", sans-serif; font-weight: 600; font-size: 27px; line-height: 1.18; letter-spacing: -0.01em; color: «INK2»; white-space: nowrap; }
    .i4-bl { position: relative; display: inline-block; }
    .i4-st { position: absolute; left: -5px; right: -5px; top: 50%; height: 4px; margin-top: -1px; border-radius: 2px; background: «RED»; transform-origin: 0 50%; }
    #i4-bubr { position: absolute; left: 0; top: 0; width: 330px; height: 92px; border-radius: 26px; border-bottom-left-radius: 8px; box-shadow: inset 0 0 0 3px «RED»; }
"""
    snds_top, bub_top = ROW0 + 3 * RH + RH - 4, ROW0 + 3 * RH + RH
    geo = dict(BX0=BX0, BY0=BY0, BW=BW, BH=BH, PX0=PX0, CARD_TOP=CARD_TOP, RH=RH, SNDS_TOP=snds_top, BUB_TOP=bub_top)
    css = sub(css, geo)
    lines = "".join(f'<i style="top:{80 + 34 * k}px; width:{[290, 250, 310, 200, 280, 240, 300, 180, 260, 290, 220, 270, 230, 300, 190, 250][k]}px;"></i>' for k in range(16))
    sheets = "".join(f'<div id="i4-s{k}" class="i4-sheet">{lines}</div>' for k in range(3))
    ring_tops = [26 + 40 * k for k in range(15)]
    holes = "".join(f'<i class="i4-hole" style="top:{t + 1}px;"></i>' for t in ring_tops)
    rings = "".join(f'<i class="i4-ring" style="top:{t}px;"></i>' for t in ring_tops)
    sparks = "".join(f'<div id="i4-k{k}" class="i4-spark" style="left:{x}px; top:{y}px; width:{s}px; height:{s}px;">{sub(SPARK, {})}</div>'
                     for k, (x, y, s) in enumerate([(-84, 70, 60), (414, -62, 46), (-56, 590, 38)]))
    cover = f"""<div id="i4-cover">
            <div id="i4-d1" class="i4-deco"></div><div id="i4-d2" class="i4-deco"></div><div id="i4-d3" class="i4-deco"></div>
            <div id="i4-spine"></div>{holes}
            <div id="i4-logo"><img src="assets/img/logo-nawar.png" alt="" /></div>
            <div id="i4-title">Neerlandés<br/>para el<br/>día a día</div>
            <div id="i4-csub">Cuaderno práctico</div>
            <div id="i4-hoi">Hoi!</div>
            <div id="i4-cflags"><span class="i4-flag">{FLAG_NL}</span><b></b><span class="i4-flag">{FLAG_ES}</span></div>
            <div id="i4-rib">BLACK FRIDAY</div>
            <div id="i4-sheen"></div>
          </div>"""
    pills = [f'{icon("book")}<b id="i4-num" class="i4-num">70</b><span>páginas</span>',
             f'<span class="i4-flag">{FLAG_ES}</span><span>En español</span>',
             f'{icon("print")}<span>Para imprimir</span>']
    pills_html = "\n".join(f'    <div id="i4-pw{k}" class="i4-pw" style="top:{PY0 + PSTEP * k}px;"><div id="i4-p{k}" class="i4-ypill i4-spec">{h}</div></div>'
                           for k, h in enumerate(pills))
    rows = []
    for k, (ic, lab) in enumerate(ROWS):
        lab_html = f'<span>{lab}</span>' + ('<span id="i4-pra">prácticos</span>' if k == 2 else "")
        rows.append(f'      <div id="i4-r{k}" class="i4-row" style="top:{ROW0 + RH * k}px;"><div id="i4-t{k}" class="i4-tile">{icon(ic)}</div>'
                    f'<div class="i4-lab">{lab_html}</div><div id="i4-c{k}" class="i4-chk">{icon("check")}</div></div>')
    divs = "".join(f'<div class="i4-div" style="top:{ROW0 + RH * k - 1}px;"></div>' for k in range(1, 4))
    snds = "".join(f'<div id="i4-n{k}" class="i4-snd">{s}</div>' for k, s in enumerate(SOUNDS))
    body = "\n".join([ground(P, "dark"), f"""    <div id="i4-stage">
    <div id="i4-card" class="i4-card i4-on-dark">
      <div id="i4-kick">Qué incluye</div>
      <div id="i4-prog"><div id="i4-progf"></div></div>
      <div id="i4-hl" style="top:{ROW0 + 6}px; height:{RH - 12}px;"></div>
      {divs}
{chr(10).join(rows)}
      <div id="i4-snds">{snds}</div>
      <div id="i4-bub"><div id="i4-bubi"><div id="i4-bico"><span id="i4-bflag" class="i4-flag i4-flagd">{FLAG_EN}</span><div id="i4-bx">{icon('xr')}</div></div>
        <div id="i4-bubt"><span class="i4-bl">Sorry, do you<i id="i4-st0" class="i4-st"></i></span><br/><span class="i4-bl">speak English?<i id="i4-st1" class="i4-st"></i></span></div></div>
        <div id="i4-bubr"></div></div>
    </div>
    <div id="i4-bkm">
      <div id="i4-halo"></div>
      <div id="i4-bk"><div id="i4-bkf"><div id="i4-bkt">
          {sheets}
          {cover}
          {rings}
      </div></div></div>
      <div id="i4-spk">{sparks}</div>
    </div>
{pills_html}
    </div>"""])

    # ---------------------------------------------------------------- timeline
    js = """
      // phase 1 · «este libro»: the workbook turns in, centred; halo, sparkles, a sheen across the cover
      tl.fromTo(q("bk"), { opacity: 0, rotationY: -62, rotation: -9, y: 150, scale: 0.8, transformPerspective: 1800 },
        { opacity: 1, rotationY: 0, rotation: 0, y: 0, scale: 1, transformPerspective: 1800, duration: 0.7, ease: "power3.out" }, 0.02);
      tl.fromTo(q("halo"), { opacity: 0, scale: 0.55 }, { opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }, 0.18);
      tl.fromTo(q("sheen"), { x: 0 }, { x: 860, duration: 0.8, ease: "power2.inOut" }, «LIB» + 0.04);
      tl.fromTo(q("bkf"), { y: 0 }, { keyframes: [{ y: -10, duration: 0.8, ease: "sine.inOut" }, { y: 0, duration: 0.8, ease: "sine.inOut" },
        { y: -7, duration: 0.45, ease: "sine.inOut" }, { y: 0, duration: 0.45, ease: "sine.inOut" }] }, 0.72);
"""
    for k in range(3):
        js += (f'      tl.fromTo(q("k{k}"), {{ opacity: 0, scale: 0, rotation: -120 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2.4)" }}, {round(c["LIB"] - 0.06 + 0.1 * k, 3)});\n'
               f'      tl.fromTo(q("k{k}"), {{ scale: 1 }}, {{ keyframes: [{{ scale: 0.55, duration: 0.3, ease: "sine.inOut" }}, {{ scale: 1, duration: 0.3, ease: "sine.inOut" }}], immediateRender: false }}, {round(1.55 + 0.35 * k, 3)});\n')
    js += """
      // «70»: the book glides left, «70 páginas» pops (and counts up); «en español»; «para imprimir» (the sheets spread)
      tl.fromTo(q("bkm"), { x: 0 }, { x: «SHIFT», duration: 0.44, ease: "power3.inOut" }, «SET» - 0.17);
      tl.fromTo(q("p0"), { opacity: 0, scale: 0.5, x: -30 }, { opacity: 1, scale: 1, x: 0, duration: 0.34, ease: "back.out(1.8)" }, «SET» - 0.08);
      (() => { const el = q("num"), o = { n: 0 };
        tl.fromTo(o, { n: 0 }, { n: 70, duration: 0.45, ease: "power2.out", immediateRender: false,
          onUpdate: () => { el.textContent = String(Math.round(o.n)); } }, «SET» - 0.06); })();
      tl.fromTo(q("p1"), { opacity: 0, scale: 0.5, x: -30 }, { opacity: 1, scale: 1, x: 0, duration: 0.34, ease: "back.out(1.8)" }, «EN1» - 0.05);
      tl.fromTo(q("p2"), { opacity: 0, scale: 0.5, x: -30 }, { opacity: 1, scale: 1, x: 0, duration: 0.34, ease: "back.out(1.8)" }, «IMP» - 0.1);
      tl.fromTo(q("s2"), { x: 0, y: 0 }, { x: 5, y: 4, duration: 0.34, ease: "back.out(2)" }, «IMP» - 0.02);
      tl.fromTo(q("s1"), { x: 0, y: 0, rotation: 0 }, { x: 10, y: 8, rotation: 0.8, duration: 0.34, ease: "back.out(2)" }, «IMP» + 0.02);
      tl.fromTo(q("s0"), { x: 0, y: 0, rotation: 0 }, { x: 16, y: 12, rotation: 1.8, duration: 0.34, ease: "back.out(2)" }, «IMP» + 0.06);

      // phase 2 · «con»: the book shrinks into the header, the pills stack beside it, the contents card rises
      tl.fromTo(q("bkm"), { x: «SHIFT», y: 0, scale: 1 }, { x: «X2», y: «Y2», scale: «S2», duration: 0.52, ease: "power3.inOut", immediateRender: false }, «T2»);
      tl.fromTo(q("halo"), { opacity: 1 }, { opacity: 0.55, duration: 0.5, ease: "power2.inOut", immediateRender: false }, «T2»);
      tl.fromTo(q("spk"), { opacity: 1 }, { opacity: 0, duration: 0.25, ease: "power2.in" }, «T2»);
"""
    for k in range(3):
        dx, dy = PX2 - PX0, (PY2 + PSTEP2 * k) - (PY0 + PSTEP * k)
        js += f'      tl.fromTo(q("pw{k}"), {{ x: 0, y: 0, scale: 1 }}, {{ x: {dx}, y: {dy}, scale: «PS2», duration: 0.52, ease: "power3.inOut" }}, {round(t2 + 0.04 * k, 3)});\n'
    js += """      tl.fromTo(q("card"), { opacity: 0, y: 110, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, ease: "power3.out" }, «T2» + 0.16);
      tl.fromTo(q("progf"), { scaleX: 0 }, { scaleX: 0, duration: 0.01 }, 0);
"""
    hl = [(ROW0 + RH * k + 6, RH - 12) for k in range(3)] + [(ROW0 + RH * 3 + 6, RH * 2 - 6)]
    for k in range(4):
        js += f'      // row {k + 1} · «{ROWS[k][1].lower()}»\n'
        # the highlight moves with transforms only (y, scaleY from its first row's box: top/height would snap to pixels)
        if k == 0:
            js += (f'      tl.fromTo(q("hl"), {{ opacity: 0, y: 0, scaleY: 1 }}, {{ opacity: 1, duration: 0.2, ease: "power2.out" }}, {round(t_row[0] - 0.02, 3)});\n')
        else:
            y0, y1 = hl[k - 1][0] - hl[0][0], hl[k][0] - hl[0][0]
            s0, s1 = round(hl[k - 1][1] / hl[0][1], 4), round(hl[k][1] / hl[0][1], 4)
            js += (f'      tl.fromTo(q("hl"), {{ y: {y0}, scaleY: {s0} }}, {{ y: {y1}, scaleY: {s1}, duration: 0.26, '
                   f'ease: "power3.inOut", immediateRender: false }}, {round(t_row[k] - 0.06, 3)});\n')
        js += (f'      tl.fromTo(q("r{k}"), {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, {t_row[k]});\n'
               f'      tl.fromTo(q("t{k}"), {{ scale: 0.3, rotation: -25 }}, {{ scale: 1, rotation: 0, duration: 0.34, ease: "back.out(2.2)" }}, {t_row[k]});\n'
               f'      tl.fromTo(q("c{k}"), {{ opacity: 0, scale: 0.2, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.28, ease: "back.out(2.4)" }}, {t_tick[k]});\n'
               f'      tl.fromTo(q("progf"), {{ scaleX: {k * 0.25} }}, {{ scaleX: {(k + 1) * 0.25}, duration: 0.3, ease: "power3.out", immediateRender: false }}, {t_tick[k]});\n')
        if k == 2:
            js += '      tl.fromTo(q("pra"), { opacity: 0, y: 22, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.26, ease: "back.out(2)" }, «PRA» - 0.06);\n'
    js += "      // «sonidos»: the hard Dutch sounds pop under «Pronunciación»\n"
    t_snd = [round(c["SON"] - 0.06 + 0.09 * k, 3) for k in range(4)]
    for k in range(4):
        js += f'      tl.fromTo(q("n{k}"), {{ opacity: 0, scale: 0.4, y: 24 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.3, ease: "back.out(2.2)" }}, {t_snd[k]});\n'
    js += """      // «te cambian en inglés»: the English bubble pops and is struck out in red
      tl.fromTo(q("bub"), { opacity: 0, scale: 0.6, y: 16 }, { opacity: 1, scale: 1, y: 0, duration: 0.32, ease: "back.out(1.9)" }, «TE» - 0.05);
      tl.fromTo(q("bubr"), { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "power2.out" }, «ING» - 0.04);
      tl.fromTo(q("st0"), { scaleX: 0 }, { scaleX: 1, duration: 0.16, ease: "power2.out" }, «ING» - 0.04);
      tl.fromTo(q("st1"), { scaleX: 0 }, { scaleX: 1, duration: 0.16, ease: "power2.out" }, «ING» + 0.06);
      tl.fromTo(q("bubt"), { color: "«INK2»" }, { color: "«MUTED»", duration: 0.2, ease: "power2.out" }, «ING» + 0.08);
      tl.fromTo(q("bflag"), { opacity: 1 }, { opacity: 0, duration: 0.1 }, «ING» + 0.04);
      tl.fromTo(q("bx"), { opacity: 0, scale: 0.3, rotation: -60 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.28, ease: "back.out(2.4)" }, «ING» + 0.04);
      tl.to(q("bub"), { keyframes: [{ x: -9, duration: 0.05 }, { x: 8, duration: 0.05 }, { x: -5, duration: 0.05 }, { x: 0, duration: 0.05 }] }, «ING» + 0.12);
      // a gentle push-in to the end; a second sheen on the book; on «boca» the chips wave and the tick pulses
      tl.fromTo(q("stage"), { scale: 1 }, { scale: 1.035, duration: «PUSH_D», ease: "sine.inOut" }, «T_PUSH»);
      tl.fromTo(q("sheen"), { x: 0 }, { x: 860, duration: 0.8, ease: "power2.inOut", immediateRender: false }, «T_PUSH» + 0.3);
"""
    for k in range(4):
        js += (f'      tl.fromTo(q("n{k}"), {{ y: 0 }}, {{ keyframes: [{{ y: -14, duration: 0.13, ease: "power2.out" }}, {{ y: 0, duration: 0.2, ease: "power2.in" }}], '
               f'immediateRender: false }}, {round(c["BOC"] - 0.12 + 0.07 * k, 3)});\n')
    js += """      tl.fromTo(q("c3"), { scale: 1 }, { keyframes: [{ scale: 1.22, duration: 0.14, ease: "power2.out" }, { scale: 1, duration: 0.22, ease: "power2.inOut" }],
        immediateRender: false }, «BOC» + 0.1);
"""
    sfx = [(c["LIB"] - 0.06, "sparkle", 0.12), (c["SET"] - 0.08, "pop", 0.15), (c["EN1"] - 0.05, "pop", 0.14), (c["IMP"] - 0.1, "pop", 0.14),
           (t2, "whoosh-short", 0.08)]
    sfx += [(t_row[k], "pop", 0.11) for k in range(4)]
    sfx += [(t_tick[k], "click-soft", 0.13) for k in range(3)] + [(t_tick[3], "ping", 0.08)]
    sfx += [(t_snd[0], "sparkle", 0.09), (c["TE"] - 0.05, "notification", 0.12), (c["ING"] - 0.04, "error", 0.12)]
    return comp(iid, d, P, css, body, js, c), sfx
