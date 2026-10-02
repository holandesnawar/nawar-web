---
format: 1920x1080
duration: 202.9s
message: "El neerlandés no se te da mal: te lo estaban enseñando desde el inglés. Nawar te lo enseña desde el español — y esto es exactamente lo que hay dentro."
arc: Hook → Pain → Reframe → Nawar → 3 phases → Sounds → PAUSE «¿y qué hay dentro?» → DROP: laptop reveal → 16 weeks · 10 modules · +360 lessons → path → short videos → practice → flashcards → consultas → weekly live class (same teachers) → no A/B/C/D tests → outcomes → promise → CTA → end card
audience: hispanohablantes en Países Bajos / Flandes, atascados con el neerlandés
mode: autonomous
music: owner's track, re-edited on its own bar grid (audio_v2.json): STOP at 97.70 (start of frame 20), DROP at 100.92 (start of frame 21), breakdown from 168.12, riser 182.52, tension bar 184.92, RE-DROP 187.32 (start of frame 38), final hit 199.32 (frame 39 + 3.60)
---

# STORYBOARD v2 — Nawar VSL (Formación Nawar A0–A1)

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

## Frame 4 — "Llevas años aquí. Trabajas, pagas tus impuestos, sacas adelante a tu familia."

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

## Frame 15 — "Vocabulario real. El del trabajo, el médico, el colegio de tus hijos y el ayuntamiento. Nada de la manzana es roja."

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

- src: compositions/frames/17-traducir.html
- ground: nawar-blue
- entrance: target icon spins in (rotation -90→0, scale)

Scene 1 (0.0–1.5s): a bullseye target icon (white rings + blue-light center) center-top; lead
"Todo con un objetivo:" (0.12–0.57).
Scene 2 (1.5–3.29s): a head silhouette in profile (SVG, white 12 % fill + white outline) center; inside
it a two-arrow loop "ES ⇄ NL" that rotates (finite, ~1.5 turns) while "que dejes de **traducir**"
builds (1.56–2.12); on "traducir" (2.12) the loop snaps/breaks (arrows fly apart) and a single clean
arrow → a white speech bubble «Ja, natuurlijk!» pops out of the mouth area on "cabeza" (2.73).

**v2 change:** the voice now says «Todo para que dejes de traducir en tu cabeza.» (no «con un objetivo»). Drop the target/dart scene; open directly on the head + ES⇄NL loop scene with the line «Todo para que dejes de / TRADUCIR / en tu cabeza.», timed to the v2 cues.

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

## Frame 20 — PAUSE: "Vale, ¿y qué hay dentro? Te lo cuento."

- src: compositions/frames/20-pausa.html
- ground: nawar-blue, slightly darker (stronger vignette) — the film is PAUSED
- entrance: none moving — a hard cut to a frozen, still image (that IS the effect). Only the player bar slides up.
- music: the music STOPPED at t=0 (silence until the drop at the end of this frame = start of 21)
- reference: Offlesson VSL — closed laptop lid lying diagonally across the frame with a big ▶ on it
  and the question under it; a cursor clicks ▶ and the lid opens on the drop. Contact sheets of the
  reference (look, do not copy their branding): /tmp/claude-0/-home-user-nawar-web/36d31257-d6ae-5587-b324-a9f00bcc433b/scratchpad/material/v2/f/efecto.jpg,
  efecto-zoom1.jpg, efecto-zoom2.jpg (same folder).

