# VSL Formación Nawar A0–A1 — proyecto HyperFrames (v4)

Vídeo de venta (16:9, 1920×1080, 2:57) hecho con [HyperFrames](https://hyperframes.heygen.com):
cada escena es una página HTML animada con GSAP que se renderiza a MP4.

**v4** (2:57): guion sin «sacas adelante a tu familia» ni «el colegio de tus hijos» (para no dejar fuera a
nadie) con la toma (4) de las tres que llegaron, a 1,065× (la que menos hay que acelerar para mantener la
estructura musical de la v3 por debajo de 2:58). En 1:31 el portátil se abre directamente sobre la web
(«nuestra visión», sin el logo sobre negro) y pasa a la página de la formación (`formacion-134.mp4`). Escena 04:
«Tienes tu vida montada» (casa con ventanas y puerta); escena 15: «de gemeente» + «de routine · tu día a día».

**v4.1** (2:57): en 0:56 el portátil arranca arriba del todo del panel («Hola, Team · Les 1») y baja con un scroll
suave hasta «Tus cursos · Comunidad · Próximos eventos» (página reconstruida desde la grabación con
`tools/stitch_page.py`); en 1:28 el cursor pulsa pausa y el clic, el cambio de icono y la parada de la música caen en
el mismo instante (la música para 0,30 s más tarde, `PAUSE_LEAD`); fuera el cursor de texto del arranque y la fila de
sonidos extra bajo G · UI · UU · EU. El gancho (hasta «…en menos de tres minutos») va a la velocidad natural de la
toma, con algo más de aire tras dos frases (`INTRO_*` en `build_audio_v4.py`); para seguir por debajo de 2:58 la
cola del logo final se acorta (`MAX_TOTAL`).

**v3** (2:57): voz nueva (toma B a 1,09×), música más suave, MacBook realista con ventana de macOS y contenido 16:9
en todas las escenas con ordenador, consultas y clase en directo nuevas (con el profe Paul), bloque de ejercicios
recortado, CTA más corta y un repaso de pulido en todas las escenas (fuera brillos, rayos, temblores y rebotes).

**v2** (sobre la v1 aprobada): voz nueva (toma B), música del cliente reeditada por compases, pausa estilo
Offlesson en «Vale, ¿y qué hay dentro?» con la música parada, apertura del portátil justo en el drop, y una
sección nueva que explica todo lo que incluye la formación (16 semanas, 10 módulos, +360 lecciones,
microlearning, lectura/escritura/escucha, flashcards, consultas, clase semanal con los mismos profes, sin
tests A/B/C/D). Las escenas 01–19 son las de la v1 reajustadas a la nueva voz; 01–03 pasan a fondo azul.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md` | Intención, público, reglas de marca (sin naranja, sin precio, profesores nativos…) |
| `STORYBOARD.md` | Las 37 escenas, plano a plano, atadas a la voz y a la música, + reglas de pulido v3 y cambios v4 |
| `frame.md` | Sistema de diseño: colores, tipografías, componentes |
| `audio_v4.json` | Plan de montaje de audio (v4): velocidad, parada, drop, re-drop, golpe final (`audio_v3.json`: el de la v3) |
| `transcript.json` | Tiempos de cada palabra de la locución (alineación forzada, tiempo del archivo de voz) |
| `timing.json` | Ventana de cada escena en la línea de tiempo y sus palabras |
| `compositions/frames/NN-*.html` | Una escena por archivo (+ `.sfx.json` con sus efectos de sonido) |
| `compositions/frames_v1/` | Escenas de la v1 tal cual (fuente del reajuste de tiempos) |
| `index.html` | Montaje final (lo genera `tools/assemble.py`) |
| `tools/` | Banda sonora (`build_audio_v4.py`), alineación, tiempos, reajustes de tiempos, generador del portátil, ensamblador |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh            # todos los medios desde el Drive (vídeos, capturas, voces, música, fuentes, gsap, sfx)
                                      # y monta la banda sonora v4 (tools/build_audio_v4.py → assets/audio/, audio_v4.json)
python3 tools/timing.py               # timing.json (cortes forzados en la parada, el drop y el re-drop)
python3 tools/gen_laptop_20_21.py     # escenas 20 y 21 (el portátil): duraciones y palabras salen de timing.json
python3 tools/assemble.py             # index.html
npx hyperframes lint
npx hyperframes render . --quality high -o renders/vsl-nawar-v4.mp4
```

Previsualizar una escena suelta: `python3 tools/preview_frame.py 21-portatil`.

## Música (reedición por compases, 100 BPM, compás = 2,4 s)

- Antes del drop (38 compases): cola de un compás de entrada + intro (9) → hats (8) → breakdown sin bombo (5) → hats (7) → breakdown + subida +
  tensión (8). Tras «…los entrenamos uno a uno» el cursor pulsa pausa y la música se para en seco (89,68 s).
- «Vale, ¿y qué hay dentro? Te lo enseño.» suena en silencio; el drop entra en 92,54 s con el portátil.
- Después: sección completa (24 compases) → breakdown desde «Al terminar…» (150,14 s) → subida (164,54 s) →
  tensión bajo «…probado. Ahora toca hablar» (166,94 s) → re-drop en «Completa tu matrícula» (169,34 s) → golpe
  final en «…cuando lo HAblas» (176,54 s) y cola hasta 177,95 s.

## v3: cómo se llevaron las escenas a la voz nueva

- Escenas que no cambiaban: `python3 tools/retime_stack.py <timing anterior> <ids…>` añade un bloque de reajuste
  de tiempos (las escenas de la v1 llevan dos: v1→v2 y v2→v3). El diseño no se toca.
- Escenas rehechas: 20–21 (`tools/gen_laptop_20_21.py`), 24/25/32 y 26/27 (fuentes de referencia en
  `tools/frame_sources/`), 28/29 y 38 escritas directamente sobre los tiempos v3.
- MacBook y ventana de macOS: `tools/mac_mockup.md` (contenido 16:9, URL `app.holandesnawar.com`).

## v4: cómo se llevaron las escenas a la toma nueva

- `python3 tools/retime_v4.py <timing anterior>` reajusta todas las escenas (menos 20–21) y de paso funde los
  bloques de reajuste que se habían ido acumulando (v1→v2→v3) en uno solo por escena. En 04 y 15, donde cambia
  el texto, empareja a mano las palabras antiguas con las nuevas.
- La alineación automática apretaba «El algún día · ya lo has probado. · Ahora toca hablar» (esta toma hace una
  pausa después de «día»): esas palabras se fijaron a mano en `tools/build_audio_v4.py` (`FIX`) a partir de
  Whisper y de la envolvente de la voz, para que «Ahora» no salga antes de tiempo.
