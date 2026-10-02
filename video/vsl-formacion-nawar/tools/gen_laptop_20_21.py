#!/usr/bin/env python3
"""Emit compositions/frames/20-pausa.html and 21-portatil.html from ONE shared laptop block.

The laptop (ground, 2D camera, perspective stage, 3D lap / deck / lid / play disc) is produced by the
same functions for both frames with only the id prefix swapped, so the last frame of 20 and the first
frame of 21 are geometrically identical.
"""
import os, json

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PROJ, "compositions", "frames")

# ---------------------------------------------------------------- shared geometry
W, D = 1300, 780                    # lid / deck footprint (local px)
LAP_L, LAP_T = 960 - W // 2, 560 - D // 2   # lap centred at (960, 560)
ROT0 = -24                          # diagonal in-plane rotation of the closed laptop
Z0 = 400                            # closed laptop sits closer to the lens (bigger, crosses the frame)
PERSP = 2400.0
LIFT_END = 4                        # lid lift (deg) at the 20 -> 21 seam
# play disc centre: world (960, 400) -> lid-local (rotate by +24 about the lap centre)
import math
_c, _s = math.cos(math.radians(24)), math.sin(math.radians(24))
PLAY_SY = 380.0                     # projected (on-screen) centre of the play disc
_k = PERSP / (PERSP - (Z0 + 13.5))
_dx, _dy = 0.0, (540.0 + (PLAY_SY - 540.0) / _k) - 560.0
PLAY_U = W / 2 + (_c * _dx - _s * _dy)
PLAY_V = D / 2 + (_s * _dx + _c * _dy)
PLAY_X, PLAY_Y = 960, PLAY_SY      # on-screen centre of the disc (for 2D overlays: ripple, cursor)
DISC_S = 200 * _k                   # on-screen disc diameter
DISC = 200

LID_LAYERS = [1.5 * (k + 1) for k in range(8)]          # 1.5 .. 12
DECK_LAYERS = [-2.0 * (k + 1) for k in range(11)]       # -2 .. -22


def fonts(weights):
    out = []
    for fam, w, f in weights:
        out.append('@font-face { font-family: "%s"; font-weight: %d; font-style: normal; src: url("assets/fonts/%s") format("woff2"); }' % (fam, w, f))
    return "\n    ".join(out)