Scene 1 (0.0–0.6s): STILL. The closed laptop lid (see shared geometry "laptop") lies diagonally across
the frame, seen from above; a big glassy ▶ play disc in its middle. At t=0 a pause glyph ❚❚ (white,
120 px) flashes at center for 0.25 s (opacity 1 → 0, scale 1 → 1.15) as if someone hit pause, and a
video-player control bar slides up from the bottom (y 1080 → its rest at bottom 40 px, 0.3 s
power3.out): ▶ icon · scrubber (white 30 % track, white fill at 48 %, round knob) · timecode
"1:37 / 3:22" (Inter 600 24 px white-72). Everything else is frozen — no drift.
Scene 2 (0.6–2.2s): the question builds ON the lid, under the ▶: "Vale," (Caveat 700 64 px, sky,
slight -4° tilt) above-left on its cue; then "¿Y qué hay" (display-h2, white) word by word on
"y · qué · hay", and **DENTRO?** (display-hero-ish 150 px, Poppins 900, blue-light #4da3ff with a soft
glow) slams on "dentro?" (scale 1.25 → 1 + blur 10 → 0, 3-frame micro-shake of the text only).
Scene 3 (2.2–3.22s): "Te lo cuento." (lead, white-72) fades in small under it on its cue. A white
arrow cursor (macOS style, black 2 px outline, 46 px) enters from the bottom-right at 2.3 s and glides
(power2.inOut) to the ▶ arriving at 2.95 s; at 3.05 s it clicks (cursor scale 0.86 and back; ▶ disc
darkens; a white ring ripples out from the ▶ 1 → 1.8, opacity 0.7 → 0); at 3.12 the player bar's
icon flips to ❚❚ (playing). The last 0.1 s: the lid starts to lift (hinge side) by 3–4° — the
opening continues in frame 21.
SFX: click-soft @0.0 (0.25) · click @3.05 (0.35).
Handoff_out to 21: lid, ▶ and cursor exactly as at 3.22 s (shared geometry "laptop"); the text and the
player bar are cut away by the drop.

## Frame 21 — THE DROP: laptop opens on the school · "Dieciséis semanas de formación guiada."

- src: compositions/frames/21-portatil.html
- ground: nawar-blue (full brightness on the drop)
- handoff_in: the closed lid + ▶ from frame 20 (shared geometry "laptop")
- music: the DROP lands at t=0 — this is the biggest visual moment of the film.

Scene 1 (0.0–1.0s): ON THE DROP: a white flash (opacity 0.55 → 0 in 0.25 s) and the lid swings open
in CSS 3D: it rotates up around its hinge while the whole laptop rotates from the top-down diagonal
to a 3/4 front view (lid ≈ upright facing camera, keyboard deck foreshortened below it), the ▶ and
cursor fly off with the lid's motion; the camera pushes in a little (scale 0.92 → 1). Motion 0.0–0.9,
expo.out — fast start, soft landing. Light streak (light-sweep-pass) crosses the screen glass at 0.6.
Scene 2 (0.9–2.0s): the screen is black with the Nawar logo (assets/img/logo-nawar.png, ~520 px wide
on the screen) blooming in with a blue-light glow behind it (like a boot screen): scale 0.85 → 1,
glow 0 → 1; a slow 3D orbit of the laptop starts (rotateY ~18° → -12° over the rest of the frame).
Scene 3 (2.0–3.9s): the logo dissolves into the school: the screen plays assets/video/nuestra-vision.mp4
(the website hero with the real "Nawar" 3D sign on the building, «Ayudarte a aprender neerlandés»,
media-start 0) for ~1.3 s, then cuts (inside the screen) to the platform dashboard
assets/video/inicio-home.mp4 (media-start 0.0 — «Hola, Team», continue lesson, «Tu repaso de hoy»).
The laptop keeps orbiting (it should feel like the reference's rotating laptop: the screen catches a
light sweep as it turns).
Scene 4 (3.9–6.22s): the laptop glides to the left third (x center ≈ 640, scale ≈ 0.78, still 3D);
on the right: **16** (Poppins 900 ~300 px, white with a blue-light glow) slams on "Dieciséis" — a
quick count 1 → 16 in 0.35 s is fine; **SEMANAS** (display-h2, white, letter-spacing 0.04em) on
"semanas"; "de formación guiada" (lead, white-72; "guiada" in blue-light) on "formación"/"guiada".
Under them a row of 16 small rounded week pills (each 34×12, white 22 %) fills left → right in
blue-light between "semanas" and "guiada" (stagger ~0.05 s) — a 16-week guided route.
SFX: impact-bass-1 @0.0 (0.5) · whoosh-cinematic @0.02 (0.35) · sparkle @1.0 (0.25) · pop @4.19 (0.3).

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

## Frame 24 — "Aprendes con vídeos cortos que te explican cada tema, y después practicas de verdad."

- src: compositions/frames/24-videos.html
- ground: nawar-blue
- entrance: browser window swings in (rotationY -22° → -8°, x +300 → 0, 0.35 s)

