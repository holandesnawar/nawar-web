## v3 polish — a top studio, not an AI template

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

## Frame 17 — "Todo con un objetivo: que dejes de traducir en tu cabeza."

- src: compositions/frames/17-traducir.html — the v1 design is back (target + dart on «OBJETIVO», then the head
  with the ES⇄NL loop and «que dejes de TRADUCIR en tu cabeza»), retimed v1 → v3 by tools/retime_v2.py.

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
- music: the DROP lands at t=0 (calmer mix than v2). Voice comes back at 2.79 s.
- 0.0–1.0 s: the lid swings open toward the camera while the camera settles STRAIGHT ON — ending exactly in the
  front-view MacBook of tools/mac_mockup.md (screen + thin base lip). The keyboard must never be seen (the owner
  explicitly asked: «sin que se le vean las teclas, simplemente de frente»): e.g. keep the camera at deck height so
  the deck is hidden behind the front lip, or let the lid hinge up past the camera axis while the body is already
  front-on. No white flash (a soft light lift is enough), no shock rings.
- 0.9–1.9 s: screen boot: the Nawar logo fades in on the dark screen (no glow halo — a faint screen bloom only).
- 1.9–4.0 s: the macOS browser appears (traffic lights, `app.holandesnawar.com`) with the website hero
  (assets/video/nuestra-vision.mp4 — the school building with the Nawar sign) and then the platform dashboard
  (assets/video/inicio-home.mp4 from media 1.4). At most a very slow push (≤ 3 %) — no zoom inside the screen.
- From «Dieciséis» (2.79): the Mac glides to the left (still front-on, no 3D tilt); right column: «16» (Poppins 900),
  «semanas» (Poppins 800), «de formación guiada» (Poppins 600, white-72, «guiada» in #4da3ff), and the row of 16
  week pills filling left → right between «semanas» and «guiada».

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

## Frame 38 — CTA (RE-DROP): "Completa tu matrícula en el siguiente paso y contactamos contigo. Sin compromiso."

- src: compositions/frames/38-cta.html — 4.27 s, starts exactly on the re-drop.
- Keep v2's idea (big «Completa tu matrícula →» button, cursor click on «siguiente paso», morph into the «Te
  contactamos» card with the team logo, «Sin compromiso.» stamp at the end) but: REMOVE the three «Tu nivel / Tu
  situación / ¿Encaja contigo?» chips (no longer in the voice), REMOVE the spark streaks/shock rings/rays; the drop
  is carried by a clean, confident button entrance. «Sin compromiso.» on «Sin · compromiso.» as a clean outlined
  label (no shake). NO PRICE.