def shared_css(P):
    lid_layer_css = ""
    deck_layer_css = ""
    return f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Poppins", sans-serif; }}

    /* ---------- ground: NAWAR BLUE + dots + vignette; {P}-dim = the "paused" darkness ---------- */
    #{P}-ground {{ position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, #025dc7 0%, #120081 72%); }}
    #{P}-dots {{
      position: absolute; inset: 0;
      background-image: radial-gradient(circle, rgba(255,255,255,0.07) 1.6px, transparent 1.7px);
      background-size: 28px 28px; background-position: 6px 10px;
    }}
    #{P}-vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse 85% 85% at 50% 50%, rgba(4,0,40,0) 55%, rgba(4,0,40,0.38) 100%); }}
    #{P}-dim {{
      position: absolute; inset: 0;
      background: radial-gradient(ellipse 70% 72% at 50% 46%, rgba(4,0,40,0.16) 0%, rgba(4,0,40,0.30) 45%, rgba(3,0,30,0.70) 100%);
    }}

    /* ---------- 2D camera > perspective stage > 3D laptop ---------- */
    #{P}-cam {{ position: absolute; inset: 0; transform-origin: 960px 540px; }}
    #{P}-stage {{ position: absolute; inset: 0; perspective: 2400px; perspective-origin: 960px 540px; }}
    #{P}-lap {{
      position: absolute; left: {LAP_L}px; top: {LAP_T}px; width: {W}px; height: {D}px;
      transform-style: preserve-3d; transform-origin: {W/2}px {D/2}px; transform: translate3d(0px, 0px, {Z0}px) rotate({ROT0}deg);
    }}
    .{P}-plane {{ position: absolute; left: 0; top: 0; width: {W}px; height: {D}px; border-radius: 44px; }}

    /* table shadow (in the deck's plane, below it) */
    #{P}-shadow {{
      position: absolute; left: 10px; top: 26px; width: {W}px; height: {D}px; border-radius: 70px;
      background: rgba(3,0,28,0.62); box-shadow: 0 0 110px 46px rgba(3,0,28,0.58);
      transform: translateZ(-24px);
    }}
    /* deck: stacked layers = machined thickness; top face carries keyboard + trackpad */
    .{P}-dl {{ box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04); }}
    #{P}-decktop {{
      background: linear-gradient(180deg, #343a4f 0%, #2a2f42 55%, #23273a 100%);
      box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.16), inset 0 3px 0 rgba(255,255,255,0.05);
      overflow: hidden;
    }}
    #{P}-deckglow {{ position: absolute; left: 0; top: 0; width: {W}px; height: {D}px; opacity: 0; background: radial-gradient(ellipse 62% 70% at 50% 0%, rgba(140,185,255,0.22) 0%, rgba(77,163,255,0.08) 45%, rgba(77,163,255,0) 75%); }}
    #{P}-hinge {{ position: absolute; left: 150px; top: 0; width: 1000px; height: 24px; border-radius: 0 0 12px 12px; background: linear-gradient(180deg, #0c0e15 0%, #1a1d29 100%); }}
    .{P}-grille {{
      position: absolute; top: 64px; width: 74px; height: 372px; border-radius: 10px;
      background-image: radial-gradient(circle, rgba(6,7,12,0.85) 1.7px, transparent 2.2px);
      background-size: 10px 10px; background-position: 2px 2px;
    }}
    #{P}-kb {{ position: absolute; left: 175px; top: 60px; width: 950px; height: 380px; display: block; }}
    #{P}-pad {{
      position: absolute; left: 400px; top: 478px; width: 500px; height: 266px; border-radius: 22px;
      background: linear-gradient(180deg, #2f3447 0%, #282c3d 100%);
      box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.10), inset 0 -2px 0 rgba(0,0,0,0.25);
    }}

    /* lid: hinge = its top edge (local); inner face (screen) points down when closed */
    #{P}-lid {{ position: absolute; left: 0; top: 0; width: {W}px; height: {D}px; transform-style: preserve-3d; transform-origin: 50% 0%; }}
    .{P}-ll {{ background: #171a25; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05); }}
    #{P}-inner {{
      background: #0C0C1E; transform: translateZ(0.5px) rotateX(180deg); backface-visibility: hidden;
      box-shadow: inset 0 0 0 7px #2b3044, inset 0 0 0 8.5px rgba(255,255,255,0.10);
    }}
    #{P}-camdot {{ position: absolute; left: {W/2 - 5}px; top: 13px; width: 10px; height: 10px; border-radius: 50%; background: #1d2133; box-shadow: inset 0 0 0 2px #2a2f45; }}
    #{P}-screen {{ position: absolute; left: 30px; top: 30px; width: {W-60}px; height: {D-84}px; border-radius: 12px; overflow: hidden; background: #020208; }}
    #{P}-outer {{
      background: linear-gradient(160deg, #3b4156 0%, #262a3c 52%, #171a28 100%);
      box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.12), inset 0 0 60px rgba(0,0,0,0.25);
      transform: translateZ(13.5px); backface-visibility: hidden; overflow: hidden;
    }}
    #{P}-spec {{
      position: absolute; left: 820px; top: -400px; width: 300px; height: 1600px; transform: rotate(-38deg);
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.075) 50%, rgba(255,255,255,0) 100%);
    }}
    #{P}-spec2 {{
      position: absolute; left: 1010px; top: -400px; width: 70px; height: 1600px; transform: rotate(-38deg);
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 100%);
    }}
    /* the play disc lives ON the lid, counter-rotated so it reads upright */
    #{P}-playpos {{ position: absolute; left: {PLAY_U - DISC/2:.1f}px; top: {PLAY_V - DISC/2:.1f}px; width: {DISC}px; height: {DISC}px; transform: rotate({-ROT0}deg); }}
    #{P}-disc {{
      position: absolute; inset: 0; border-radius: 50%; box-sizing: border-box;
      background: radial-gradient(circle at 34% 26%, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.14) 46%, rgba(255,255,255,0.10) 100%);
      border: 3px solid rgba(255,255,255,0.65);
      box-shadow: 0 22px 50px rgba(0,0,0,0.42), inset 0 0 26px rgba(255,255,255,0.10);
    }}
    #{P}-press {{ position: absolute; inset: 0; border-radius: 50%; background: rgba(6,4,30,0.34); opacity: 0; }}
    #{P}-tri {{ position: absolute; left: 0; top: 0; width: {DISC}px; height: {DISC}px; overflow: visible; }}
