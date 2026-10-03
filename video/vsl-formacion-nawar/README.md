# VSL Formación Nawar A0–A1 — proyecto HyperFrames (v4)

Vídeo de venta (16:9, 1920×1080, 2:57) hecho con [HyperFrames](https://hyperframes.heygen.com):
cada escena es una página HTML animada con GSAP que se renderiza a MP4.

**v4** (2:57): guion sin «sacas adelante a tu familia» ni «el colegio de tus hijos» (para no dejar fuera a
nadie) con la toma (4) de las tres que llegaron, a 1,065× (la que menos hay que acelerar para mantener la
estructura musical de la v3 por debajo de 2:58). En 1:31 el portátil se abre directamente sobre la web
(«nuestra visión», sin el logo sobre negro) y pasa a la página de la formación (`formacion-134.mp4`). Escena 04:
«Tienes tu vida montada» (casa con ventanas y puerta); escena 15: «de gemeente» + «de routine · tu día a día».

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

- Antes del drop (37 compases): intro (9) → hats (8) → breakdown sin bombo (5) → hats (7) → breakdown + subida +
  tensión (8). La música se para en seco en 88,37 s, al acabar «…los entrenamos uno a uno».
- «Vale, ¿y qué hay dentro? Te lo enseño.» suena en silencio; el drop entra en 91,23 s con el portátil.
- Después: sección completa (24 compases) → breakdown desde «Al terminar…» (148,83 s) → subida (163,23 s) →
  tensión bajo «…probado. Ahora toca hablar» (165,63 s) → re-drop en «Completa tu matrícula» (168,03 s) → golpe
  final en «…cuando lo HAblas» (175,23 s) y cola hasta 177,13 s.

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
