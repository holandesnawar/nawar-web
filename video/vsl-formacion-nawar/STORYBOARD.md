---
format: 1920x1080
duration: 178.0s
message: "El neerlandés no se te da mal: te lo estaban enseñando desde el inglés. Nawar te lo enseña desde el español — y esto es exactamente lo que hay dentro."
arc: Hook → Pain → Reframe → Nawar → 3 phases → Sounds → PAUSE «¿y qué hay dentro?» → DROP: laptop reveal → 16 weeks · 10 modules · +360 lessons → path → short videos → practice → flashcards → consultas → weekly live class (same teachers) → no A/B/C/D tests → outcomes → promise → CTA → end card
audience: hispanohablantes en Países Bajos / Flandes, atascados con el neerlandés
mode: autonomous
music: owner's track re-edited on its bar grid (audio_v4.json, calmer mix): frame 20 opens at 89.38, STOP at 89.68 (= the cursor's click on pause), DROP at 92.54 (start of frame 21), breakdown from 150.14, riser 164.54, tension 166.94, RE-DROP 169.34 (start of frame 38), final hit 176.54 (on «…cuando lo HABLAS»)

# STORYBOARD v4 — Nawar VSL (Formación Nawar A0–A1)

**v4 changes** (owner): voice take (4) of the new script, which drops «sacas adelante a tu familia» and «el colegio
de tus hijos» so nobody feels left out → frame 04 says «tienes tu vida montada», frame 15 «el ayuntamiento y tu día a
día». Frame 21 opens straight onto the website (no Nawar logo on a black screen) and hands over to the course page
(assets/video/formacion-134.mp4). Everything else as v3, retimed to the new take (tools/retime_v4.py).

**v4.1 changes** (owner): 01 — no white text caret at the start (it read as a glitch). 14 — the laptop shows the
«Inicio» dashboard from the very top and scrolls smoothly (two moves) to «Tus cursos · Comunidad · Próximos eventos»;
the page is stitched from inicio-home.mp4 by tools/stitch_page.py (the raw recording scrolled fast to the bottom).
18 — no row of extra sound chips under G · UI · UU · EU. 20 — the film is still playing when 20 opens (❚❚ on the disc
and in the bar); the cursor glides onto the disc and clicks at 0.30 s: the click SFX, the ❚❚ → ▶ swap and the music
stop are one instant. The hook (01–03, up to «…en menos de tres minutos») plays at the take's natural speed
with a little more air (owner: «el inicio va algo rápido»); the end card's tail is shortened so the film stays under 2:58.

All times inside a frame are **frame-relative seconds**. Exact per-word cue times for every frame are
in `timing.json` and are inlined into each frame packet — every reveal must land on its word's cue
(≤ 0.06 s early, never late). Master timeline: frame N starts at `timing.json → frames[N].start`.

v2 keeps frames 01–19 of v1 (same design, retimed to the new voice by `tools/retime_v2.py`; 01–03 are
re-grounded on NAWAR BLUE because the owner found the opening too white, 17 gets its new line). Frames
20–39 are new: the owner asked to stop the film Offlesson-style on «Vale, ¿y qué hay dentro?», reveal
the school with a laptop effect exactly on the music drop, and then show clearly EVERYTHING the
product includes.

## Video direction