"""


def keyboard_svg(P):
    pitch_x, pitch_y = 950 / 15, 62
    keys = []
    # 5 rows from the pattern area, bottom row hand-laid (modifiers + space bar)
    rows = []
    for r in range(5):
        y = 6 + r * pitch_y
        for c in range(15):
            x = c * pitch_x
            rows.append('<rect x="%.1f" y="%.1f" width="%.1f" height="54" rx="8" fill="#252937"></rect>' % (x + 4, y + 4, pitch_x - 8))
    y = 6 + 5 * pitch_y
    xs = [0, 1, 2, 3]
    for c in xs:
        rows.append('<rect x="%.1f" y="%.1f" width="%.1f" height="52" rx="8" fill="#252937"></rect>' % (c * pitch_x + 4, y + 4, pitch_x - 8))
    sx = 4 * pitch_x + 4
    ex = 950 - 4 * pitch_x - 4
    rows.append('<rect x="%.1f" y="%.1f" width="%.1f" height="52" rx="8" fill="#252937"></rect>' % (sx, y + 4, ex - sx))
    for c in range(4):
        rows.append('<rect x="%.1f" y="%.1f" width="%.1f" height="52" rx="8" fill="#252937"></rect>' % (950 - (4 - c) * pitch_x + 4, y + 4, pitch_x - 8))
    return ('<svg id="%s-kb" viewBox="0 0 950 380" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="950" height="380" rx="18" fill="#10121a"></rect>%s</svg>') % (P, "".join(rows))


def laptop_html(P, screen_inner):
    ll = "\n".join('            <div class="%s-plane %s-ll" style="transform: translateZ(%.1fpx);"></div>' % (P, P, z) for z in LID_LAYERS)
    # deck layers: lighter (machined chamfer) near the top, darker toward the bottom
    cols = ["#4a5068", "#3d4258", "#33384c", "#2d3144", "#282c3d", "#24283a", "#212435", "#1e2131", "#1b1e2c", "#181a27", "#151722"]
    dl = "\n".join('          <div class="%s-plane %s-dl" style="transform: translateZ(%.1fpx); background: %s;"></div>' % (P, P, z, cols[i]) for i, z in enumerate(DECK_LAYERS))
    return f"""
    <!-- ======= 2D camera > perspective stage > 3D laptop (shared geometry 20 <-> 21) ======= -->
    <div id="{P}-cam">
      <div id="{P}-stage">
        <div id="{P}-lap">
          <div id="{P}-shadow"></div>
{dl}
          <div id="{P}-decktop" class="{P}-plane">
            <div id="{P}-hinge"></div>
            <div class="{P}-grille" style="left: 78px;"></div>
            <div class="{P}-grille" style="left: 1148px;"></div>
            {keyboard_svg(P)}
            <div id="{P}-pad"></div>
            <div id="{P}-deckglow"></div>
          </div>
          <div id="{P}-lid">
            <div id="{P}-inner" class="{P}-plane">
              <div id="{P}-camdot"></div>
              <div id="{P}-screen">
{screen_inner}
              </div>
            </div>
{ll}
            <div id="{P}-outer" class="{P}-plane">
              <div id="{P}-spec"></div>
              <div id="{P}-spec2"></div>
              <div id="{P}-playpos">
                <div id="{P}-disc"></div>
                <div id="{P}-press"></div>
                <svg id="{P}-tri" viewBox="0 0 200 200"><path d="M 80 62 L 80 138 Q 80 146 87 142 L 142 106 Q 148 100 142 94 L 87 58 Q 80 54 80 62 Z" fill="#FFFFFF"></path></svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>"""


def ground_html(P, dur):
    return f"""    <div id="{P}-ground" class="clip" data-start="0" data-duration="{dur}" data-track-index="0">
      <div id="{P}-dots"></div>
      <div id="{P}-vig"></div>
      <div id="{P}-dim"></div>
    </div>"""


CURSOR_SVG = ('<svg viewBox="0 0 30 46" width="30" height="46" xmlns="http://www.w3.org/2000/svg" style="display:block; overflow:visible;">'
              '<path d="M 1.5 1.5 L 1.5 35.5 L 9.5 27.8 L 14.6 40.2 L 20.2 37.9 L 15.2 25.8 L 26.5 25.8 Z" fill="#FFFFFF" stroke="#000000" stroke-width="2" stroke-linejoin="round"></path></svg>')

CURSOR_CSS = """
    #{P}-cursor {{ position: absolute; left: {cx}px; top: {cy}px; width: 30px; height: 46px; }}
    #{P}-cursori {{ position: absolute; left: 0; top: 0; width: 30px; height: 46px; transform-origin: 2px 2px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.35)); }}
    #{P}-ripple {{
      position: absolute; left: {rx}px; top: {ry}px; width: {d}px; height: {d}px; border-radius: 50%;
      box-sizing: border-box; border: 3px solid #FFFFFF; opacity: 0;
    }}"""

# cursor tip target (just inside the play triangle's lower-right)
TIP_X, TIP_Y = 980, 400
# ripple state at 20's last frame (t=3.20): GSAP power2.out = 1-(1-p)^3, tween 3.05 -> 3.40
_p = (3.20 - 3.05) / 0.35
_e = 1 - (1 - _p) ** 3
RIPPLE_SCALE_SEAM, RIPPLE_OP_SEAM = round(1 + 0.8 * _e, 4), round(0.7 * (1 - _e), 4)

# ======================================================================== FRAME 20
def frame20():
    P = "f20"; DUR = 3.22
    css = fonts([("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 800, "poppins-latin-800-normal.woff2"),
                 ("Poppins", 900, "poppins-latin-900-normal.woff2"), ("Inter", 600, "inter-latin-600-normal.woff2"),
                 ("Caveat", 700, "caveat-latin-700-normal.woff2")])
    css += shared_css(P)
    css += CURSOR_CSS.format(P=P, cx=TIP_X - 2, cy=TIP_Y - 2, rx=round(PLAY_X - DISC_S / 2, 1), ry=round(PLAY_Y - DISC_S / 2, 1), d=round(DISC_S, 1))
    css += f"""
    /* ---------- player chrome (the film is PAUSED) ---------- */
    #{P}-shade {{ position: absolute; left: 0; top: 640px; width: 1920px; height: 440px; background: linear-gradient(180deg, rgba(3,0,28,0) 0%, rgba(3,0,28,0.62) 100%); }}
    #{P}-bar {{
      position: absolute; left: 80px; top: 916px; width: 1760px; height: 72px; box-sizing: border-box;
      display: flex; align-items: center; gap: 30px; padding: 0 36px; border-radius: 999px;
      background: rgba(7,4,31,0.58); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.16), 0 18px 40px rgba(3,0,28,0.35);
    }}
    .{P}-ic {{ position: relative; width: 30px; height: 30px; flex: 0 0 30px; }}
    .{P}-ic svg {{ position: absolute; left: 0; top: 0; width: 30px; height: 30px; display: block; }}
    #{P}-track {{ position: relative; flex: 1 1 auto; height: 6px; border-radius: 3px; background: rgba(255,255,255,0.30); }}
    #{P}-fill {{ position: absolute; left: 0; top: 0; width: 48%; height: 6px; border-radius: 3px; background: #FFFFFF; }}
    #{P}-knob {{ position: absolute; left: 48%; top: 3px; width: 20px; height: 20px; margin: -10px 0 0 -10px; border-radius: 50%; background: #FFFFFF; box-shadow: 0 2px 8px rgba(0,0,0,0.35); }}
    #{P}-time {{ font-family: "Inter", sans-serif; font-weight: 600; font-size: 24px; line-height: 1; color: rgba(255,255,255,0.72); white-space: nowrap; letter-spacing: 0.01em; }}
    #{P}-pause {{ position: absolute; left: 900px; top: 580px; width: 120px; height: 120px; }}
    #{P}-pause i {{ position: absolute; top: 0; width: 38px; height: 120px; border-radius: 10px; background: #FFFFFF; box-shadow: 0 10px 40px rgba(3,0,28,0.45); }}

    /* ---------- the question (2D, over the lid) ---------- */
    .{P}-row {{ position: absolute; left: 0; width: 1920px; display: flex; justify-content: center; align-items: baseline; white-space: nowrap; }}
    .{P}-w {{ display: inline-block; }}
    #{P}-r1 {{ top: 524px; height: 100px; gap: 22px; }}
    .{P}-h2 {{ font-weight: 800; font-size: 84px; line-height: 1.05; letter-spacing: -0.03em; color: #FFFFFF; text-shadow: 0 6px 30px rgba(3,0,28,0.45); }}
    #{P}-r2 {{ top: 606px; height: 160px; }}
    #{P}-dentro {{
      font-weight: 900; font-size: 150px; line-height: 1; letter-spacing: -0.04em; color: #4da3ff;
      text-shadow: 0 0 46px rgba(77,163,255,0.55), 0 8px 30px rgba(3,0,28,0.40); transform-origin: 50% 60%;
    }}
    #{P}-r3 {{ top: 782px; height: 60px; gap: 12px; }}
    .{P}-lead {{ font-weight: 600; font-size: 44px; line-height: 1.2; letter-spacing: -0.01em; color: rgba(255,255,255,0.72); }}
    #{P}-valepos {{ position: absolute; left: 652px; top: 462px; transform: rotate(-4deg); transform-origin: 0 100%; }}
    #{P}-vale {{ font-family: "Caveat", cursive; font-weight: 700; font-size: 64px; line-height: 1; color: #9fd5f5; text-shadow: 0 4px 20px rgba(3,0,28,0.45); }}