Scene 1 (0.0–2.8s): a large browser window (browser-device-stage look: dark chrome, 3 dots, URL pill
"holandesnawar.com/escuela") on the right ~60 % of the frame, slightly 3D-tilted, playing
assets/video/clases-video-dentro.mp4 from media-start 0.0 (the video lesson slide «Dit is / Dit zijn»
with the NATIVE TEACHER's webcam tile at its top-left). On "vídeos cortos" a white pill
**MICROLEARNING** (label typography, indigo text, a small ▶ icon) pops on the window's top-left corner
and a thin progress bar under the video fills (short video). Left column, big type: "Aprendes con"
(lead, white) → **VÍDEOS CORTOS** (display-h1, white; "CORTOS" blue-light) on "vídeos · cortos";
"que te explican **cada tema**" (lead; "cada tema" white bold) on "explican · cada · tema,". Push the
camera slightly toward the teacher tile on "explican" (scale 1 → 1.08 focused on the webcam tile).
Scene 2 (2.8–4.4s): seam: the browser window flips on its Y axis (rotationY → 90°, then the back face
from -90° → 0) on "después" to reveal an exercise screen: assets/img/ui-lezen-texto.png (real reading
exercise). Left type swaps to **PRACTICAS DE VERDAD** ("DE VERDAD" in a white word-chip with indigo
text) on "practicas" / "verdad.". Hold.
SFX: whoosh-short @0.0 (0.3) · pop @0.71 (0.25) · whoosh @2.95 (0.3).

## Frame 25 — "Lectura, escritura y escucha activa."

- src: compositions/frames/25-practica.html
- ground: nawar-blue
- entrance: first card slams in from the left with motion-blur streak (0.25 s)

Three tall cards (white, radius 28, ~520 × 640, card-on-blue shadow, gap 40, centered) each showing a
REAL exercise inside its top area and a big label under it:
1. on "Lectura," → card 1 slams in from the left: assets/img/ui-lezen-texto.png (crop to the Dutch
   text + question) — label **Lectura** (Poppins 800 54 px, indigo) + tiny "Lezen" (label, muted).
2. on "escritura" → card 2 slams down from the top: assets/video/completa-frase.mp4 (media-start 4.0:
   the student types the missing word «alstublieft» into «Een koffie, ___ (por favor)»; crop to the
   sentence + input) — label **Escritura** + tiny "Schrijven".
3. on "escucha" → card 3 slams in from the right: assets/img/ui-luisteren-audio.png (crop to the
   waveform player) with an animated playhead sweeping the waveform — label **Escucha activa**
   ("activa" in blue-vivid) on "activa." + tiny "Luisteren".
Each landing gives the previous cards a small recoil (x ±12 px). The labels land on their cues. Hold
on the trio.
SFX: whoosh-short @0.10 (0.3) · whoosh-short @0.74 (0.3) · whoosh-short @1.53 (0.3) · pop @1.97 (0.25).

## Frame 26 — "Además tienes flashcards para que el vocabulario se quede y no se te escape a la semana."

- src: compositions/frames/26-flashcards.html
- ground: nawar-blue
- entrance: a 3D flashcard flips in from edge-on (rotationY 90° → 0, 0.3 s)

Scene 1 (0.0–1.8s): left: a laptop/browser playing the REAL flashcards tool
assets/video/flashcards.mp4 (media-start 0.0: card «el bocadillo» → flips to «het broodje»,
«Repasar» / «Ya lo sé» buttons; 1718×842 source, the card sits around x≈1030, y≈310 — inspect frames
with ffmpeg to place your crop/zoom). Right: big kinetic type: "Además tienes" (lead, white) →
**FLASHCARDS** (display-h1, white) on "flashcards". In front, a crafted 3D flashcard prop (white card
420 × 260, radius 24) flips on "flashcards": front «el bocadillo» (Poppins 700 48 px, ink) → back
«het broodje» (Poppins 800 52 px, indigo) with a small Dutch flag tag.
Scene 2 (1.8–2.8s): "para que el vocabulario" (lead) → **SE QUEDE** (display-h2) on "quede": a
deck of four word cards (het broodje · de vis · komen · geen — real words from the tool) snaps into a
neat stack with a pin/lock tick (svg check) — the vocabulary stays.
Scene 3 (2.8–4.55s): on "no se te escape": the top two cards try to fly away (rise + rotate, slight
blur) and get pulled back into the stack on "escape" (spring back, power3.out) — they don't escape;
"a la semana." (lead, white-72) on "semana."; a tiny weekly calendar strip under the deck (L M X J V S
D) with every day ticked blue-light. Hold.
SFX: whoosh-short @0.78 (0.25) · pop @2.51 (0.25) · whoosh-short @3.37 (0.25).

## Frame 27 — "¿Te atascas un martes por la noche? Preguntas dentro de la escuela y te responden. Tus dudas no se quedan esperando."

- src: compositions/frames/27-consultas.html
- ground: NIGHT (night-glow) for scene 1, flooding to nawar-blue in scene 2 (the doubt gets light)
- entrance: a phone-lock-screen style clock zooms in from blur (scale 1.2 → 1, 0.3 s)

Scene 1 (0.0–1.8s): night ground with a few fine stars (deterministic dots) and a crescent moon (svg)
top-right. Center: a lock-screen style clock **23:14** (Poppins 300-ish → use 600 at 200 px, white)
with "martes" (lead, white-72) above it on "martes"; "¿Te atascas…" (lead, white) on "Te · atascas";
"…por la noche?" on "noche?" (the moon glows on "noche").
Scene 2 (1.8–3.4s): seam up: a laptop rises showing assets/video/consulta-nueva.mp4 (media-start 1.0:
the real "Nueva consulta" form, category «Gramática», typing «cómo se traduce gezellig?», «Publicar
consulta»); the ground floods from night to nawar-blue (radial wipe from the screen). Type:
**PREGUNTAS** (display-h2, white) on "Preguntas"; "dentro de la escuela" (lead) on "dentro · escuela".
On "responden." an answer card pops in front (assets/img/ui-consulta-respondida.png — the real
answered consulta; crop to the modal ≈ x 560–1510, y 250–700) with a success pill "✓ Respondida"
(success-on-dark fill, ink text, svg check).
Scene 3 (3.4–6.57s): **Tus dudas** (display-h2) on "Tus · dudas"; an hourglass/"esperando…" chip with
three animated dots (finite) is struck out on "no se quedan" and replaced by the ✓; **NO SE QUEDAN
ESPERANDO.** builds on "no · quedan · esperando." (key word "ESPERANDO" in a white chip / indigo text).
Hold.
SFX: notification @0.70 (0.2) · typing @1.9 (0.18) · ping @3.0 (0.3) · pop @5.39 (0.25).

## Frame 28 — "Y cada semana una clase en directo, con los mismos profesores que te explican en los módulos."

- src: compositions/frames/28-directo.html
- ground: nawar-blue
- entrance: calendar card swings in (rotationX 25° → 0, 0.3 s)
- REUSE: v1 frame compositions/frames_v1/22-clase-directo.html built the calendar + "● EN DIRECTO" +
  video-call look — re-use its look and pieces, re-timed to THIS voice.

Scene 1 (0.0–2.3s): a laptop showing assets/img/ui-eventos-calendario.png (the real "Eventos" calendar
with "Clase en directo" entries); **CADA SEMANA** (display-h2, white) on "cada · semana"; on "semana"
a blue-vivid highlight ring finds one "Clase en directo" entry and the camera zooms toward it; on
"directo," a red pill "● EN DIRECTO" (alert dot + white text on #E02D3C… keep it as v1) pops; type
"una clase **en directo**" on "clase · directo,".
Scene 2 (2.3–5.09s): seam left: a video-call card (rounded, dark bezel, "● EN DIRECTO" tag) plays
assets/video/clases-video-dentro.mp4 framed on the NATIVE TEACHER's webcam tile (source region ≈ x
840–1190, y 175–375 of 2560×1376; media-start 1.0) — big, centered-right; next to it a smaller card
"Módulo · vídeo" showing the same lesson slide (same video, full frame, media-start 3.0). Type:
"con los" (lead) → **MISMOS PROFESORES** (display-h2, "MISMOS" blue-light) on "mismos · profesores";
"que te explican en los módulos." (lead, white-72) on "explican · módulos.". A thin connector line
draws between the two cards on "módulos." (same person in both). Hold.
SFX: whoosh-short @0.0 (0.25) · pop @1.71 (0.3) · whoosh-short @2.3 (0.25).

## Frame 29 — "La cara que te enseña en el vídeo es la que te corrige en directo. Te conocen y saben dónde estás."

- src: compositions/frames/29-mismo-profe.html
- ground: nawar-blue
- entrance: split-screen slam — two portrait cards slide in from left and right and meet (0.3 s)

Scene 1 (0.0–3.3s): two big cards side by side (~760 × 480 each, gap 40): LEFT "EN EL VÍDEO"
(label pill) — the teacher's webcam tile from assets/video/clases-video-dentro.mp4 (media-start 0.5,
cropped to the webcam region ≈ x 840–1190, y 175–375), with a ▶ progress bar; RIGHT "EN DIRECTO"
(red "● EN DIRECTO" pill) — the SAME teacher crop (media-start 4.0, slightly different moment) with a
video-call UI (mic/cam icons, 2 small participant placeholder tiles with initials, no real names).
On "cara" a white face-frame bracket (four corner marks) snaps around the teacher's face on the LEFT
card; on "vídeo" the bracket is copied (a clean match-cut line sweeps) onto the RIGHT card on "es la
que"; on "corrige" a correction chip pops by the right card: «Werkt jij?» with an alert strike →
«Werk jij?» with a success ✓. Headline across the top: **LA MISMA CARA** (display-h2, white; "MISMA"
blue-light) building on "La · cara … es · la · que".
Scene 2 (3.3–5.78s): **TE CONOCEN** (display-h2) on "Te · conocen"; under the right card a small
progress card "Tu progreso · Módulo 3 · Eten en drinken" with a ring at 40 % and a location pin
"Estás aquí" pops on "dónde · estás." — they know where you are. Hold.
SFX: whoosh-short @0.0 (0.3) · click @0.27 (0.25) · pop @2.22 (0.3) · ping @5.13 (0.25).

