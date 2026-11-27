#!/usr/bin/env python3
"""Build one self-contained packet per frame + the shared role file.

.hyperframes/frame-packets/_role.md      = hyperframes frame-worker core contract + tools/role_delta.md
.hyperframes/frame-packets/<id>.md       = frame header, storyboard block, exact word cues,
                                            neighbours, shared geometry, asset inventory, references
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.expanduser("~/.claude/skills")
OUT = os.path.join(ROOT, ".hyperframes", "frame-packets")

ASSETS = """\
Images (assets/img/, all real, use them as-is — never redraw the platform):
- logo-nawar.png 754×269 — transparent Nawar wordmark (red/white/blue letters, black outline, Spanish-flag swoosh).
- ui-eventos-calendario.png 2048×978 (rounded alpha corners) — platform "Eventos" calendar, Sept 2026, several "Clase en directo" entries.
- ui-consulta-respondida.png 2048×1064 — consulta modal: «por qué a veces veo hij werkt y otras werk jij?» answered by Team Nawar (student name blurred). Modal ≈ x 560–1510, y 250–700.
- ui-videoclase-verbos.png 2048×1201 (browser window) — video lesson «¿Cómo conjugar verbos?» with the teacher's webcam.
- ui-lezen-texto.png 2048×1447 — reading exercise (Dutch text + question «¿Qué es el "gezin"?»).
- ui-luisteren-audio.png 1902×1080 — listening exercise «De familiefoto's» with waveform player.
- ui-curso-desktop.png 2048×1037 / ui-curso-desktop-17.png 2048×988 — course page «Formación Nawar A0-A1 · De cero a tu primera conversación».
- ui-curso-movil.png 634×1380 — the course page on mobile (fits a phone screen).
- web-edificio-nawar.png 2048×1270 — website hero: 3D "Nawar" sign on a building, «Ayudarte a aprender neerlandés».
- web-hero-aprende.png 2048×1311 — website hero «Aprende neerlandés de verdad» (blue).
- web-ebook.png 1705×872 — ebook landing.
Videos (assets/video/, 2560×1376, 30 fps, silent — always `muted`):
- inicio-home.mp4 9.7 s — dashboard: 0–3.0 «Hola, Team» + continue lesson + «Tu repaso de hoy»; 3.0–4.0 scroll to courses/community; 4.0–9.7 «Esta semana te toca» + «Hoja de ruta» weekly tasks (Semana 1 «Preséntate en neerlandés a una persona real…», «Pedir perdón y por favor…»; Semana 2 «Saluda con la hora correcta…») + «¿Tienes dudas?» banner.
- formacion-cv.mp4 6.2 s — course page hero (0–1.0) then scroll through the module list (MODULE 1 – OVER JOU …, lessons with ✓).
- clases-video-dentro.mp4 23.2 s — inside a lesson: 0–7.5 video class slide «Dit is / Dit zijn» with the NATIVE TEACHER's webcam tile at the slide's top-left (≈ x 840–1190, y 175–375 in the 2560×1376 source); 8–14 lesson summary; 15–17 reading; 18–23 quiz.
- consulta-nueva.mp4 11.6 s — opening a new consulta: category «Gramática», typing «cómo se traduce gezellig?», then «Publicar consulta».
- flashcards.mp4 20.1 s (1718×842, NEW v2) — the REAL flashcards tool inside a lesson: left blue sidebar (course
  modules), top lesson header + progress, center a flashcard (≈ x 830–1230, y 220–400) with «Repasar» (red) / «Ya lo sé»
  (green) buttons under it, a «¿Tienes una duda sobre esta lección?» box below. Sequence (approx.): 0–1.5 «el bocadillo»,
  2–3.5 flipped «het broodje» (+ Escuchar), 5 «wie», 6 «quién», 8 «el café», 9 «de vis», 10 «el pescado», 13 «willen»,
  14 «venir», 15 «komen», 16 «no / ningún / ninguna», 17 «geen», 18–20 «cuánto / cuánta / cuántos».
- completa-frase.mp4 19.1 s (1718×690, NEW v2) — REAL «Completa la frase» exercise: sentence «Een koffie, ___ (por favor)»
  (input ≈ x 640–760, y 150–175), typing the answer ~4–7 s, «Comprobar» 8–9 s, green «¡Correcto!» bar ~10 s; second
  sentence «Ik ___ elke dag koffie. (beber)» 11–17 s, ¡Correcto! ~18 s. Left blue sidebar lists MODULE 4–9.
- nuestra-vision.mp4 4.5 s (1722×904, NEW v2) — the REAL website: hero with the 3D "Nawar" sign on the school building +
  «Ayudarte a aprender neerlandés» (0–2.8 s), then scrolls to the vision text «Creemos que aprender neerlandés no debería
  ser una barrera…» (3.0–4.5 s).