"""
    screen_inner = """                <div id="f20-scr-off" style="position:absolute; inset:0; background:#020208;"></div>"""
    html = f"""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    {css}
  </style>

  <div id="root" data-composition-id="20-pausa" data-width="1920" data-height="1080" data-duration="{DUR}">
{ground_html(P, DUR)}
{laptop_html(P, screen_inner)}

    <div id="{P}-shade"></div>
    <div id="{P}-ripple"></div>

    <!-- the question -->
    <div id="{P}-valepos"><div id="{P}-vale" class="{P}-w">Vale,</div></div>
    <div id="{P}-r1" class="{P}-row">
      <span id="{P}-w1" class="{P}-w {P}-h2">¿Y</span>
      <span id="{P}-w2" class="{P}-w {P}-h2">qué</span>
      <span id="{P}-w3" class="{P}-w {P}-h2">hay</span>
    </div>
    <div id="{P}-r2" class="{P}-row"><div id="{P}-shake" class="{P}-w"><span id="{P}-dentro" class="{P}-w">DENTRO?</span></div></div>
    <div id="{P}-r3" class="{P}-row">
      <span id="{P}-w5" class="{P}-w {P}-lead">Te</span>
      <span id="{P}-w6" class="{P}-w {P}-lead">lo</span>
      <span id="{P}-w7" class="{P}-w {P}-lead">cuento.</span>
    </div>

    <!-- player chrome -->
    <div id="{P}-bar">
      <div class="{P}-ic">
        <svg id="{P}-bplay" viewBox="0 0 30 30"><path d="M 8 4.5 L 8 25.5 Q 8 28 10.2 26.7 L 26 16.6 Q 28 15 26 13.4 L 10.2 3.3 Q 8 2 8 4.5 Z" fill="#FFFFFF"></path></svg>
        <svg id="{P}-bpause" viewBox="0 0 30 30" style="opacity:0;"><rect x="6" y="4" width="6.5" height="22" rx="2" fill="#FFFFFF"></rect><rect x="17.5" y="4" width="6.5" height="22" rx="2" fill="#FFFFFF"></rect></svg>
      </div>
      <div id="{P}-track"><div id="{P}-fill"></div><div id="{P}-knob"></div></div>
      <div id="{P}-time">1:37 / 3:22</div>
      <div class="{P}-ic"><svg viewBox="0 0 30 30"><path d="M 4 11 L 9 11 L 15 5.5 L 15 24.5 L 9 19 L 4 19 Z" fill="#FFFFFF"></path><path d="M 19.5 10 Q 23 15 19.5 20 M 22.5 7 Q 28.5 15 22.5 23" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"></path></svg></div>
      <div class="{P}-ic"><svg viewBox="0 0 30 30"><path d="M 4 11 L 4 4 L 11 4 M 19 4 L 26 4 L 26 11 M 26 19 L 26 26 L 19 26 M 11 26 L 4 26 L 4 19" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"></path></svg></div>
    </div>

    <div id="{P}-pause"><i style="left: 6px;"></i><i style="left: 76px;"></i></div>

    <div id="{P}-cursor"><div id="{P}-cursori">{CURSOR_SVG}</div></div>
  </div>

  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const $ = (id) => document.getElementById(id);

      // ===== Scene 1 (0.0-0.6): hard cut to a FROZEN image. Only the pause flash + player bar move. =====
      tl.fromTo($("{P}-pause"), {{ opacity: 1, scale: 1 }}, {{ opacity: 0, scale: 1.15, duration: 0.25, ease: "power2.out" }}, 0);
      tl.fromTo($("{P}-bar"), {{ y: 170 }}, {{ y: 0, duration: 0.3, ease: "power3.out" }}, 0);
      tl.fromTo($("{P}-shade"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, 0);
      // the lid itself is still: rotationX 0 until the very end
      tl.fromTo($("{P}-lid"), {{ rotationX: 0 }}, {{ rotationX: 0, duration: 0.01, ease: "none" }}, 0);

      // ===== Scene 2 (0.6-2.2): the question builds ON the lid =====
      tl.fromTo($("{P}-vale"), {{ opacity: 0, y: 22, rotation: -6 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.3, ease: "power3.out" }}, 0.58);
      [["{P}-w1", 1.05], ["{P}-w2", 1.20], ["{P}-w3", 1.41]].forEach(([id, t]) => {{
        tl.fromTo($(id), {{ opacity: 0, y: 40, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.26, ease: "power3.out" }}, t);
      }});
      tl.fromTo($("{P}-dentro"), {{ opacity: 0, scale: 1.25, filter: "blur(10px)" }},
        {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }}, 1.53);
      // 3-frame micro-shake of the text only
      tl.set($("{P}-shake"), {{ x: 0 }}, 0);
      tl.set($("{P}-shake"), {{ x: 7, y: -2 }}, 1.70);
      tl.set($("{P}-shake"), {{ x: -6, y: 2 }}, 1.7334);
      tl.set($("{P}-shake"), {{ x: 3, y: -1 }}, 1.7667);
      tl.set($("{P}-shake"), {{ x: 0, y: 0 }}, 1.80);

      // ===== Scene 3 (2.2-3.22): "Te lo cuento." + cursor clicks play =====
      [["{P}-w5", 2.24], ["{P}-w6", 2.36], ["{P}-w7", 2.45]].forEach(([id, t]) => {{
        tl.fromTo($(id), {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.24, ease: "power2.out" }}, t);
      }});
      // cursor enters from bottom-right, glides to the play disc
      tl.fromTo($("{P}-cursor"), {{ x: 1020, y: 700 }}, {{ x: 0, y: 0, duration: 0.65, ease: "power2.inOut" }}, 2.30);
      // click
      tl.fromTo($("{P}-cursori"), {{ scale: 1 }}, {{ scale: 0.86, duration: 0.05, ease: "power2.out" }}, 3.05);
      tl.to($("{P}-cursori"), {{ scale: 1, duration: 0.08, ease: "power2.out" }}, 3.10);
      tl.fromTo($("{P}-press"), {{ opacity: 0 }}, {{ opacity: 1, duration: 0.06, ease: "power2.out" }}, 3.05);
      tl.fromTo($("{P}-ripple"), {{ opacity: 0.7, scale: 1 }}, {{ opacity: 0, scale: 1.8, duration: 0.35, ease: "power2.out", immediateRender: false }}, 3.05);
      tl.set($("{P}-ripple"), {{ opacity: 0 }}, 0);
      // player icon flips to pause (= playing)
      tl.set($("{P}-bplay"), {{ opacity: 1 }}, 0);
      tl.set($("{P}-bpause"), {{ opacity: 0 }}, 0);
      tl.set($("{P}-bplay"), {{ opacity: 0 }}, 3.12);
      tl.set($("{P}-bpause"), {{ opacity: 1 }}, 3.12);
      // the lid starts to lift on its hinge (continues in 21)
      tl.to($("{P}-lid"), {{ rotationX: {LIFT_END}, duration: 0.09, ease: "power2.in" }}, 3.10);

      window.__timelines["20-pausa"] = tl;
    }})();
  </script>