## Frame 30 — "Y una cosa más. Aquí no hay tests de la a, la be, la ce o la de."

- src: compositions/frames/30-sin-tests.html
- ground: nawar-blue
- entrance: "Y una cosa más." — a single raised-finger "1" (svg, white) pops center with the words (it
  is the beat itself; 0.2 s spring-pop)

Scene 1 (0.0–1.25s): center: "Y una cosa más." (display-h3 → lead size, white) word by word with a
small "+1" badge (blue-light). Quick and light.
Scene 2 (1.25–4.57s): seam down: a generic multiple-choice quiz card (shared "quiz card" design in
your packet — NOT the Nawar platform) slams in on "tests": question «¿Qué significa "gezellig"?» and
four options A «aburrido» · B «acogedor» · C «caro» · D «rápido». Above it: **AQUÍ NO HAY TESTS**
(display-h2, white; "NO" in an alert-red word-chip) on "Aquí · no · hay · tests". Then each option's
letter badge gets an alert-red ✕ that draws over it EXACTLY on its spoken letter: A on "a,"
(2.43), B on "be," (3.02), C on "ce" (3.55), D on "de." (4.16) — each with a tiny shake of that row
and the row greys out. Hold on the fully crossed card.
SFX: pop @0.70 (0.25) · whoosh-short @1.78 (0.25) · error @2.43 (0.15) · error @4.16 (0.15).