**Look.** Same system as v1 (`frame.md`). The owner LOVES how NAWAR BLUE is used from the middle of
the film on — so the whole second half (20–39) is predominantly NAWAR BLUE (radial #025dc7 → #120081,
white dots, soft vignette), with NIGHT (#07041F glow) only for the "martes por la noche" beat (27) and
white cards/devices carrying the real product. Absolutely no orange anywhere. Yellow only inside the
logo image. Paper (#F5F7FF) only inside cards/UI — never as a full ground in 20–39.

**Energy.** Reference = Offlesson-style VSL: something new arrives on almost every spoken phrase; big
key words land exactly on the voice; the real product is shown inside devices; the camera moves with
purpose (push-ins, dives through screens, 3D tilts). Each frame cuts in **hard** on its first word —
the first 0.25 s carries a strong entrance move. No exits (the next frame's entrance is the
transition); only 39 fades out at the very end.

**The music is part of the edit.** Frame 20 starts at the instant the music STOPS dead — total silence
except the voice: the image must feel *paused*. Frame 21 starts exactly on the DROP: the biggest visual
hit of the film. Frames 34–37 sit on the song's breakdown (calmer, emotional, slower moves); 37 rides
the riser/tension (build, push-in, glow) and 38 starts exactly on the RE-DROP (second big hit). The
song's final hit lands at 39 + 3.60 s (right after "…cuando lo hablas.").

**Motion grammar.** power3.out for entrances, power4/expo.out for slams, ≤ 0.35 s per word reveal;
after the last reveal, hold (subtle drift ≤ 2 % scale at most). Overshoot only for logo bloom, check
pops and the CTA button. Within-frame scene changes are velocity-matched seams.

**Type.** 2–6 key words per sentence, big (Poppins 800/900); supporting words as a smaller lead-in
line (Poppins 600–700) or nothing. One accent per moment (chip OR blue-light color OR strike).

**The product is real.** Whenever the narration talks about the school, show actual platform footage
or screenshots inside a laptop/browser/phone (inventory in every packet). Never redraw the platform UI.
Props that are NOT the platform (quiz card, dice, flashcard prop, chat bubbles, toggles) are crafted
SVG/CSS in the house style.

**Negative list.** No orange. No emoji glyphs (no emoji font — draw icons as inline SVG). No brand
logos other than Nawar (no Duolingo, no Offlesson). No invented numbers/prices: the only numbers
allowed on screen are 16 semanas · 10 módulos · +360 lecciones · +30.000 alumnos siguen nuestras clases
en redes · lesson/exercise numbers visible in the real UI. No student names (blur if any appear). No
text below y=1000, nothing important within 60 px of the frame edges. No repeat/yoyo, no CSS
animations, no Math.random.

**Sound.** Each worker writes a sidecar `compositions/frames/<id>.sfx.json` (≤ 4 cues, quiet,
purposeful). The drop/re-drop already hit hard in the music — add at most a whoosh/impact that
*supports* them, never fights them. Frame 20 must stay nearly silent (one soft click on the pause, one
click on the play at the end).


### v3 polish — a top studio, not an AI template

Owner (v3 brief, verbatim): «quitar todo lo que haga parecer este vídeo muy notable hecho con IA o hagan parecer la
formación algo barato y estúpido … que se vea que somos los mejores, detalles mínimos, cosas realistas no tan IAs,
recuerda que me gustó el estilo, solo mini cosas que se podrían mejorar a algo más chulo hecho por profesional».
Reference of the level he wants: the Offlesson VSL (material/objetivo.mp4): restraint, clean type, real people and
the real platform, few effects.

Rules for every frame (new or touched):
- **Restraint.** One accent per beat. NO lens flares, light-ray bursts, sparkle/star particles, confetti, shockwave
  rings, neon/outer glows on text, speed-line "anime" streaks, chromatic/glitch effects, or camera shakes. Soft,
  physically plausible shadows only. A gentle light sweep across glass/devices is OK (once).
- **Real over fake.** Show the real platform inside the realistic MacBook / macOS window from tools/mac_mockup.md
  (content area exactly 16:9, URL `app.holandesnawar.com`). Props that aren't the platform must read as clean product
  UI or physical objects — never clip-art.
- **Type.** Poppins 700/800 for headlines (900 only for big numbers), Inter for UI/labels. Sentence case for
  headlines; ALL CAPS only for short labels. Max 2 type sizes + 1 label size per frame. Generous spacing, 96 px side
  margins, align to a grid. White on blue; #4da3ff as the single accent.
- **Motion.** Smooth and confident: power2/power3.out, expo.out only for one hero move. One move per element per
  beat, no bounce/elastic/back eases, no wiggles, no pop-overshoot on every element, no per-letter gimmicks. Elements
  settle and breathe; camera moves are slow and purposeful.
- **Icons.** Thin, consistent line icons (≈2.5 px stroke at 48 px), never emoji-like or cartoonish.
- **Sound.** ≤ 2 SFX per frame, soft (volume ≤ 0.25): UI clicks/taps and an occasional soft whoosh. Never glitch or
  "error" noises, never sparkle/chime sweeteners except the end card chime.
- **Credibility.** No invented numbers, no student names/faces, correct Dutch (copy verbatim), no fake brands.

---

## Frame 1 — Hook: "si has llegado hasta aquí"

- src: compositions/frames/01-hook.html
- ground: paper
- entrance: first words fade-rise (it is the opening; no cut to sell)
- assets: none (typography + SVG)

Scene 1 (0.0–1.5s): centered lead line builds word by word on cues "Si · has · llegado · hasta · aquí,"
(display-h3, ink). On "aquí" a hand-drawn alert-red arrow (SVG path draw, Caveat-like stroke) swoops in
from the right and points at the viewer (toward camera / down-center) — "sí, es a ti".
Scene 2 (1.55–3.7s): seam: the line flies up and out of frame fast while the next line rises in from
below (velocity-matched). New line builds on cues "llevas · tiempo · queriendo · hablar" (display-h3,
ink, upper third). On "neerlandés" (3.28) **NEERLANDÉS** slams center (display-hero, indigo, scale
1.3→1 + blur 12→0) and a Dutch-flag tricolor bar (nl-red / white with hairline / nl-blue, 3 stacked
strips) wipes in under it left→right. SFX impact-bass-1 @3.28.
Scene 3 (3.8–5.96s): NEERLANDÉS eases up ~140 px and scales to 0.7; beneath it a white card with a
progress bar labelled "Tu neerlandés" fills 0→68 % fast (3.85–4.6) then **stalls**: at "funcionar"
(4.84) it jitters (3 frames x-shake), turns alert-red and an ✕ badge pops at the bar's end; small
caption under the bar "algo no termina de funcionar" appears word-paced from 3.89. SFX error @4.84.

**v2 change:** ground NAWAR BLUE instead of paper (owner: the opening was too white). Same layout and motion; white/light-blue type on blue, cards stay white.

## Frame 2 — "No es que no valgas"

- src: compositions/frames/02-no-valgas.html
- ground: paper
- entrance: hard slam of "NO" at 0.12 (scale 1.6→1, blur→0)

Scene 1 (0.0–0.75s): giant **NO** (display-hero ×1.6, ink) slams dead center on "no," (0.18). SFX impact-bass-2 (quiet).
Scene 2 (0.75–2.66s): NO shrinks to the top third (power3) while a line builds below on cues:
"es que · no valgas · para los idiomas" (display-h2, ink). On "valgas" (1.31) an alert-red strike draws
across "no valgas". On "idiomas" (1.99) "idiomas" gets an indigo word-chip pop. Hold.

**v2 change:** ground NAWAR BLUE instead of paper. Same layout and motion; type recolored for blue.

## Frame 3 — "Te lo explico en menos de tres minutos"

- src: compositions/frames/03-tres-minutos.html
- ground: paper
- entrance: stopwatch ring zooms in from 0.6 with blur (0.0–0.25)

Scene 1 (0.0–1.1s): an indigo stopwatch (SVG: ring + crown + two side buttons) center-left; its ring
track draws; small lead text "Te lo explico" (0.12) at top. Inside the ring: "3:00".
Scene 2 (1.1–2.31s): on "tres minutos" (1.18–1.41) the right side shows "en menos de" (lead) and
**3 MINUTOS** (display-h1, indigo) slams; the ring's progress arc starts sweeping and the center
counts down 3:00 → 2:59 → 2:58 (a tick each 0.5 s, deterministic). SFX click-soft on each tick.

**v2 change:** ground NAWAR BLUE instead of paper. Same layout and motion; the stopwatch keeps its white face.

## Frame 4 — "Llevas años aquí. Trabajas, pagas tus impuestos, tienes tu vida montada."

- src: compositions/frames/04-llevas-anos.html
- ground: paper
- entrance: whip-in from right (x 300→0 with motion-blur streak) of the calendar

Scene 1 (0.0–1.45s): a tear-off calendar block (white card, indigo header strip) center-left flips
its year fast 2019 → 2020 → … → 2026 (flip-clock style, 7 flips between 0.12 and 0.75); right of it
"Llevas **años** aquí." builds on cues (display-h2; "años" indigo).
Scene 2 (1.5–5.3s): seam: calendar + line slide up out; a row of three life cards (card component,
icon-tile style, ~420×300 each) enters left→right on cues — "Trabajas" (1.56, briefcase icon),
"Pagas tus impuestos" (2.36, envelope + document icon), "Sacas adelante a tu familia" (3.50, house
with three figures icon). Each card gets a success ✓ check that draws 0.25 s after it lands. After the
third, the three cards hold — the viewer is doing everything right. SFX click on each ✓.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 5 — "Pero llegas a la caja del supermercado, al médico, a una reunión o a una entrevista…"

- src: compositions/frames/05-situaciones.html
- ground: paper
- entrance: first vignette card slides up from below with blur

Four vignette cards, each = icon illustration (inline SVG) + a Dutch speech bubble from the *other*
person + your reply bubble showing only "…" (three dots that fade in one by one, finite). They enter
on their cues and build a 4-up row (each ~400×560, gap 36):
1. "supermercado" (0.67–1.03): shopping-cart / checkout icon, label "de supermarkt", bubble
   «Wilt u het bonnetje?»
2. "médico" (2.12): stethoscope icon, label "de huisarts", bubble «Wat kan ik voor u doen?»
3. "reunión" (3.06): school/whiteboard icon, label "het oudergesprek", bubble «Hoe gaat het met uw dochter?»
4. "entrevista" (3.75): two chairs + desk icon, label "het sollicitatiegesprek", bubble «Vertel eens iets over uzelf.»
Camera: a gentle lateral conveyor — as each new card lands, the row recenters (x shift) so the newest
is near center; by 4.2 s all four sit centered. Each "…" reply appears ~0.35 s after its card.
SFX pop (quiet) per card.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 6 — "y el neerlandés se te queda atascado. Y el otro cambia al inglés. Otra vez."

- src: compositions/frames/06-atascado.html
- ground: paper
- entrance: chat bubble pops in from left (scale 0.75→1 from its tail corner)

Scene 1 (0.0–2.05s): a large chat-style bubble (you, left, white card) types Dutch character by
character from 0.30: «Ik wil graag een af…» and the caret blinks (finite, 3 blinks). On "atascado"
(1.21) the bubble shakes (deterministic 4-frame x-jitter), its border turns alert-red, and a rubber
stamp **ATASCADO** (display-h2, alert-red outline text, rotated -6°) thumps over it. SFX glitch-3.
Scene 2 (2.05–3.7s): a reply bubble (right side, light grey #E8ECF7, ink text) pops on "cambia"
(2.44): «Oh, let's just speak English!»; on "inglés" (2.91) a small "EN" pill flips in on that bubble.
Scene 3 (3.7–5.06s): "Otra vez." (3.76): the English bubble duplicates 3 times in a fast cascade
(offset +24 px / -2° each, each slightly more transparent) — déjà vu; **OTRA VEZ.** (display-h1, ink)
lands at 4.09 over the stack, bottom-center. Hold still to the end.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 7 — "Y no será por falta de intentos. Una clase a la semana. Un libro pensado para todo el mundo y para nadie."

- src: compositions/frames/07-intentos.html
- ground: paper
- entrance: lead line slides in from left with streak

Scene 1 (0.0–1.85s): small lead "Y no será por falta de" (0.12–0.99, display-h3) then **INTENTOS**
(1.09, display-hero, ink). Under it five tally strokes draw fast (4 vertical + 1 diagonal, alert-red,
SVG stroke draw, 0.06 s stagger) ending at ~1.6.
Scene 2 (1.9–3.25s): seam up. A week strip of 7 rounded day boxes with Spanish initials
**L M X J V S D**; on "clase" (2.11) only **X** fills blue-vivid with a white "1h" chip; the other six
stay grey outlines. Label above "Una clase a la semana." (display-h3).
Scene 3 (3.3–6.05s): seam up. A generic textbook (3D-ish: cover + page edge, ~420×560, tilted
rotationY -18°) slides in: cover title "DUTCH FOR EVERYONE" (English on purpose) with a globe icon.
Lead "pensado para **todo el mundo**" builds 3.69–4.55; on "y para nadie" (4.84–5.12) the book
desaturates to grey (filter grayscale→1, opacity .55) and **y para nadie.** (display-h2, ink) lands.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 8 — "Una app que te enseña los colores, pero no a pedirle un día libre a tu jefe. Una hora de clase y seis días de silencio."

- src: compositions/frames/08-app-silencio.html
- ground: paper
- entrance: phone rises from below (y 500→0, power4)

Scene 1 (0.0–1.75s): a phone (phone component) center-left. Screen = a generic, cartoonish language
app drawn in HTML (NOT Duolingo: no owl, no green brand; use a playful purple/blue UI): a flashcard
showing a colour swatch + word that cycles on "colores" (1.21): «rood — rojo» → «blauw — azul» →
«geel — amarillo» (hard swaps 0.18 s apart), plus a lightning-bolt streak chip "12". Lead text right:
"Una app que te enseña **los colores**" (0.12–1.21).
Scene 2 (1.8–3.9s): to the right of the phone, a chat bubble addressed to "Jefe" (avatar circle "J")
with the Dutch you'd need: «Mag ik vrijdag vrij nemen?» drawn faded/disabled (opacity .35,
dashed border) as the lead builds "pero no a pedirle un día libre a tu jefe" (1.81–3.27); on "jefe"
(3.27) an alert-red ✕ badge pops on the bubble. SFX error (quiet).
Scene 3 (4.0–6.67s): seam (everything slides up/out). A 7-block week timeline (wide, centered):
block 1 fills blue-vivid "1 h de clase" on "hora" (4.42); on "seis días" (5.26–5.52) blocks 2–7 draw as
flat grey, each containing a small audio-waveform line that flattens to a straight line; a muted
speaker icon at the end. **SILENCIO.** (display-h1, ink) lands on 5.92. Hold.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 9 — "Ahora dime: ¿alguna vez alguien te explicó por qué tu ge suena como una jota? ¿O por qué el verbo se te va al final de la frase?"

- src: compositions/frames/09-preguntas.html
- ground: night
- entrance: soft fade from black (0.0–0.2) — the quiet beat

Scene 1 (0.0–0.95s): small white "Ahora dime:" (lead, 0.12–0.34) center with a soft glow.
Scene 2 (1.0–4.4s): it moves up; question line builds small (ui, white-72): "¿alguna vez alguien te
explicó por qué tu…" (1.03–2.76). On "ge" (2.91) a big keycap tile **G** (white, display-hero, 260×260
rounded key on a translucent tile) pops center-left; on "jota" (3.83) a second tile **J** pops to its
right with a "≈" between them and a tiny phonetic label "[x]" under both — "¿por qué suena igual?".
Scene 3 (4.45–6.76s): seam up. Dutch sentence of white word tiles in Spanish order:
[Ik] [wil] [gaan] [morgen] [naar de markt] — on "verbo" (5.05) the [gaan] tile turns blue-light;
on "se te va al final" (5.31–5.73) [gaan] lifts, arcs over and drops at the END while the others close
the gap (FLIP-style), giving «Ik wil morgen naar de markt gaan.»; on "frase" (6.17) the period pops
and a small gloss appears under: "Mañana quiero ir al mercado." SFX whoosh-short on the arc.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 10 — "Casi ninguna escuela piensa en ti. Te enseñan el idioma como si vinieras del inglés, y luego te dejan solo con tus errores."

- src: compositions/frames/10-escuelas.html
- ground: paper
- entrance: grid cards cascade in from top (stagger 0.04)

Scene 1 (0.0–2.1s): 12 small generic course cards (4×3 grid, white, each with a thumbnail block +
English title: "Dutch for Beginners", "Learn Dutch Fast", "Dutch A1", "Dutch Grammar 101", "Speak
Dutch Today", "Dutch for Expats", … ) cascade in 0.12–0.78. On "piensa en ti" (1.21–1.59) every card
gets a small "EN" badge and desaturates; text "Casi ninguna escuela piensa en **ti**." (display-h3)
over a white band.
Scene 2 (2.15–4.45s): seam. Route diagram: three nodes in a triangle — ESPAÑOL (left), INGLÉS (top
center), NEERLANDÉS (right). On "enseñan" (2.29) the path draws ES → EN (alert-red), on "inglés"
(3.81) it continues EN → NL; the INGLÉS node pulses once (scale 1→1.12→1, not looped) — the detour.
Scene 3 (4.5–6.61s): seam. Center: a Dutch sentence card «Ik gisteren heb gewerk.» with red squiggly
underlines drawing under two words (4.6, 4.9); a small lone person icon beside it; on "solo" (5.34)
the rest dims to 30 %; on "errores" (6.05) three alert-red ✕ marks pop around the card. Hold — lonely.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 11 — THE TURN: "Nawar nace para cambiar eso."

- src: compositions/frames/11-nawar-nace.html
- ground: paper → nawar-blue
- entrance: iris — a nawar-blue circle grows from center (clip-path circle 0 → 150 %) 0.0–0.35, white flash ring at its edge

Scene 1 (0.0–0.5s): iris floods the frame with nawar-blue; on "Nawar" (0.12) the logo
(assets/img/logo-nawar.png, ~820 px wide) blooms center (scale 0.55→1.04→1, blur 16→0) with a soft
blue-light glow behind it; a light-sweep band crosses the logo once (0.35–0.9). SFX impact-bass-1 @0.12.
Scene 2 (0.5–1.95s): logo eases up 90 px; white lead line below builds on cues "nace · para ·
**cambiar** · eso." (lead, white; "cambiar" blue-light). Hold.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 12 — "Un método construido desde el español, con profesores nativos que saben exactamente dónde vas a tropezar."

- src: compositions/frames/12-metodo.html
- ground: nawar-blue
- entrance: nodes pop from center with streaks

Scene 1 (0.0–2.25s): callback to frame 10's diagram, now on blue: ESPAÑOL (left) and NEERLANDÉS
(right) nodes; on "construido desde el español" (0.70–1.71) a bright white straight line draws ES →
NL (left→right, light trail); the INGLÉS node appears above, off the path, greyed, and gets a ✕ on
"español" (1.71). Small label under the line: "sin pasar por el inglés".
Scene 2 (2.3–4.7s): seam left. Left 55 %: a laptop (laptop component, rotationY ~12°) playing
assets/video/clases-video-dentro.mp4 from media-start 0.0 (the live video lesson with the native
teacher). Right: on "profesores" (2.58) pill «Profesores nativos holandeses» pops; on "saben" (3.61)
second pill «Expertos en español» pops. The laptop pushes in slightly toward the teacher's webcam
tile (top-left of the slide) between 2.6–4.2.
Scene 3 (4.75–6.04s): right side swaps (seam up) to a Dutch sentence card «Ik heb gisteren gewerkt.»
with a crosshair reticle that slides across and LOCKS on "heb … gewerkt" on "tropezar" (5.27) — the
reticle snaps (scale 1.4→1) and a bracket connects "heb" and "gewerkt". SFX ping @5.27.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 13 — "Tres fases. Supervivencia."

- src: compositions/frames/13-tres-fases.html
- ground: nawar-blue
- entrance: three pills slam in left→right (0.12, 0.22, 0.32) with motion-blur streaks

Scene 1 (0.0–1.0s): **3 FASES** small label on top; three big pills in a row: "01 Supervivencia",
"02 Vocabulario real", "03 Estructura y soltura" (pill component, lead size).
Scene 2 (1.0–2.14s): on "Supervivencia" (1.05) pill 01 fills white (indigo text), pills 02/03 dim to
35 %, and the camera pushes in toward pill 01 (scale 1→1.25 centered on it, 1.05–2.1) — a hand-off
into frame 14. SFX whoosh-short @1.05.

**v2 voice:** «Son tres fases. Primero, supervivencia.» — design unchanged (retimed).

## Frame 14 — "Presentarte, entender números y horarios, pedir una cita, hacer la compra, preguntar cuando no entiendes. Lo que te hace falta mañana mismo."

- src: compositions/frames/14-supervivencia.html
- ground: nawar-blue
- entrance: laptop slides in from left with streak; pill "01 · Supervivencia" small top-left

Left ~52 %: laptop (tilt rotationY 10°) playing assets/video/inicio-home.mp4 from media-start 4.0
(the weekly "Hoja de ruta" with real survival tasks), slow push-in over the frame.
Right: a checklist card (white, 5 rows). Rows reveal on cues and their ✓ draws 0.2 s later:
"Presentarte" (0.12) · "Números y horarios" (0.99) · "Pedir una cita" (2.46) · "Hacer la compra"
(3.39) · "Preguntar cuando no entiendes" (4.43). SFX click per ✓.
Callout (2.6–3.9s): on "pedir una cita" a Dutch subtitle bubble pops over the laptop's lower area:
«Ik wil graag een afspraak maken.» + gloss "Quiero pedir una cita." then it settles smaller.
Scene 3 (5.95–8.03s): the checklist slides up/out; **MAÑANA MISMO** (display-h1, white; "MAÑANA"
with a white word-chip, indigo text) lands on "mañana" (6.88) with small lead "Lo que te hace falta"
(6.00–6.55). Hold.

**v2:** unchanged design, retimed to the v2 voice.

**v4:** third card = «Tienes tu vida / **montada**»: the same house, without the three figures —
the door rises on «vida», the two windows light up (blue) on «montada». No family, no children.

## Frame 15 — "Vocabulario real. El del trabajo, el médico, el ayuntamiento y tu día a día. Nada de la manzana es roja."

- src: compositions/frames/15-vocabulario.html
- ground: paper (contrast beat)
- entrance: hard slam of the title (scale 1.3→1, blur)

Scene 1 (0.0–1.45s): pill "02" + **Vocabulario real.** (display-h1, indigo) center-top on 0.12/0.74.
Scene 2 (1.5–5.0s): four icon-tiles in a row (≈340×380 each) pop on cues, each = SVG icon + Dutch
word (display-h3, indigo) + Spanish gloss (ui-small, muted):
"het werk / el trabajo" (1.76, briefcase) · "de huisarts / el médico" (2.52, stethoscope) ·
"de school / el colegio" (3.21, school building) · "de gemeente / el ayuntamiento" (4.40, town hall
with columns). SFX pop per tile.
Scene 3 (5.1–7.21s): the tiles shrink and slide up; a card «De appel is rood.» with a red apple icon
and gloss "La manzana es roja." pops center (5.21); on "roja" (6.48) an alert-red strike draws across
it and the card tips (rotate 8°) and drops away 200 px with fade — "nada de esto". SFX whoosh-short.

**v2 voice:** «Luego, vocabulario real. …» — design unchanged (retimed).

**v4:** tiles = het werk · de huisarts · **de gemeente / el ayuntamiento** (on «ayuntamiento») · **de routine / tu día a día** (on «día», a mug with steam and a
small blue heart). The school tile is gone.

## Frame 16 — "Estructura y soltura. Ahora sí, la gramática: dónde va el verbo, las frases invertidas, cómo hablar del pasado."

- src: compositions/frames/16-estructura.html
- ground: nawar-blue
- entrance: title zooms in from blur

Scene 1 (0.0–1.7s): pill "03" + **Estructura y soltura.** (display-h1, white) on 0.12–0.78.
Scene 2 (1.75–3.35s): seam up. "Ahora sí," (lead, white-72) + **GRAMÁTICA** (display-hero, white with
blue-light underline bar) on 2.52.
Scene 3 (3.4–6.99s): seam up. Word tiles (white, indigo text, ~display-h3): [Ik] [ga] [morgen]
[naar Amsterdam] appear on "dónde va el verbo" (3.42–3.87) with [ga] tinted blue-light; on
"invertidas" (4.83) the sentence re-orders with FLIP motion into [Morgen] [ga] [ik] [naar Amsterdam]
(tiles arc to new slots; [Morgen] capitalises) — gloss under: "Mañana voy a Ámsterdam."; on "pasado"
(6.17) a second line slides in: [Ik] [heb] [gisteren] [gewerkt] with [heb] and [gewerkt] blue-light and
a bracket connecting them; gloss "Ayer trabajé." SFX click on each tile landing (max 3).

**v2 voice:** «Y después, estructura y soltura. …» — design unchanged (retimed).

## Frame 17 — "Todo con un objetivo: que dejes de traducir en tu cabeza."

- src: compositions/frames/17-traducir.html — the v1 design is back (target + dart on «OBJETIVO», then the head
  with the ES⇄NL loop and «que dejes de TRADUCIR en tu cabeza»), retimed v1 → v3 by tools/retime_v2.py.

## Frame 18 — "Y desde el primer día, los sonidos que el español no tiene: la ge, la ui, la uu, la eu…"

- src: compositions/frames/18-sonidos.html
- ground: paper (contrast beat)
- entrance: waveform line draws in from left
- note: tile cues were hand-corrected — G 3.45 · UI 4.00 · UU 4.80 · EU 6.00

Scene 1 (0.0–3.3s): pill "DESDE EL DÍA 1" pops on "primer día" (0.56–0.83); a horizontal audio
waveform (indigo bars, ~60 bars, deterministic heights) draws left→right across the middle while
"los sonidos que **el español no tiene**" builds (1.18–2.40, display-h3).
Scene 2 (3.35–6.88s): the waveform slides down/away; four big keycap tiles (≈300×300, white, radius
key, indigo letters display-hero-ish, a thin example word under each) press in one by one on their
cues — **G** "goed" (3.45) · **UI** "huis" (4.00) · **UU** "uur" (4.80) · **EU** "leuk" (6.00). Each
tile lands with a key-press (y 18→0, shadow compress) and a blue-vivid glow ring. SFX key-press each.
Final layout (handoff_out to 19): tiles centered in one row at y=430 (top edge), x left edges at
282, 652, 1022, 1392 (300×300, gap 70). At 6.3 s, six smaller dim chips fade in under the row:
"G/CH · NG-NK · SCH-ISCH · A-AA · E-EE · O-OO" (ui, muted).

**v2:** unchanged design, retimed to the v2 voice.

## Frame 19 — "Son los que te delatan, y los entrenamos uno a uno"

- src: compositions/frames/19-delatan.html
- ground: paper
- handoff_in: the four keycap tiles G/UI/UU/EU exactly as frame 18 ended (row at y=430, x 282/652/1022/1392, 300×300, opacity 1, still); the six small chips are NOT carried over.

Scene 1 (0.0–1.15s): on "delatan" (0.70) all four tiles flash an alert-red outline and a red radar
ring pulses once out of each (finite) — "te delatan"; small label above "te delatan" (display-h3, alert).
Scene 2 (1.2–2.87s): the red outlines clear; on "entrenamos uno a uno" (1.47–2.43) each tile gets a
success ✓ badge popping in sequence (1.5, 1.85, 2.2, 2.45) and turns indigo-filled with white letters.
SFX click per ✓.

**v2:** unchanged design, retimed to the v2 voice.

## Frame 20 — PAUSE: "Vale, ¿y qué hay dentro? Te lo enseño."

- src: compositions/frames/20-pausa.html (+ 21 from the same generator: tools/gen_laptop_20_21.py — update it)
- ground: nawar-blue, darker (vignette) — the film is PAUSED; the music STOPPED at t=0
- device: the REALISTIC MacBook (tools/mac_mockup.md look), CLOSED, seen from above: silver aluminium lid (no logo,
  no text), soft studio reflection, real shadow on the ground — lying diagonally across the frame like the
  Offlesson reference (material/v2/f/efecto*.jpg), a glassy ▶ disc on the lid.
- Same choreography as v2 (pause glyph flash + player bar «1:28 / 2:57», «Vale,» · «¿Y qué hay» · «dentro?» · «Te lo
  enseño.», cursor glides in and clicks ▶ just before the end, lid lifts a few degrees on the last frames) — but
  «dentro?» WITHOUT neon glow (solid blue-light, Poppins 800), and the text is the new line «Te lo enseño.».

## Frame 21 — THE DROP: the Mac opens on the school · "Dieciséis semanas de formación guiada."

- src: compositions/frames/21-portatil.html (same generator as 20)
- music: the DROP lands at t=0 (calmer mix than v2). Voice comes back at 2.91 s (v4).
- 0.0–1.0 s: the lid swings open toward the camera while the camera settles STRAIGHT ON — ending exactly in the
  front-view MacBook of tools/mac_mockup.md (screen + thin base lip). The keyboard must never be seen (the owner
  explicitly asked: «sin que se le vean las teclas, simplemente de frente»): e.g. keep the camera at deck height so
  the deck is hidden behind the front lip, or let the lid hinge up past the camera axis while the body is already
  front-on. No white flash (a soft light lift is enough), no shock rings.
- v4 (owner): NO boot screen. As the lid opens the macOS browser already shows the website hero
  (assets/video/nuestra-vision-hero.mp4 — the school building with the Nawar sign, `holandesnawar.com`); on the bar
  line 2.4 s it navigates to the course page (assets/video/formacion-134.mp4: «Formación Nawar A0–A1» and the lesson
  list scrolling, `app.holandesnawar.com`). At most a very slow push (≤ 3 %) — no zoom inside the screen.
- From «Dieciséis» (2.91): the Mac glides to the left (still front-on, no 3D tilt); right column: «16» (Poppins 900),
  «semanas» (Poppins 800), «de formación guiada» (Poppins 600, white-72, «guiada» in #4da3ff), and the row of 16
  week pills filling left → right between «semanas» and «guiada».

## Frame 22 — "Diez módulos, con más de trescientas sesenta lecciones."

- src: compositions/frames/22-modulos.html
- ground: nawar-blue
- entrance: zoom-through — we arrive as if we dove into the laptop screen: the whole module grid
  rushes in from scale 1.6 + blur 14 px → 1 + blur 0 in 0.35 s (expo.out).

Scene 1 (0.0–1.0s): **10** (Poppins 900 ~240 px, white) counts 0 → 10 landing on "Diez" (0.12–0.5)
with **MÓDULOS** (display-h2, blue-light) beside it on "módulos,". Behind/below: a 5 × 2 grid of ten
module cards (white cards, radius 22, ~300 × 150, gap 26) slam in a fast stagger (0.04 s) on
"módulos": each card shows "MÓDULO 1…10" (label, muted) and the REAL Dutch module name (Poppins 700
30 px, indigo): 1 «Over jou» · 2 «Familie & vrienden» · 3 «Eten en drinken» · 4 «Het werk» ·
5 «Hobby's & vrije tijd» · 6 «Thuis & wonen» · 7 «Gezondheid» · 8 «Vervoer & reizen». Cards 9 and
10 show "MÓDULO 9" / "MÓDULO 10" with their name area blurred/greyed and a small padlock (future
modules — we must not invent their titles). Cards 1 has a ✓ (success), cards 2–10 a tiny lock.
Scene 2 (1.0–3.16s): **+360** (Poppins 900 ~240 px, white) counts 0 → 360 between "trescientas"
(1.40) and "lecciones." (2.42), landing exactly on 360 at 2.42 with **LECCIONES** (display-h2,
blue-light). As it counts, each module card fills with a row of tiny lesson dots (deterministic, ~36
per card, white→blue-light) — the 360 lessons visibly inside the 10 modules. Hold.
Layout suggestion: counters on the top band (y 120–380), grid below (y 440–900).
SFX: whoosh-short @0.0 (0.3) · pop @0.12 (0.3) · typing @1.4 (0.18) · ping @2.42 (0.3).

## Frame 23 — "Cada módulo se desbloquea cuando terminas el anterior, así que avanzas a tu ritmo, pero con tus compañeros en el mismo camino."

- src: compositions/frames/23-camino.html
- ground: nawar-blue
- entrance: the path draws in from the left with a fast camera slide (x +240 → 0, 0.3 s, motion-blur streaks)
- REUSE: v1 already built this world — read compositions/frames_v1/20-por-dentro.html (scene 2: road
  path, nodes, padlocks) and compositions/frames_v1/21-tu-ritmo.html ("TÚ" avatar + companions) and
  re-use their geometry, SVG and look (shared geometry "path" is in your packet). Re-time everything
  to THIS voice.

Scene 1 (0.0–2.5s): path with 5 nodes (1 «Over jou» … 5 «Hobby's & vrije tijd»), node 1 open, 2–5
locked. Top-left lead "Cada módulo" (lead, white) on "Cada · módulo"; **SE DESBLOQUEA** (display-h2,
white; padlock icon inline) on "desbloquea" while lock 1→2 visual: node 1 gets its ✓ on "terminas",
lock 2 opens (shackle lifts, turns blue-light) on "anterior," and the progress overlay draws to node 2.
Scene 2 (2.5–4.2s): the white "TÚ" avatar disc drops onto node 2 and travels along the road toward
node 3 on "avanzas a tu ritmo" (3.15–3.83), arriving on "ritmo,"; heading swaps (kinetic-type-swap)
to **A TU RITMO** on "ritmo,".
Scene 3 (4.2–6.46s): on "compañeros" six companion discs (initials MA, JL, SO, PE, LU, AN — same fills
as v1 21) pop onto the road around "TÚ" in a stagger, some ahead, some behind, all advancing a bit;
heading swaps to **CON TUS COMPAÑEROS** ("compañeros" blue-light) and "en el mismo camino." (lead,
white-72) lands under it on "mismo · camino.". Hold.
SFX: click @0.79 (0.3) · pop @3.15 (0.25) · pop @4.74 (0.3).

## Frame 24 — "Microlearning. Vídeos cortos que te explican cada tema. Y después, práctica de verdad."

- src: compositions/frames/24-videos.html
- device: a macOS window (tools/mac_mockup.md `.fNN-win`, 16:9, `app.holandesnawar.com`) — right ~60 % of the frame,
  front-on (no 3D tilt).
- Inside: assets/video/paul-clase-2.mp4 — a REAL module video with teacher Paul (small webcam top-left of the slide
  «De structuur», player bar with time) — the same teacher the viewer will see again in the live class (28/29).
- Left column: label pill «Microlearning» on «Microlearning», headline «Vídeos cortos» on «Vídeos · cortos», line «que
  te explican cada tema» on its words.
- «Y después, práctica de verdad.»: the window content cuts (a clean horizontal slide inside the window, not a 3D
  flip) to the real reading exercise (assets/img/ui-lezen-texto.png); the left text swaps to «Y después,» /
  «práctica de verdad.» («de verdad» in #4da3ff). Hold.

## Frame 25 — "Lectura, escritura y escucha activa."

- src: compositions/frames/25-practica.html — 2.33 s, three quick beats.
- Three macOS windows (`.fNN-win`, 16:9, ~560 px wide) arranged in a slight overlapping cascade or a clean row,
  each with a REAL exercise and a label under/over it: «Lectura» (ui-lezen-texto.png) on «Lectura», «Escritura»
  (completa-frase.mp4 from 6.85 — the student types «alstublieft») on «escritura», «Escucha activa»
  (ui-luisteren-audio.png with a moving playhead) on «escucha · activa». Smooth slides, no motion-blur streaks.

## Frame 26 — "Flashcards incluidas, para que el vocabulario se quede y no se te escape a la semana."

- src: compositions/frames/26-flashcards.html
- Left: the front-view MacBook (mac_mockup.md) playing the REAL flashcards tool assets/video/flashcards.mp4 (from
  ≈0.8 so the card flips «el bocadillo» → «het broodje» on «Flashcards»).
- Right column: «Flashcards» (headline) + «incluidas» (pill or second line) on their words; «para que el vocabulario
  se quede» (line) with a clean stack of 3 real word cards (het broodje · de vis · komen) settling into place on
  «quede»; «y no se te escape a la semana.» → a minimal week strip L M X J V S D whose days tick in #4da3ff. No
  strings/pins/escaping-card gimmicks.

## Frame 27 — "Consultas dentro de la escuela. ¿Te atascas y necesitas ayuda? Preguntas, y te responden. Tus dudas no se quedan esperando, y se quedan guardadas para todos."

- src: compositions/frames/27-consultas.html — 9.13 s, nawar-blue (the v2 night/23:14 idea is DROPPED: the owner
  said consultas don't work like that).
- 0 → «¿Te atascas…»: headline «Consultas dentro de la escuela» (on «Consultas … escuela»); the front-view MacBook
  rises with the REAL «Nueva consulta» form (assets/video/consulta-nueva.mp4 from ≈3.5: category «Gramática»,
  typing «cómo se traduce gezellig?»). «¿Te atascas y necesitas ayuda?» as a supporting line.
- «Preguntas, y te responden.»: the REAL answered consulta (assets/img/ui-consulta-respondida.png, crop the modal
  ≈ x 560–1510, y 250–700; the student's name is already blurred) slides in front with a «Respondida» status pill.
- «Tus dudas no se quedan esperando,»: a clean status change «Pendiente» → «Respondida» (no hourglass gimmick).
- «y se quedan guardadas para todos.»: the answered consulta files itself into a shared library — a tidy list of 4–5
  answered consultas in the platform's own card style (titles only, e.g. «¿Cuándo se usa "er"?», «hij werkt / werk
  jij», «¿De of het?», «¿Cómo se traduce "gezellig"?», each with a topic chip and a «Respondida» tag, NO names or
  avatars), with a small «Visible para todos los alumnos» label. Hold.

## Frame 28 — "Y una clase en directo cada semana, con los mismos profesores que te explican en los módulos."

- src: compositions/frames/28-directo.html — 4.54 s.
- «Y una clase en directo cada semana»: the real «Eventos» calendar (assets/img/ui-eventos-calendario.png) in a macOS
  window; the weekly «Clase en directo» entries get a soft highlight one after another (weekly rhythm); «● En directo»
  pill (red dot) on «directo».
- «con los mismos profesores que te explican en los módulos.»: cut to the live class: a macOS window / call layout
  with teacher Paul big (assets/video/paul-clase-1.mp4, crop to his camera — left part of the slide, ≈ x 740–1330 of
  2502, full height) with «● En directo»; on «módulos» a smaller window with the module video
  (assets/video/paul-clase-2.mp4 — Paul's webcam on «De structuur») slides in beside it: the same teacher in both.

## Frame 29 — "La cara que te enseña en el vídeo es la que te corrige en directo. Te conocen y saben dónde estás. Además, queda grabada por si no pudiste asistir."

- src: compositions/frames/29-mismo-profe.html — 7.78 s.
- Two windows side by side: LEFT «En el vídeo del módulo» (paul-clase-2.mp4, the player with Paul's webcam),
  RIGHT «En directo» (paul-clase-1.mp4 cropped to Paul, live-call chrome: mic/cam controls, red «● En directo»).
  Two different videos, same face — that's the point. On «cara» a thin face-frame (four corner marks) on the left
  Paul; on «es la que» the same frame appears on the right Paul (a clean match line between them, no glow).
- «te corrige en directo»: a correction chip by the live window: «Werkt jij?» (struck in red) → «Werk jij?» ✓.
- «Te conocen y saben dónde estás.»: a small progress card «Tu progreso · Módulo 3 · Eten en drinken» with a
  location marker «Estás aquí».
- «Además, queda grabada por si no pudiste asistir.»: the live window gets a «● Grabando» tag, then it slides into a
  «Grabaciones» list as a recording card «Clase en directo · martes» with a ▶ and duration bar. Hold.

## Frame 32 — "Y no menos importante, los ejercicios. Aquí escribes, ordenas frases, escuchas y respondes, completas sin pistas."

- src: compositions/frames/32-practicas.html — 7.28 s. Same idea as v2 (verb list + one device whose real content
  swaps per verb) but: the lead line is «Y no menos importante, los ejercicios.» (no Nawar logo header); the
  device is the macOS window (`.fNN-win`, 16:9, `app.holandesnawar.com`), front-on; verbs «Escribes» · «Ordenas
  frases» · «Escuchas y respondes» · «Completas sin pistas» each land on its word with a clean check; contents as v2
  (completa-frase typing, «Ordena las palabras» with the chips flying into «Ik wil een glas water, alsjeblieft.»,
  luisteren with playhead, completa-frase «¡Correcto!» on «pistas»). Read compositions/frames/32-practicas.html (v2)
  and keep what works.

## Frame 33 — "No puedes jugar al azar. O lo sabes, o lo practicas hasta saberlo. Y cuando avanzas, sabes que es de verdad."

- src: compositions/frames/33-de-verdad.html
- ground: nawar-blue
- entrance: the 3D die from frame 31 rolls in (rotation + x 600 → 0, 0.3 s)

Scene 1 (0.0–1.6s): "No puedes jugar" (lead, white) → **AL AZAR.** (display-h1) on "azar."; on
"azar." the die gets an alert-red ✕ stamp over it and shatters into 6 shards that fall away
(deterministic) — no luck here.
Scene 2 (1.6–4.1s): split in two halves: LEFT "O lo" → **SABES** (display-h1, white, a success ✓
circle pops) on "sabes,"; RIGHT "o lo" → **PRACTICAS** (display-h1, blue-light, a circular repeat
arrow icon spins one turn) on "practicas" + "hasta saberlo." (lead, white-72) on "saberlo.".
Scene 3 (4.1–6.78s): the halves slide away; a big solid progress bar (white track 18 %, fill
success-on-dark #34D399 → blue-light gradient, 1200 × 34, radius 999) fills from 0 to ~70 % on
"cuando avanzas," with module markers (1 · 2 · 3) ticking as it passes them; **DE VERDAD.**
(display-h1, white, in a white-outline stamp frame rotated -4°) stamps on "de · verdad." with a
3-frame shake. Hold.
SFX: glitch-2 @1.10 (0.2) · pop @1.94 (0.25) · whoosh-short @4.25 (0.25) · impact-bass-2 @6.05 (0.25).

## Frame 34 — "Al terminar, te presentas, pides una cita, entiendes lo que te dicen en el médico y respondes en neerlandés."

- src: compositions/frames/34-al-terminar.html
- ground: nawar-blue (the music drops to its breakdown 0.3 s into this frame: calmer, warmer — slower
  eases, softer moves, more air)
- entrance: a label pill "AL TERMINAR" (white pill, indigo text) + a finish-flag icon rise in (0.35 s, power3.out)

A vertical chat thread (centered-right, ~900 px wide) that builds message by message — YOU (blue-vivid
bubbles, white text, right) and THEM (white bubbles, ink text, left, with small icon avatars: a shop
assistant, a receptionist, a doctor with a stethoscope icon). Left column: the Spanish verbs land in
sync, each followed by a success ✓ (success-on-dark):
1. "te presentas," → YOU: «Hallo, ik ben Ana. Ik woon hier sinds twee jaar.» → left verb **te presentas** ✓
2. "pides una cita," → YOU: «Ik wil graag een afspraak maken.» (THEM: «Dinsdag om tien uur?») → **pides una cita** ✓
3. "entiendes … médico" → THEM (doctor): «Waar heeft u last van?» with a tiny Spanish gloss under it
   in white-72 («¿Qué le pasa?») → **entiendes al médico** ✓
4. "respondes en neerlandés." → YOU: «Ik heb al drie dagen hoofdpijn.» → **respondes en neerlandés.** ✓
   ("neerlandés" blue-light).
The thread scrolls up gently as new messages arrive (waterfall). Bubbles use chat-message mechanics
(arrive from their sender's side). Hold the full thread at the end.
SFX: pop @1.02 (0.2) · pop @2.27 (0.2) · pop @4.18 (0.2) · chime @5.53 (0.25).

## Frame 35 — "Y cuando el otro vaya a cambiar al inglés, no le va a hacer falta."

- src: compositions/frames/35-sin-ingles.html
- ground: nawar-blue (breakdown — keep it light and witty)
- entrance: a big NL ⇄ EN toggle switch slides up into the center (0.3 s)
- callback: in v1 frame 06 the other person switched to English («Oh, let's just speak English!»)
  and an "EN" chip appeared. Look at compositions/frames_v1/06-atascado.html for that look.

Scene 1 (0.0–2.1s): a large pill toggle (white track 520 × 160, knob 140 px) with "NL" (left, indigo,
Dutch flag stripes on the knob) and "EN" (right, muted). A THEM bubble starts «Oh, shall we speak
Eng—» on "cambiar al inglés" and the knob starts sliding toward EN on "cambiar"… it gets halfway
(1.46) and stalls.
Scene 2 (2.1–3.44s): on "no le va a hacer falta." the knob snaps back to NL with a satisfying
overshoot, a small padlock locks it on "falta.", the THEM bubble's text gets deleted backwards and
replaced by «Oké, gewoon in het Nederlands!» with a smile icon (svg); **NO LE VA A HACER FALTA.**
(display-h2, white; "FALTA" blue-light) builds on "no · hacer · falta.". Hold.
SFX: click @1.04 (0.25) · click @2.30 (0.3) · pop @2.83 (0.25).

## Frame 36 — "No prometemos milagros. Prometemos claridad, cercanía y un método pensado para ti."

- src: compositions/frames/36-promesa.html
- ground: nawar-blue (breakdown → the riser starts at 4.89 s: from there everything slowly brightens
  and pushes in)
- entrance: "No prometemos" lead-in rises from blur (0.3 s)

Scene 1 (0.0–1.6s): "No prometemos" (lead, white) → **MILAGROS** (display-h1, white, with a few
sparkle glyphs svg around it) on "milagros." and an alert-red strike draws across it right after
(0.12 s later), the sparkles fall/fade.
Scene 2 (1.6–5.6s): "Prometemos" (lead) on its cue; then three promise rows stack (display-h2, white,
each with a round white icon badge, blue-vivid line icons): **CLARIDAD** (icon: eye/lens) on
"claridad," · **CERCANÍA** (icon: two speech bubbles / handshake) on "cercanía" · **UN MÉTODO PENSADO
PARA TI** ("PARA TI" in a white word-chip with indigo text; icon: compass/target) building on "método
· pensado · para · ti.". From 4.9 s (riser) a slow push-in (scale 1 → 1.06) and a light glow rising
behind the rows.
SFX: whoosh-short @0.9 (0.2) · pop @2.23 (0.2) · pop @2.99 (0.2) · pop @4.07 (0.2).

## Frame 37 — "El algún día ya lo has probado. Ahora toca hablar."

- src: compositions/frames/37-ahora.html
- ground: nawar-blue → building to the RE-DROP at the end of this frame (the music's tension bar starts
  at 1.69 s: bass gone, high riser — the image must build tension: slow push-in, glow growing,
  everything held in suspense)
- entrance: a calendar page / sticky note drops in (0.3 s)

Scene 1 (0.0–1.4s): a white sticky note (slightly rotated, paper texture via subtle gradient) with
"algún día…" handwritten (Caveat 700 88 px, ink) — "El" (lead) on "El", the note on "algún · día";
on "probado." the note crumples (scaleX/Y squish + rotate + svg crease lines) and is tossed away
off-frame down-left.
Scene 2 (1.4–4.09s): **AHORA** (Poppins 900 ~260 px, white) slams center on "Ahora" (1.43) — then
held in tension: a slow push-in (scale 1 → 1.12 over 2.6 s, power1.in), a blue-light glow behind
growing, fine speed lines converging toward the center faster and faster; "toca" (lead, white-72) on
"toca" (2.60) under it; **HABLAR.** (display-h1, blue-light) on "hablar." (3.13) with a microphone icon
and a few voice bars. The last 0.25 s: everything accelerates toward the camera (scale ramps 1.12 →
1.4, blur up) — we are sucked into the RE-DROP that opens frame 38.
SFX: whoosh-short @0.83 (0.25) · riser @1.5 (0.35) · whoosh-cinematic @3.85 (0.3).

## Frame 38 — CTA (RE-DROP): "Completa tu matrícula en el siguiente paso y contactamos contigo. Sin compromiso."

- src: compositions/frames/38-cta.html — 4.27 s, starts exactly on the re-drop.
- Keep v2's idea (big «Completa tu matrícula →» button, cursor click on «siguiente paso», morph into the «Te
  contactamos» card with the team logo, «Sin compromiso.» stamp at the end) but: REMOVE the three «Tu nivel / Tu
  situación / ¿Encaja contigo?» chips (no longer in the voice), REMOVE the spark streaks/shock rings/rays; the drop
  is carried by a clean, confident button entrance. «Sin compromiso.» on «Sin · compromiso.» as a clean outlined
  label (no shake). NO PRICE.

## Frame 39 — End card: "Formación Nawar. Tu neerlandés empieza cuando lo hablas."

- src: compositions/frames/39-end-card.html
- ground: nawar-blue
- entrance: logo bloom (scale 0.6 → 1, blur → 0) + light sweep
- REUSE: v1 end card compositions/frames_v1/25-end-card.html — same look and layout; re-time it to
  the voice; the music's FINAL HIT lands at 3.60 s.

Scene 1 (0.0–1.4s): logo-nawar.png blooms center-upper (~760 px wide) on "Formación" (0.12) with the
glow behind; "FORMACIÓN NAWAR · A0 → A1" (label, white-72) under the logo on "Nawar." (0.74).
Scene 2 (1.4–3.6s): the claim builds word by word under it ON THE VOICE: "Tu neerlandés empieza
**cuando lo hablas.**" (display-h2, white; "cuando lo hablas" blue-light) — Tu 1.54 · neerlandés 1.65 ·
empieza 2.16 · cuando 2.64 · lo 2.99 · hablas 3.10.
Scene 3 (3.6–7.2s): ON THE FINAL HIT (3.60): a light sweep crosses the logo + a soft white pulse ring
from the logo; the pill "holandesnawar.com" (white fill, indigo text) rises at 3.7; a small line
"+30.000 alumnos siguen nuestras clases en redes" (ui-small, white-72, with a small people icon) at
4.0. Hold; from 6.3 everything fades to night (#07041F) by 7.2 — the only exit in the film.
SFX: chime @0.12 (0.3) · sparkle @3.60 (0.25).