New image: ui-ordena-palabras.png 879×434 — REAL «Ordena las palabras» exercise (Les 1 — Eten en drinken): «Ordena:
"Quiero un vaso de agua, por favor."», dashed answer area, chips wil · een · glas · alsjeblieft. · water, · Ik,
buttons Reiniciar / Comprobar.
Real module names (sidebar): MODULE 1 – Over jou · 2 – Familie & vrienden · 3 – Eten en drinken · 4 – Het werk ·
5 – Hobby's & vrije tijd · 6 – Thuis & wonen · 7 – Gezondheid · 8 – Vervoer & reizen · 9 – (title not confirmed:
show it locked/blurred) · 10 – (not confirmed: locked/blurred). Lesson items inside a module: Video · Samenvatting ·
Flashcards · Oefening · Lezen · Luisteren · Spreken.
To inspect any video yourself: ffmpeg -ss <t> -i assets/video/<file>.mp4 -frames:v 1 /tmp/claude-0/-home-user-nawar-web/36d31257-d6ae-5587-b324-a9f00bcc433b/scratchpad/<name>.png  (then Read it).
v1 frames for reference/reuse (read-only!): compositions/frames_v1/*.html (e.g. 20-por-dentro, 21-tu-ritmo,
22-clase-directo, 25-end-card, 06-atascado).
- paul-clase-1.mp4 10.1 s (2502×992, NEW v3) — a REAL module video lesson: platform sidebar (left ≈0–430 px) + teacher
  PAUL's camera big (≈ x 740–1330, full height) + slide «Wat doe jij in je vrije tijd?» (matching exercise). Crop to
  Paul's camera to use him as the live-class teacher.
- paul-clase-2.mp4 14.3 s (2424×1238, NEW v3) — another REAL module video with PAUL: slide «De structuur» (ZIN + OM … TE +
  infinitief) with his webcam tile top-left (≈ x 230–490, y 55–205 of a 1600-wide frame ⇒ scale ×1.515) and the video
  player bar (play, 2:07–2:09, volume, fullscreen) at the bottom; «Ver la presentación (PDF)» card under the player.
Device: ALWAYS use the realistic MacBook / macOS window from tools/mac_mockup.md (content area exactly 16:9, URL
`app.holandesnawar.com`). Reference pilots: compositions/frames/12-metodo.html and 14-supervivencia.html.
Owner's style reference (Offlesson VSL, vertical screen recording): /tmp/claude-0/-home-user-nawar-web/36d31257-d6ae-5587-b324-a9f00bcc433b/scratchpad/material/objetivo.mp4
(contact sheet: /tmp/claude-0/-home-user-nawar-web/36d31257-d6ae-5587-b324-a9f00bcc433b/scratchpad/material/f_obj/sheet1.jpg).
Audio: none in frames (SFX via the sidecar).
"""

COMPONENTS = """\
Reference implementations installed in compositions/components/ (read for technique; copy/adapt the
code INTO your frame with your fNN- prefix; do not mount them as separate compositions):
- headline-slam.html — heavyweight headline scales down into frame, lands with deterministic 3-frame shake.
- shutter-slam.html — one word thrown through single-property beats under shutter blur.
- char-slam-explode.html — glyphs scatter then reassemble with a slam.
- caption-kinetic-slam.html — full-screen single-word display, alternating entrance directions.
- kinetic-type-swap.html — held sentence with one masked slot rolling through alternatives.
- whip-pan-cut.html — full-frame whip with capped directional motion blur.
- zoom-through-transition.html — zooms through a focal card into the next scene.
- chat-message.html — one chat message arriving from its sender's corner (measured entry).
- browser-device-stage.html / device-frame-stage.html / parallax-device-dive.html — device chrome stages.
- light-sweep-pass.html — a soft diagonal light band crossing a scene once.
- conic-progress-ring.html — progress ring + center count settling together.
- offset-path-traveler.html — an element following an authored SVG path with tangent rotation.
Motion rule recipes (mechanics, seek-safe): ~/.claude/skills/hyperframes-animation/rules/<id>.md — e.g.
kinetic-beat-slam, dynamic-content-sequencing, discrete-text-sequence, svg-path-draw, counting-dynamic-scale,
coordinate-target-zoom, center-outward-expansion, motion-blur-streak, spring-pop-entrance,
depth-of-field-blur, css-marker-patterns, scale-swap-transition, stat-bars-and-fills, hacker-flip-3d,
avatar-cloud-network, waterfall-entry, 3d-page-scroll, multi-phase-camera, svg-icon-enrichment.
Within-frame seams: ~/.claude/skills/product-launch-video/references/cut-catalog.md.
"""

GEOMETRY = {
    "path": """\
SHARED GEOMETRY — module path (frames 20 and 21 MUST use exactly this):
- Full-frame SVG, viewBox "0 0 1920 1080".
- Road path d = "M 120 840 C 210 830 250 790 300 760 C 420 690 500 520 640 520 C 780 520 840 720 980 720 C 1120 720 1180 470 1320 470 C 1460 470 1540 660 1640 660 C 1720 660 1760 620 1820 600"
  base stroke rgba(255,255,255,0.20) width 14, round caps; progress overlay = same path in #4da3ff width 14
  drawn (stroke-dashoffset) from the start up to the last completed node.
- Node discs (radius 52) centered at N1 (300,760) · N2 (640,520) · N3 (980,720) · N4 (1320,470) · N5 (1640,660).
  Labels (Inter 600 26px, white) centered 96 px BELOW each node center:
  "1 · Over jou" · "2 · Familie & vrienden" · "3 · Eten en drinken" · "4 · Het werk" · "5 · Hobby's & vrije tijd".
- Node states: done = #34D399 disc + white ✓; open = #4da3ff disc + open padlock (white); locked =
  rgba(255,255,255,0.14) disc + 1.5px rgba(255,255,255,0.35) ring + closed padlock (rgba(255,255,255,0.6)).
- Top-left pill (x=80, y=70): "Formación Nawar A0 → A1" (pill on blue).
- END STATE of frame 20 == START STATE of frame 21: N1 done, N2 done, N3 open, N4 locked, N5 locked;
  progress overlay drawn from the path start to N2; no laptop, no heading; pill visible; ground nawar-blue.
""",
    "constellation": """\
SHARED GEOMETRY — community constellation (frames 23 and 24 MUST use exactly this):
- Center pill «Comunidad Nawar» centered at (960, 470), 460×96, white fill, indigo text (Poppins 700 40px).
- 14 avatar discs (center x, center y, diameter, initials, fill, text color):
  (560,300,104,"MA",#0b6df0,white) (760,230,88,"JL",#9fd5f5,#1D0084) (1180,220,96,"SO",#FFFFFF,#1D0084)
  (1380,310,104,"PE",#4da3ff,white) (1500,470,88,"LU",#21468C,white) (1390,640,100,"AN",#1D0084,white + 3px white ring)
  (1160,720,88,"CR",#0b6df0,white) (760,720,96,"DI",#9fd5f5,#1D0084) (540,640,88,"RO",#FFFFFF,#1D0084)
  (420,470,100,"VA",#4da3ff,white) (320,250,72,"IS",#21468C,white) (1600,230,72,"TO",#1D0084,white + ring)
  (1640,780,76,"EL",#FFFFFF,#1D0084) (300,780,76,"GA",#0b6df0,white)
  initials Inter 700, ~0.36× diameter. Thin connector lines rgba(255,255,255,0.22) 2px from each disc to the pill.
- END STATE of frame 23 (minus its chat bubbles and the "en tu idioma." line) == START STATE of frame 24.
""",
    "tiles": """\
SHARED GEOMETRY — sound keycaps (frames 18 and 19 MUST use exactly this):
- Four keycaps 300×300, radius 22px, white, 1px #DDE6F5 border, shadow 0 18px 0 #DDE6F5 + 0 30px 60px rgba(18,0,129,0.16)
  (a physical key), top edge y=430, left edges x = 282 · 652 · 1022 · 1392 (gap 70).
- Letters centered (Poppins 900, 150px, #1D0084): G · UI · UU · EU; example word under the letters inside the key
  (Inter 600 26px, #5A6480): goed · huis · uur · leuk.
- END STATE of frame 18 (minus the six small chips and the waveform) == START STATE of frame 19 (ground paper with dots).
""",
}
GEOMETRY["laptop"] = """\
SHARED GEOMETRY — the laptop (frames 20 and 21 are built by the SAME worker; the last frame of 20 and the
first frame of 21 must be pixel-identical for the lid, the ▶ disc and the cursor — share one CSS/markup block).
Start from: closed lid seen from above, ~1240×800, radius 44, centered ≈ (960, 560), rotated ≈ -24° so it crosses the
frame diagonally (corners may leave frame); graphite shell (linear-gradient 160deg #3b4156 → #262a3c → #171a28),
1.5 px inner highlight rgba(255,255,255,0.12), a darker thickness edge and a deep drop shadow on the blue ground;
a faint diagonal specular streak. ▶ disc 200 px at ≈ (960, 470), unrotated, glassy white (14 % fill, 3 px white 65 %
ring), white triangle. Adjust if needed, but keep 20's end == 21's start.
"""
GEOMETRY["path_v2"] = GEOMETRY["path"].replace("frames 20 and 21 MUST use exactly this", "frame 23 re-uses v1's path world").split("- END STATE")[0] + """\
- START STATE of frame 23: N1 open (#4da3ff + open padlock), N2–N5 locked; no progress overlay yet; pill visible.
"""
GEOMETRY["quiz"] = """\
SHARED DESIGN — generic quiz card + die (frames 30, 31, 33 — same worker; NOT the Nawar platform):
quiz card white, radius 28, ~980×600, card-on-blue shadow; question «¿Qué significa "gezellig"?» Inter 700 40 px ink;
4 option rows (≈ 868×86, radius 18, #F1F4FB fill, 1 px #DDE6F5 border, gap 18) each with a 56 px indigo letter badge
(A/B/C/D white Inter 800) + option text Inter 600 32 px ink: A «aburrido» · B «acogedor» · C «caro» · D «rápido».
Die: white CSS 3D cube ~200 px, radius 26 px faces, indigo pips, soft shadow.
"""
GEOM_FOR = {"23-camino": "path_v2", "33-de-verdad": "quiz"}

def storyboard_blocks():
    s = open(os.path.join(ROOT, "STORYBOARD.md"), encoding="utf-8").read()
    parts = re.split(r"(?m)^## Frame (\d+) — ", s)
    blocks = {}
    for i in range(1, len(parts), 2):
        n = int(parts[i]); body = parts[i + 1]
        body = re.split(r"(?m)^## (?!Frame)", body)[0]
        blocks[n] = "## Frame %d — %s" % (n, body.strip())
    vd = re.search(r"(?ms)^## Video direction\n(.*?)(?=^---\n)", s)
    return blocks, (vd.group(1).strip() if vd else "")

def main():
    os.makedirs(OUT, exist_ok=True)
    timing = json.load(open(os.path.join(ROOT, "timing.json")))
    frames = timing["frames"]
    blocks, video_direction = storyboard_blocks()
    core = open(os.path.join(SKILLS, "hyperframes", "references", "frame-worker-core.md"), encoding="utf-8").read()
    delta = open(os.path.join(ROOT, "tools", "role_delta.md"), encoding="utf-8").read()
    open(os.path.join(OUT, "_role.md"), "w").write(core.rstrip() + "\n\n---\n\n" + delta)
    for k, f in enumerate(frames):
        n = int(f['id'].split('-')[0])
        fid = f["id"]
        prefix = f"f{fid.split('-')[0]}-"
        ws = f["words"]
        cues = "\n".join(f"| {w['t']:.2f} | {min(w['end'], ws[i + 1]['t'] - 0.02) if i + 1 < len(ws) else w['end']:.2f} | {w['text']} |" for i, w in enumerate(ws)) or "| — | — | (no voice: end card) |"
        prev_f = frames[k - 1] if k > 0 else None
        next_f = frames[k + 1] if k + 1 < len(frames) else None
        neigh = []
        if prev_f:
            neigh.append(f"- Previous frame {prev_f['id']} ends at the cut; its last spoken words: \"{' '.join(w['text'] for w in prev_f['words'][-6:])}\".")
        if next_f:
            neigh.append(f"- Next frame {next_f['id']} hard-cuts in at your end ({f['duration']} s); its first words: \"{' '.join(w['text'] for w in next_f['words'][:6]) or 'end card'}\".")
        geom = GEOMETRY[GEOM_FOR[fid]] if fid in GEOM_FOR else ""
        note = f"\nTiming note: {f['note']}\n" if f.get("note") else ""
        packet = f"""# Frame packet — {fid}

- PROJECT_DIR: {ROOT}
- frame_id: {fid}  (composition id + window.__timelines key + file name)
- write: compositions/frames/{fid}.html  and  compositions/frames/{fid}.sfx.json
- CSS-safe id/class prefix: {prefix}
- canvas: 1920×1080 · captions: disabled (kinetic type instead) · safe area x 80–1840, y 70–1000
- duration: {f['duration']} s (root data-duration and the ground clip use exactly this)
- master start: {f['start']} s (for your information only — everything you author is frame-local)
- preview: python3 tools/preview_frame.py {fid}
{note}
## Word cues (frame-relative seconds — reveals land on these)

| start | end | word |
|---|---|---|
{cues}

## Neighbours

{chr(10).join(neigh)}

{geom}
## Your storyboard block

{blocks.get(n, '(missing block)')}

## Video direction (shared by every frame)

{video_direction}

## Assets available

{ASSETS}
## References

{COMPONENTS}
Design truth: frame.md (project root) — palette, type ramp, components. Read it before writing.
"""
        open(os.path.join(OUT, f"{fid}.md"), "w").write(packet)
    print(f"wrote {len(frames)} packets + _role.md to {OUT}")

if __name__ == "__main__":
    main()