## Frame 31 — "Estamos cansados de esos ejercicios en los que aciertas por pura suerte y te crees que vas avanzando."

- src: compositions/frames/31-suerte.html
- ground: nawar-blue
- entrance: the quiz card (same design as 30, fresh/uncrossed, smaller, left side) drops in with a
  slight 3D tilt (0.3 s)

Scene 1 (0.0–2.2s): **CANSADOS** (display-h2, white) lands on "cansados"; "de esos ejercicios" (lead)
on "ejercicios"; the quiz card sits left (scale ~0.8) with a cursor hovering indecisively between
options (eeny-meeny path B→D→A→C, deterministic).
Scene 2 (2.2–3.8s): on "aciertas" the cursor clicks C at random → the row turns success green with
"¡Correcto!" and small confetti (svg rectangles, deterministic) — but on "pura suerte" a big white 3D
die (CSS cube, 200 px, indigo pips) tumbles in from the right and lands showing 4 — **PURA SUERTE**
(display-h1; "SUERTE" blue-light) on "pura · suerte".
Scene 3 (3.8–5.41s): "y te crees que vas" (lead) → a progress bar "Tu progreso" fills fast to 80 %
with a "+10 %" pop on "avanzando." … and then visibly CRACKS/glitches (glitch-1 sfx, bar flickers
alert-red, drops back to 20 %) — fake progress. **AVANZANDO** with quote marks «avanzando» (lead,
white-72, italic) on "avanzando.". Hold on the cracked bar.
SFX: click @2.31 (0.3) · sparkle @2.4 (0.2) · whoosh-short @2.9 (0.25) · glitch-1 @4.9 (0.25).

