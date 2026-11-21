"""ins-03 · «(La realidad es que) cuando te lo explican desde el español avanzas mucho más rápido de lo que crees» —
the VSL's «como si vinieras del inglés» diagram, set vertically on BLUE: three flag nodes (ES bottom-left, EN
top-middle, NL right). The usual route ES → EN → NL is a faded dashed arch from the start. On «desde el español»
the title lands («Desde el» + chip «español») and ES gets a sky ring; on «avanzas» the direct ES → NL line draws,
the detour dims, and a glowing dot zips along it; it arrives on «más»: NL pops with a green tick and the pill
«Más rápido». Then everything holds."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa: F401,F403


def round_flag(svg):
    """the 40×27 flag filling a circle (centre crop)."""
    return svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid slice" ', 1)


def build():
    iid, P = "ins-03", "i3"; d = INS[iid]["duration"]
    c = dict(DES=cue(iid, "desde"), ESP=cue(iid, "espanol"), AVA=cue(iid, "avanzas"), MAS=cue(iid, "mas"))
    # ---- geometry (1080×1920; content zone y 180–1200)
    R = 75                                        # node radius (150 px discs)
    ES, EN, NL = (210, 1030), (540, 500), (870, 858)
    RING = 96                                     # ES sky ring radius
    dx, dy = NL[0] - ES[0], NL[1] - ES[1]; dist = math.hypot(dx, dy); ux, uy = dx / dist, dy / dist
    x0, y0 = ES[0] + ux * (RING + 12), ES[1] + uy * (RING + 12)          # direct line: from the ring …
    x1, y1 = NL[0] - ux * (R + 16), NL[1] - uy * (R + 16)                # … to NL's edge
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.degrees(math.atan2(dy, dx))
    nx, ny = -uy, ux                                                      # normal pointing up-left (into the triangle)
    if ny > 0: nx, ny = -nx, -ny
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    PX, PY = mx + nx * 112, my + ny * 112                                 # «Más rápido» pill centre, inside the triangle
    G = 14                                                                # gap between a line end and a node
    route_a = (f"M {ES[0]} {ES[1] - RING - G} C {ES[0]} {EN[1] + 190} {EN[0] - 210} {EN[1]} {EN[0] - R - G} {EN[1]}")
    route_b = (f"M {EN[0] + R + G} {EN[1]} C {EN[0] + 210} {EN[1]} {NL[0]} {EN[1] + 100} {NL[0]} {NL[1] - R - G}")
    # ---- timing (cues: explican 0.55, desde 0.94, español 1.45, avanzas 1.98, mucho 2.45, más 2.70, rápido 2.98)
    c["ARR"] = round(c["MAS"] - 0.07, 3)          # the dot reaches NL just before «más»
    c["ZIP"] = round(c["ARR"] - 0.26, 3)          # … after a fast 0.26 s zip
    c["SHIFT"] = 196                              # half of «␣español» chip (Poppins 800 84 px): centres «Desde el» alone
    c.update(L=round(L, 1), DX=round(x1 - x0, 1), DY=round(y1 - y0, 1))
    pos = lambda p, r: f"left:{round(p[0] - r)}px; top:{round(p[1] - r)}px;"
    css = f"""
    #i3-h1 {{ top: 206px; }}
    #i3-chip {{ transform-origin: 50% 60%; }}
    #i3-svg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }}
    .i3-node {{ position: absolute; width: {2 * R}px; height: {2 * R}px; border-radius: 50%; background: #FFFFFF;
      box-shadow: 0 30px 70px rgba(4,0,40,0.42), 0 6px 18px rgba(4,0,40,0.24); }}
    .i3-fl {{ position: absolute; left: 14px; top: 14px; width: {2 * R - 28}px; height: {2 * R - 28}px; border-radius: 50%; overflow: hidden; }}
    .i3-fl svg {{ display: block; width: {2 * R - 28}px; height: {2 * R - 28}px; }}
    #i3-en .i3-fl {{ filter: grayscale(0.8); }}
    .i3-fe {{ position: absolute; left: 14px; top: 14px; width: {2 * R - 28}px; height: {2 * R - 28}px; border-radius: 50%;
      box-shadow: inset 0 0 0 2px rgba(12,12,30,0.10); }}
    .i3-lab {{ position: absolute; width: 320px; text-align: center; font-family: "Inter", sans-serif; font-weight: 700; font-size: 25px;
      line-height: 1; letter-spacing: 0.14em; text-indent: 0.14em; color: #FFFFFF; white-space: nowrap; }}
    #i3-ring {{ position: absolute; {pos(ES, RING)} width: {2 * RING}px; height: {2 * RING}px; border-radius: 50%; box-sizing: border-box;
      border: 6px solid «SKY»; box-shadow: 0 0 34px rgba(77,163,255,0.55), inset 0 0 22px rgba(77,163,255,0.30); }}
    #i3-glow {{ position: absolute; {pos(NL, 190)} width: 380px; height: 380px; border-radius: 50%;
      background: radial-gradient(circle, rgba(77,163,255,0.42) 0%, rgba(77,163,255,0.14) 42%, rgba(77,163,255,0) 70%); }}
    #i3-tick {{ position: absolute; left: {NL[0] + 30}px; top: {NL[1] - R - 12}px; width: 62px; height: 62px; border-radius: 50%; background: «GREEN»;
      box-shadow: 0 0 0 5px #FFFFFF, 0 10px 22px rgba(4,0,40,0.35); }}
    #i3-tick svg {{ display: block; width: 62px; height: 62px; }}
    #i3-dotw {{ position: absolute; left: {round(x0, 1)}px; top: {round(y0, 1)}px; width: 0; height: 0; }}
    #i3-tail {{ position: absolute; left: -130px; top: -7px; width: 130px; height: 14px; border-radius: 7px; transform-origin: 100% 50%;
      transform: rotate({round(ang, 2)}deg); background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(190,224,255,0.55) 70%, rgba(255,255,255,0.95) 100%); }}
    #i3-dot {{ position: absolute; left: -15px; top: -15px; width: 30px; height: 30px; border-radius: 50%; background: #FFFFFF;
      box-shadow: 0 0 0 7px rgba(77,163,255,0.35), 0 0 30px 10px rgba(77,163,255,0.75); }}
    #i3-prow {{ position: absolute; left: {round(PX - 300)}px; top: {round(PY - 36)}px; width: 600px; height: 72px; display: flex; justify-content: center; }}
    #i3-pill {{ gap: 14px; padding: 0 30px 0 14px; }}
    #i3-pill svg {{ display: block; width: 46px; height: 46px; }}
