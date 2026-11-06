---
format: 1920x1080
duration: 121.6s
message: "El neerlandés no se te da mal: te lo estaban enseñando desde el inglés. Nawar te lo enseña desde el español."
arc: Hook → Pain (life) → Pain (failed attempts) → Reframe (it's the method) → Nawar → 3 phases → Sounds → Inside the school → Community → End card
audience: hispanohablantes en Países Bajos / Flandes, atascados con el neerlandés
mode: autonomous
music: TBD (owner to supply; none reachable offline)
---

# STORYBOARD — Nawar VSL (Formación Nawar A0–A1)

All times inside a frame are **frame-relative seconds**. Exact per-word cue times for every frame are
in `timing.json` and are inlined into each frame packet — every reveal must land on its word's cue
(≤ 0.06 s early, never late). Master timeline: frame N starts at `timing.json → frames[N].start`.

## Video direction

**Look.** Two worlds (see `frame.md`): PAPER (light #F5F7FF + indigo dot grid; ink text; alert-red
accents) for the viewer's frustrating reality (01–10, plus 15 and 18 as contrast beats later), NIGHT
(#07041F glow) for the intimate questions (09), and NAWAR BLUE (radial #025dc7 → #120081) from the turn
(11) onward. Absolutely no orange anywhere. Yellow only inside the logo image.

**Energy.** Reference = a fast VSL: something new arrives on almost every spoken phrase; big key words
land exactly on the voice; props and UI are concrete, not decorative. Each frame cuts in **hard** on
its first word — so every frame's first 0.25 s carries a strong *entrance move* (the "cut-the-curve"
arrival: a slam, a fast slide with motion-blur streak, a zoom-in from blur, or an iris), named per
frame below. No frame has an exit (the next frame's entrance is the transition); only 25 fades out.

**Motion grammar.** power3.out for entrances, power4/expo.out for slams, ≤ 0.35 s per word reveal;
reveals paced to the word cues; after the last reveal, hold still (subtle jitter at most).
Overshoot only for the logo bloom and check pops. Within-frame scene changes are velocity-matched
seams (outgoing moves up/left fast while incoming continues the same direction).

**Type.** Not every word is shown: 2–6 key words per sentence, the rest as a smaller lead-in line or
nothing. Key words: Poppins 800/900, big. One accent per moment (chip OR color OR strike).

**Rhythm / holds.** Deliberate held beats: end of 06 ("Otra vez." holds), end of 10 (alone with
errors), 11 (logo breath), end of 24 → 25 (end card hold). Everything else keeps arriving.

**Negative list.** No orange. No stock-photo look, no emoji glyphs (no emoji font in the renderer —
draw icons as inline SVG), no Duolingo owl / branding, no fake platform UI where real footage exists,
no lazy breathing, no slow back-half pans, no repeat/yoyo, no CSS animations, no text below y=1000,
nothing important within 60 px of the frame edges.

**Sound.** Each worker writes a sidecar `compositions/frames/<id>.sfx.json` naming SFX cues
(whoosh-short on whip entrances, pop/click on reveals and ticks, impact-bass on slams, glitch/error on
"atascado"/"funcionar", riser into 11, chime on 25). Keep it tasteful: ≤ 4 cues per frame, quiet.

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

## Frame 2 — "No es que no valgas"

- src: compositions/frames/02-no-valgas.html
- ground: paper
- entrance: hard slam of "NO" at 0.12 (scale 1.6→1, blur→0)

Scene 1 (0.0–0.75s): giant **NO** (display-hero ×1.6, ink) slams dead center on "no," (0.18). SFX impact-bass-2 (quiet).
Scene 2 (0.75–2.66s): NO shrinks to the top third (power3) while a line builds below on cues:
"es que · no valgas · para los idiomas" (display-h2, ink). On "valgas" (1.31) an alert-red strike draws
across "no valgas". On "idiomas" (1.99) "idiomas" gets an indigo word-chip pop. Hold.

## Frame 3 — "Te lo explico en menos de tres minutos"

- src: compositions/frames/03-tres-minutos.html
- ground: paper
- entrance: stopwatch ring zooms in from 0.6 with blur (0.0–0.25)

Scene 1 (0.0–1.1s): an indigo stopwatch (SVG: ring + crown + two side buttons) center-left; its ring
track draws; small lead text "Te lo explico" (0.12) at top. Inside the ring: "3:00".
Scene 2 (1.1–2.31s): on "tres minutos" (1.18–1.41) the right side shows "en menos de" (lead) and
**3 MINUTOS** (display-h1, indigo) slams; the ring's progress arc starts sweeping and the center
counts down 3:00 → 2:59 → 2:58 (a tick each 0.5 s, deterministic). SFX click-soft on each tick.

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

## Frame 11 — THE TURN: "Nawar nace para cambiar eso."

- src: compositions/frames/11-nawar-nace.html
- ground: paper → nawar-blue
- entrance: iris — a nawar-blue circle grows from center (clip-path circle 0 → 150 %) 0.0–0.35, white flash ring at its edge

Scene 1 (0.0–0.5s): iris floods the frame with nawar-blue; on "Nawar" (0.12) the logo
(assets/img/logo-nawar.png, ~820 px wide) blooms center (scale 0.55→1.04→1, blur 16→0) with a soft
blue-light glow behind it; a light-sweep band crosses the logo once (0.35–0.9). SFX impact-bass-1 @0.12.
Scene 2 (0.5–1.95s): logo eases up 90 px; white lead line below builds on cues "nace · para ·
**cambiar** · eso." (lead, white; "cambiar" blue-light). Hold.

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

## Frame 13 — "Tres fases. Supervivencia."

- src: compositions/frames/13-tres-fases.html
- ground: nawar-blue
- entrance: three pills slam in left→right (0.12, 0.22, 0.32) with motion-blur streaks

Scene 1 (0.0–1.0s): **3 FASES** small label on top; three big pills in a row: "01 Supervivencia",
"02 Vocabulario real", "03 Estructura y soltura" (pill component, lead size).
Scene 2 (1.0–2.14s): on "Supervivencia" (1.05) pill 01 fills white (indigo text), pills 02/03 dim to
35 %, and the camera pushes in toward pill 01 (scale 1→1.25 centered on it, 1.05–2.1) — a hand-off
into frame 14. SFX whoosh-short @1.05.

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

## Frame 19 — "Son los que te delatan, y los entrenamos uno a uno"

- src: compositions/frames/19-delatan.html
- ground: paper
- handoff_in: the four keycap tiles G/UI/UU/EU exactly as frame 18 ended (row at y=430, x 282/652/1022/1392, 300×300, opacity 1, still); the six small chips are NOT carried over.

Scene 1 (0.0–1.15s): on "delatan" (0.70) all four tiles flash an alert-red outline and a red radar
ring pulses once out of each (finite) — "te delatan"; small label above "te delatan" (display-h3, alert).
Scene 2 (1.2–2.87s): the red outlines clear; on "entrenamos uno a uno" (1.47–2.43) each tile gets a
success ✓ badge popping in sequence (1.5, 1.85, 2.2, 2.45) and turns indigo-filled with white letters.
SFX click per ✓.

## Frame 20 — "¿Cómo es por dentro? Cada módulo se abre cuando terminas el anterior."

- src: compositions/frames/20-por-dentro.html
- ground: nawar-blue
- entrance: zoom-through — a laptop rushes toward camera from small (scale 0.4→1, blur→0) 0.0–0.45

Scene 1 (0.0–1.3s): laptop center playing assets/video/formacion-cv.mp4 (media-start 0.0, the real
course page "Formación Nawar A0-A1 · De cero a tu primera conversación"); "¿Cómo es por dentro?"
(display-h3, white) above it. On "dentro" (0.53) the camera dives INTO the screen (laptop scales to
~2.6× centered on the screen, the bezel leaving frame) — zoom-through.
Scene 2 (1.3–3.81s): out of the screen dive we land on a winding path (SVG road, white 20 % stroke)
across the frame with five module nodes using the REAL module names: 1 «Over jou» · 2 «Familie &
vrienden» · 3 «Eten en drinken» · 4 «Het werk» · 5 «Hobby's & vrije tijd». Node 1 has a ✓; nodes
2–5 show closed padlocks. On "abre" (2.10) lock 2 opens (shackle lifts, turns blue-light) and node 2
lights; on "terminas" (2.60) node 2 gets its ✓; on "anterior" (3.09) lock 3 opens. SFX click (unlock).
Handoff_out to 21: path + nodes exactly as at 3.81 s (state: 1 ✓, 2 ✓, 3 open, 4–5 locked).

## Frame 21 — "Tú marcas el ritmo, pero nunca vas solo."

- src: compositions/frames/21-tu-ritmo.html
- ground: nawar-blue
- handoff_in: identical path/node layout and state from frame 20's end (same SVG geometry — the two workers must share it: see "shared geometry" in the packet)

Scene 1 (0.0–1.05s): a white avatar disc "TÚ" (indigo text) drops onto node 2 and travels along the
path toward node 3 on "marcas el ritmo" (0.24–0.65), arriving on "ritmo".
Scene 2 (1.1–2.29s): on "nunca vas solo" (1.31–1.89) six companion avatar discs (initials: "MA",
"JL", "SO", "PE", "LU", "AN"; fills: blue-vivid, sky, white, blue-light, nl-blue, indigo with white
ring) pop onto the path around "TÚ" in a stagger, some slightly ahead, some behind, all advancing a
bit. Hold.

## Frame 22 — "Cada semana tienes clase en directo con profesores que te corrigen y te hacen hablar."

- src: compositions/frames/22-clase-directo.html
- ground: nawar-blue
- entrance: calendar card swings in (rotationX 25→0)

Scene 1 (0.0–1.8s): a laptop showing assets/img/ui-eventos-calendario.png (the real "Eventos"
calendar with "Clase en directo" entries); on "semana" (0.51) a blue-vivid highlight ring finds a
"Clase en directo" entry and the laptop zooms toward it; on "directo" (1.55) a red pill
"● EN DIRECTO" pops on the card (red dot is alert, text white).
Scene 2 (1.85–3.1s): seam left. A video-call card (rounded, dark bezel) plays
assets/video/clases-video-dentro.mp4 from media-start 1.0 (teacher webcam + slide) with a small
label "Profesor nativo"; on "corrigen" (2.79) a correction chip pops beside it: «Werkt jij?» with an
alert-red strike → «Werk jij?» with a success ✓ (the real doubt students ask: hij werkt / werk jij).
Scene 3 (3.1–4.22s): a microphone icon with five voice bars bouncing (finite, deterministic) and
**HABLAR** (display-h2, white) on "hablar" (3.57).

## Frame 23 — "Y tienes una comunidad de compañeros que están haciendo el mismo camino que tú, en tu idioma."

- src: compositions/frames/23-comunidad.html
- ground: nawar-blue
- entrance: center pill pops; avatars burst outward from center (center→outward expansion)

Scene 1 (0.0–2.0s): center pill «Comunidad Nawar»; on "comunidad" (0.78) ~14 avatar discs (initials,
brand fills) expand outward from the center into a loose constellation with thin connector lines to
the pill (svg draw). "compañeros" (1.39) — the discs settle.
Scene 2 (2.0–4.1s): two Spanish chat bubbles pop near avatars: «¡Hoy pedí cita con el huisarts en
neerlandés!» (2.16) and «¿Alguien practica esta tarde?» (3.0); a third tiny «¡Yo!» reply (3.5).
Scene 3 (4.1–4.99s): **en tu idioma.** (display-h2, white; "tu idioma" blue-light) lands bottom-
center on 4.14–4.30. Hold.
Handoff_out to 24: avatar constellation as at the end.

## Frame 24 — "Avanzas a tu ritmo, pero acompañado."

- src: compositions/frames/24-acompanado.html
- ground: nawar-blue
- handoff_in: the avatar constellation from frame 23 (positions provided in shared geometry)

Scene 1 (0.0–1.3s): "Avanzas a tu ritmo," (lead, white, 0.12–0.73) top; the camera pulls OUT
(constellation scales 1→0.35) revealing hundreds of small dots (deterministic grid-jitter field) —
the scale of the community.
Scene 2 (1.3–2.59s): **acompañado.** (display-h1, white) lands on 1.46; under it a counter card counts
0 → **+30.000** (1.3–2.4, power3.out) with label "alumnos siguen nuestras clases en redes".
SFX ping when the counter lands.

## Frame 25 — End card

- src: compositions/frames/25-end-card.html
- ground: nawar-blue
- entrance: logo bloom (scale 0.6→1, blur→0) + light sweep

Scene 1 (0.0–1.0s): logo-nawar.png blooms center-upper (~760 px wide), glow behind. SFX chime @0.1.
Scene 2 (1.0–2.6s): claim builds word by word under it (display-h2, white): "Tu neerlandés empieza
**cuando lo hablas**." ("cuando lo hablas" blue-light), words every ~0.18 s from 1.0.
Scene 3 (2.8–6.2s): a pill "holandesnawar.com" (white fill, indigo text) rises at 2.9 and a small
label "Formación Nawar A0 → A1 · desde el español" (ui, white-72) at 3.2. Hold; from 5.6 everything
fades to night (#07041F) — the only exit in the film.