## Frame 32 — "En Nawar escribes, ordenas frases, escuchas y respondes, completas sin pistas."

- src: compositions/frames/32-practicas.html
- ground: nawar-blue
- entrance: "En Nawar" slides in with a light sweep (0.25 s)

Left column: a vertical list of four verbs that stack in on their cues (display-h2, white, each with
a small blue-light numeral 01–04 and a check that draws when it lands): **ESCRIBES** (0.56) ·
**ORDENAS FRASES** (1.47) · **ESCUCHAS Y RESPONDES** (2.46) · **COMPLETAS SIN PISTAS** (3.82; "SIN
PISTAS" blue-light). The active verb is full white; previous ones dim to 45 %.
Right column: ONE device/card whose content swaps with each verb (scale-swap-transition / fast slide
up), always the REAL product:
1. escribes → assets/video/completa-frase.mp4 (media-start 4.0, typing the word in «Een koffie, ___
   (por favor)»), zoomed on the input.
2. ordenas frases → assets/img/ui-ordena-palabras.png (the real «Ordena las palabras» exercise:
   «Quiero un vaso de agua, por favor.»); animate crafted word chips (same style as the screenshot's
   chips: wil · een · glas · alsjeblieft. · water, · Ik) flying from the chip row into the dashed
   answer area in the correct order «Ik wil een glas water, alsjeblieft.» on "ordenas · frases,".
3. escuchas y respondes → assets/img/ui-luisteren-audio.png with an animated playhead + 3 small
   speaker waves.
4. completas sin pistas → assets/video/completa-frase.mp4 (media-start 11.0: the second sentence,
   student fills it, «Comprobar», green «¡Correcto!» bar) and a "pista" lightbulb icon struck out with
   an alert line on "sin · pistas.".
SFX: key-press @0.56 (0.25) · click @1.47 (0.25) · pop @2.46 (0.25) · key-press @3.82 (0.25).

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

## Frame 38 — CTA (RE-DROP): "Completa tu matrícula en el siguiente paso y contactamos contigo. Vemos tu nivel, tu situación y si la formación encaja contigo. Sin compromiso."

- src: compositions/frames/38-cta.html
- ground: nawar-blue, full brightness (the RE-DROP lands at t=0)
- entrance: ON THE DROP: a white flash (0.5 → 0, 0.2 s) and a huge CTA button slams in (scale 1.6 →
  1, blur → 0, expo.out) with a shockwave ring.

Scene 1 (0.0–2.0s): the CTA button (white pill ~1100 × 150, radius 999, indigo text Poppins 800 64 px)
"Completa tu matrícula" + a blue-vivid circle with a → arrow at its right end; it lands on "Completa"
and its text builds "Completa · tu · matrícula" (or it is fully there and the word "matrícula" gets
the accent on its cue). A white cursor glides in and CLICKS the button on "siguiente paso" (1.18–1.57):
button presses (scale 0.96), ripple. Under it: "en el siguiente paso" (lead, white-72) with a small
"↓ debajo de este vídeo" hint? NO — keep only "en el siguiente paso" (we don't know the page layout).
Scene 2 (2.0–3.4s): the button morphs (Flip or scale swap) into a contact card: a phone/chat icon in a
blue-vivid circle ringing (3 finite wiggles) + **TE CONTACTAMOS** (display-h2, white) on
"contactamos · contigo." — a small "Equipo Nawar" label with the logo (logo-nawar.png, ~180 px).
Scene 3 (3.4–7.2s): "Vemos" (lead) then three check-chips land in a row (white pills, indigo text,
success ✓ circle): **Tu nivel** on "nivel," · **Tu situación** on "situación" · **¿Encaja contigo?**
on "encaja · contigo.".
Scene 4 (7.2–8.4s): **SIN COMPROMISO.** (display-h1, white; inside a success-on-dark outline stamp,
rotated -3°) stamps on "Sin · compromiso." (7.27–7.53) with a 3-frame shake. Hold.
NO PRICE anywhere.
SFX: impact-bass-1 @0.0 (0.45) · click @1.30 (0.35) · notification @2.07 (0.3) · impact-bass-2 @7.30 (0.3).

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