"""
    def node(k, p, flag, label, below):
        return (f'    <div id="i3-{k}" class="i3-node" style="{pos(p, R)}"><div class="i3-fl">{round_flag(flag)}</div><div class="i3-fe"></div></div>\n'
                f'    <div id="i3-{k}l" class="i3-lab" style="left:{p[0] - 160}px; top:{p[1] + below}px;">{label}</div>')
    ff = '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="24" fill="«INDIGO»"/><path d="M14 15 L23 24 L14 33 M25 15 L34 24 L25 33" fill="none" stroke="#FFFFFF" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    body = "\n".join([ground(P, "blue"), f"""    <div id="i3-h1" class="i3-h1"><span id="i3-t1" class="i3-w">Desde el</span> <span id="i3-chip" class="i3-chip">español</span></div>
    <div id="i3-glow" data-layout-allow-overlap></div>
    <svg id="i3-svg" viewBox="0 0 1080 1920" data-layout-allow-overlap>
      <g id="i3-route" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-dasharray="16 15">
        <path id="i3-ra" d="{route_a}" /><path id="i3-rb" d="{route_b}" />
      </g>
      <g id="i3-dir">
        <line id="i3-dg" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="«SKY»" stroke-opacity="0.38" stroke-width="24" stroke-linecap="round" stroke-dasharray="{L:.1f} {L + 40:.1f}" />
        <line id="i3-dl" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" stroke-dasharray="{L:.1f} {L + 40:.1f}" />
      </g>
    </svg>
    <div id="i3-dotw" data-layout-allow-overlap><div id="i3-tail"></div><div id="i3-dot"></div></div>
    <div id="i3-ring" data-layout-allow-overlap></div>
{node("en", EN, FLAG_EN, "INGLÉS", R + 24)}
{node("es", ES, FLAG_ES, "ESPAÑOL", RING + 18)}
{node("nl", NL, FLAG_NL, "NEERLANDÉS", R + 24)}
    <div id="i3-tick" data-layout-allow-overlap>{icon('check')}</div>
    <div id="i3-prow"><div id="i3-pill" class="i3-wpill">{ff}<span>Más rápido</span></div></div>"""])
    js = """
      // the map: ES, NL, then the faded EN and the usual detour through it
      tl.fromTo(q("es"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.36, ease: "back.out(1.8)" }, 0.02);
      tl.fromTo(q("esl"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.08);
      tl.fromTo(q("nl"), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.36, ease: "back.out(1.8)" }, 0.1);
      tl.fromTo(q("nll"), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 0.16);
      tl.fromTo(q("en"), { opacity: 0, scale: 0.6 }, { opacity: 0.5, scale: 1, duration: 0.36, ease: "back.out(1.8)" }, 0.18);
      tl.fromTo(q("enl"), { opacity: 0, y: 14 }, { opacity: 0.5, y: 0, duration: 0.3, ease: "power3.out" }, 0.24);
      tl.fromTo(q("route"), { opacity: 0 }, { opacity: 0.42, duration: 0.45, ease: "power2.out" }, 0.22);
      // «desde el español»: the title, the chip, the sky ring on ES
      tl.fromTo(q("t1"), { opacity: 0, y: 30, x: «SHIFT» }, { opacity: 1, y: 0, x: «SHIFT», duration: 0.3, ease: "power3.out" }, «DES» - 0.05);
      tl.to(q("t1"), { x: 0, duration: 0.24, ease: "power3.out" }, «ESP» - 0.13);
      tl.fromTo(q("chip"), { opacity: 0, scale: 0.7, rotation: -1.5 }, { opacity: 1, scale: 1, rotation: -1.5, duration: 0.3, ease: "back.out(1.8)" }, «ESP» - 0.05);
      tl.fromTo(q("ring"), { opacity: 0, scale: 0.78 }, { opacity: 1, scale: 1, duration: 0.36, ease: "back.out(1.8)" }, «ESP» - 0.04);
      tl.to(q("es"), { scale: 1.06, duration: 0.14, ease: "power2.out" }, «ESP» - 0.04);
      tl.to(q("es"), { scale: 1, duration: 0.3, ease: "power2.out" }, «ESP» + 0.1);
      // «avanzas»: the direct line draws, the detour steps back
      tl.fromTo(q("dir"), { opacity: 0 }, { opacity: 1, duration: 0.01 }, «AVA» - 0.05);
      tl.fromTo([q("dl"), q("dg")], { strokeDashoffset: «L» }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.inOut" }, «AVA» - 0.05);
      tl.to(q("route"), { opacity: 0.16, duration: 0.4, ease: "power2.out" }, «AVA» - 0.05);
      tl.to([q("en"), q("enl")], { opacity: 0.36, duration: 0.4, ease: "power2.out" }, «AVA» - 0.05);
      // the dot zips along it and lands on «más»
      tl.fromTo(q("dotw"), { opacity: 0, x: 0, y: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, «ZIP» - 0.06);
      tl.fromTo(q("tail"), { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "none" }, «ZIP»);
      tl.to(q("dotw"), { x: «DX», y: «DY», duration: «ARR» - «ZIP», ease: "power2.in" }, «ZIP»);
      tl.to(q("dotw"), { opacity: 0, duration: 0.08, ease: "none" }, «ARR»);
      // NL: bump, the green tick, the glow; then the pill
      tl.to(q("nl"), { scale: 1.12, duration: 0.12, ease: "power2.out" }, «ARR»);
      tl.to(q("nl"), { scale: 1, duration: 0.34, ease: "back.out(2)" }, «ARR» + 0.12);
      tl.fromTo(q("glow"), { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, «ARR»);
      tl.fromTo(q("tick"), { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.34, ease: "back.out(2)" }, «ARR» + 0.02);
      tl.fromTo(q("pill"), { opacity: 0, y: 22, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, «MAS» - 0.04);
"""
    sfx = [(c["ESP"] - 0.06, "click-soft", 0.18), (c["ZIP"] - 0.04, "whoosh-short", 0.15), (c["ARR"] + 0.02, "ping", 0.2)]
    return comp(iid, d, P, css, body, js, c), sfx