</template>
"""
    return html


# ======================================================================== FRAME 21
def frame21():
    P = "f21"; DUR = 6.22
    css = fonts([("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 800, "poppins-latin-800-normal.woff2"),
                 ("Poppins", 900, "poppins-latin-900-normal.woff2"), ("Inter", 600, "inter-latin-600-normal.woff2")])
    css += shared_css(P)
    css += CURSOR_CSS.format(P=P, cx=TIP_X - 2, cy=TIP_Y - 2, rx=round(PLAY_X - DISC_S / 2, 1), ry=round(PLAY_Y - DISC_S / 2, 1), d=round(DISC_S, 1))
    SW, SH = W - 60, D - 84
    css += f"""
    /* ---------- screen content ---------- */
    .{P}-vwrap {{ position: absolute; left: 0; top: 0; width: {SW}px; height: {SH}px; transform-origin: 50% 50%; }}
    .{P}-vid {{ position: absolute; left: 0; top: 0; width: {SW}px; height: {SH}px; object-fit: cover; display: block; }}
    #{P}-boot {{ position: absolute; inset: 0; background: radial-gradient(ellipse 70% 80% at 50% 50%, #0d0a3c 0%, #05031a 55%, #020208 100%); }}
    #{P}-bootglow {{
      position: absolute; left: {SW/2 - 420}px; top: {SH/2 - 300}px; width: 840px; height: 600px; border-radius: 50%;
      background: radial-gradient(ellipse at 50% 50%, rgba(77,163,255,0.62) 0%, rgba(11,109,240,0.30) 36%, rgba(11,109,240,0) 70%);
    }}
    #{P}-logo {{ position: absolute; left: {SW/2 - 260}px; top: {SH/2 - 93}px; width: 520px; height: 186px; display: block; }}
    #{P}-off {{ position: absolute; inset: 0; background: #020208; }}
    #{P}-cutflash {{ position: absolute; inset: 0; background: #FFFFFF; opacity: 0; }}
    #{P}-glass {{
      position: absolute; inset: 0;
      background: linear-gradient(118deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.035) 33%, rgba(255,255,255,0) 34%, rgba(255,255,255,0) 100%);
    }}
    .{P}-sweep {{
      position: absolute; left: 0; top: -300px; width: 260px; height: {SH + 600}px; transform-origin: 50% 50%;
      background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.20) 45%, rgba(255,255,255,0.32) 50%, rgba(255,255,255,0.20) 55%, rgba(255,255,255,0) 100%);
    }}

    /* ---------- drop flash ---------- */
    #{P}-flash {{ position: absolute; inset: 0; background: #FFFFFF; opacity: 0; }}

    /* ---------- right column: 16 SEMANAS de formación guiada ---------- */
    #{P}-col {{ position: absolute; left: 1150px; top: 30px; width: 690px; height: 1080px; }}
    #{P}-num {{
      position: absolute; left: -8px; top: 196px; height: 300px;
      font-weight: 900; font-size: 300px; line-height: 1; letter-spacing: -0.045em; color: #FFFFFF; white-space: nowrap;
      text-shadow: 0 0 70px rgba(77,163,255,0.60), 0 0 22px rgba(77,163,255,0.35); transform-origin: 0% 70%;
    }}
    #{P}-sem {{
      position: absolute; left: 0; top: 500px; font-weight: 800; font-size: 84px; line-height: 1.05;
      letter-spacing: 0.04em; color: #FFFFFF; white-space: nowrap;
    }}
    #{P}-sub {{ position: absolute; left: 2px; top: 606px; display: flex; gap: 12px; white-space: nowrap; }}
    .{P}-lead {{ display: inline-block; font-weight: 600; font-size: 44px; line-height: 1.2; letter-spacing: -0.01em; color: rgba(255,255,255,0.72); }}
    #{P}-guiada {{ color: #4da3ff; }}
    #{P}-pills {{ position: absolute; left: 2px; top: 712px; width: 680px; height: 14px; }}
    .{P}-pill {{ position: absolute; top: 0; width: 34px; height: 12px; border-radius: 6px; background: rgba(255,255,255,0.22); overflow: hidden; }}
    .{P}-pf {{ position: absolute; left: 0; top: 0; width: 34px; height: 12px; border-radius: 6px; background: #4da3ff; transform-origin: 0% 50%; box-shadow: 0 0 12px rgba(77,163,255,0.8); }}
"""
    screen_inner = f"""                <div id="{P}-v1wrap" class="{P}-vwrap">
                  <video id="{P}-vid1" class="clip {P}-vid" src="assets/video/nuestra-vision.mp4" muted playsinline
                    data-start="1.8" data-duration="1.5" data-media-start="0" data-hf-media-start-basis="local" data-track-index="2"></video>
                </div>
                <div id="{P}-v2wrap" class="{P}-vwrap">
                  <video id="{P}-vid2" class="clip {P}-vid" src="assets/video/inicio-home.mp4" muted playsinline
                    data-start="3.3" data-duration="2.92" data-media-start="1.4" data-hf-media-start-basis="local" data-track-index="2"></video>
                </div>
                <div id="{P}-boot">
                  <div id="{P}-bootglow"></div>
                  <img id="{P}-logo" src="assets/img/logo-nawar.png" alt="Nawar">
                </div>
                <div id="{P}-off"></div>
                <div id="{P}-cutflash"></div>
                <div id="{P}-glass"></div>
                <div id="{P}-sweep1" class="{P}-sweep"></div>
                <div id="{P}-sweep2" class="{P}-sweep"></div>"""
    pills = "\n".join('        <div class="%s-pill" style="left: %dpx;"><div id="%s-pf%d" class="%s-pf"></div></div>' % (P, i * 43, P, i, P) for i in range(16))
    html = f"""<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    {css}
  </style>

  <div id="root" data-composition-id="21-portatil" data-width="1920" data-height="1080" data-duration="{DUR}">
{ground_html(P, DUR)}
{laptop_html(P, screen_inner)}

    <div id="{P}-ripple"></div>
    <div id="{P}-cursor"><div id="{P}-cursori">{CURSOR_SVG}</div></div>

    <!-- right column -->
    <div id="{P}-col">
      <div id="{P}-num"><span id="{P}-numtxt">16</span></div>
      <div id="{P}-sem">SEMANAS</div>
      <div id="{P}-sub">
        <span id="{P}-w3" class="{P}-lead">de</span>
        <span id="{P}-w4" class="{P}-lead">formación</span>
        <span id="{P}-guiada" class="{P}-lead">guiada</span>
      </div>
      <div id="{P}-pills">
{pills}
      </div>
    </div>

    <div id="{P}-flash"></div>
  </div>

  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const $ = (id) => document.getElementById(id);

      // ===== Scene 1 (0.0-1.0): ON THE DROP the lid swings open in 3D =====
      tl.fromTo($("{P}-flash"), {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.25, ease: "power2.out" }}, 0);
      tl.fromTo($("{P}-dim"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, 0);
      // lid: hinge rotation 4 deg (seam) -> 112 deg
      tl.fromTo($("{P}-lid"), {{ rotationX: {LIFT_END} }}, {{ rotationX: 112, duration: 0.85, ease: "power3.out" }}, 0);
      // whole laptop: top-down diagonal -> 3/4 front view
      tl.fromTo($("{P}-lap"), {{ rotation: {ROT0}, rotationX: 0, rotationY: 0, x: 0, y: 0, z: {Z0} }},
        {{ rotation: 0, rotationX: 66, rotationY: 18, x: 0, y: 272, z: -800, duration: 1.0, ease: "power3.out" }}, 0);
      // the pressed play disc releases; the click ripple finishes; the cursor is flung off with the lid
      tl.fromTo($("{P}-press"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.2, ease: "power1.out" }}, 0);
      tl.fromTo($("{P}-ripple"), {{ opacity: {RIPPLE_OP_SEAM}, scale: {RIPPLE_SCALE_SEAM} }}, {{ opacity: 0, scale: 1.8, duration: 0.15, ease: "power1.out" }}, 0);
      tl.fromTo($("{P}-cursor"), {{ x: 0, y: 0, opacity: 1 }}, {{ x: 160, y: -560, opacity: 0, duration: 0.32, ease: "power2.out" }}, 0);
      tl.fromTo($("{P}-cursori"), {{ scale: 1, rotation: 0 }}, {{ scale: 1.5, rotation: 28, duration: 0.32, ease: "power2.out" }}, 0);
      // screen powers on, light streak crosses the glass
      tl.fromTo($("{P}-off"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, ease: "power1.inOut" }}, 0.5);
      // the screen's light spills onto the keyboard deck
      tl.fromTo($("{P}-deckglow"), {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.6, ease: "power2.out" }}, 0.9);
      tl.to($("{P}-deckglow"), {{ opacity: 1, duration: 0.4, ease: "power2.out" }}, 1.9);
      tl.fromTo($("{P}-sweep1"), {{ x: -420, rotation: 22 }}, {{ x: {SW + 180}, rotation: 22, duration: 0.55, ease: "power2.inOut" }}, 0.6);

      // ===== Scene 2 (0.9-2.0): boot screen - the logo blooms; orbit starts =====
      tl.fromTo($("{P}-logo"), {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, 0.9);
      tl.fromTo($("{P}-bootglow"), {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: "power2.out" }}, 0.9);
      tl.fromTo($("{P}-lap"), {{ rotationY: 18 }}, {{ rotationY: -12, duration: {DUR - 1.0:.2f}, ease: "sine.inOut", immediateRender: false }}, 1.0);
      tl.fromTo($("{P}-cam"), {{ scale: 1 }}, {{ scale: 1.035, duration: 2.72, ease: "sine.inOut" }}, 1.0);

      // ===== Scene 3 (2.0-3.9): the logo dissolves into the school; real footage inside the screen =====
      tl.fromTo($("{P}-boot"), {{ opacity: 1 }}, {{ opacity: 0, duration: 0.4, ease: "power1.inOut" }}, 1.86);
      tl.fromTo($("{P}-logo"), {{ filter: "blur(0px)" }}, {{ scale: 1.22, filter: "blur(8px)", duration: 0.4, ease: "power2.in", immediateRender: false }}, 1.86);
      tl.fromTo($("{P}-v1wrap"), {{ scale: 1.12 }}, {{ scale: 1, duration: 1.5, ease: "power2.out" }}, 1.8);
      // in-screen cut to the platform dashboard
      tl.fromTo($("{P}-cutflash"), {{ opacity: 0 }}, {{ opacity: 0, duration: 0.01 }}, 0);
      tl.fromTo($("{P}-cutflash"), {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.22, ease: "power2.out", immediateRender: false }}, 3.3);
      tl.fromTo($("{P}-v2wrap"), {{ scale: 1.08 }}, {{ scale: 1, duration: 0.6, ease: "power3.out" }}, 3.3);
      // the screen catches a light sweep as it turns
      tl.fromTo($("{P}-sweep2"), {{ x: -420, rotation: 22 }}, {{ x: {SW + 180}, rotation: 22, duration: 0.8, ease: "power1.inOut" }}, 2.55);

      // ===== Scene 4 (3.9-6.22): laptop glides to the left third; 16 SEMANAS lands on the voice =====
      tl.to($("{P}-cam"), {{ scale: 0.82, x: -330, y: 0, duration: 0.55, ease: "power3.inOut" }}, 3.72);
      // 16 slams on "Dieciseis" with a 1 -> 16 count
      const cnt = {{ v: 1 }};
      const numtxt = $("{P}-numtxt");
      tl.fromTo(cnt, {{ v: 1 }}, {{ v: 16, duration: 0.35, ease: "power2.out",
        onUpdate: () => {{ numtxt.textContent = String(Math.round(cnt.v)); }} }}, 4.17);
      tl.fromTo($("{P}-num"), {{ opacity: 0, scale: 1.25, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }}, 4.17);
      tl.fromTo($("{P}-sem"), {{ opacity: 0, y: 46, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }}, 4.80);
      tl.fromTo($("{P}-w3"), {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.26, ease: "power3.out" }}, 5.14);
      tl.fromTo($("{P}-w4"), {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.26, ease: "power3.out" }}, 5.23);
      tl.fromTo($("{P}-guiada"), {{ opacity: 0, y: 24, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.out" }}, 5.76);
      // the 16-week route: empty pills arrive with "semanas", fill left -> right up to "guiada"
      tl.fromTo(Array.from($("{P}-pills").children), {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.22, ease: "power2.out", stagger: 0.012 }}, 4.84);
      for (let i = 0; i < 16; i++) {{
        tl.fromTo($("{P}-pf" + i), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.12, ease: "power2.out" }}, 4.98 + i * 0.05);
      }}

      window.__timelines["21-portatil"] = tl;
    }})();
  </script>
</template>
"""
    return html


if __name__ == "__main__":
    open(os.path.join(OUT, "20-pausa.html"), "w").write(frame20().strip())
    open(os.path.join(OUT, "21-portatil.html"), "w").write(frame21().strip())
    json.dump([{"t": 0.0, "sfx": "click-soft", "volume": 0.25}, {"t": 3.05, "sfx": "click", "volume": 0.35}],
              open(os.path.join(OUT, "20-pausa.sfx.json"), "w"), indent=2)
    json.dump([{"t": 0.0, "sfx": "impact-bass-1", "volume": 0.5}, {"t": 0.02, "sfx": "whoosh-cinematic", "volume": 0.35},
               {"t": 1.0, "sfx": "sparkle", "volume": 0.25}, {"t": 4.19, "sfx": "pop", "volume": 0.3}],
              open(os.path.join(OUT, "21-portatil.sfx.json"), "w"), indent=2)
    print("ok")
