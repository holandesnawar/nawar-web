# Reel «Suárez habla neerlandés» · Holandés Nawar (Instagram, 9:16) — proyecto HyperFrames

Segundo reel de Luis Suárez, en el formato del de Mario Casas (100 000 visitas) y del primero de Suárez
(`../reel-suarez`): una escena real en neerlandés, en vertical, con el título arriba y subtítulos en holandés y en español.
Esta vez es una entrevista de Sportweek TV a Suárez en el Amsterdam ArenA, sin la marca del canal.

- **Corte** (`SEGMENTS` en `tools/frame.py`): tres momentos de la entrevista de 4:17, uno tras otro (42,4 s):
  1. «Het was spannend.» — «Wie?»;
  2. «Feestje gevierd?» — «Sorry?» — «… in vier… in achtenveertig uur.» (48 horas);
  3. «Ben je blij dat je in de spits staat?» — «Voor mij maakt niet uit… Ik wil alleen maar spelen.»

  Fuera quedan la cortinilla «Sportweek TV» del principio y del final y los planos de recurso del entrenamiento.
- **9:16 a pantalla completa:** el encuadre sigue su cara con suavidad. Un detector de caras (YuNet) la encuentra en
  cada fotograma, y la cámara (mediana + gaussiana) mantiene toda la cara dentro del encuadre, también al empezar cada
  momento. Siempre queda a la izquierda del logo «SPORTWEEK.NL» de la esquina.
- **Nitidez:** el original está entrelazado, así que primero se desentrelaza (bwdif). Después cada encuadre se amplía ×4
  con Real-ESRGAN («realesr-general-x4v3», en ONNX y en CPU), se mezcla con un 40 % de ampliación normal y lleva un grano
  fino, para que la piel no quede de cera.
- **Sin marca:** el texto «SPORTWEEK» del micrófono se pinta con el rojo del propio micrófono (`mic()`), en todos los
  fotogramas, también cuando el borde del encuadre corta el micrófono (hasta el borde mismo). Se comprueba fotograma a
  fotograma antes de ampliar. El primer fotograma (la portada) es una copia del segundo: en el original pasa el micrófono.
- **Dos versiones (v4)**, para elegir:
  - **con tarjeta** (`python3 tools/gen.py`): arriba, todo el reel, una tarjeta blanca esmerilada grande (estilo Apple),
    «Aprendiendo neerlandés» y, debajo y en grande, «con Luis Suárez», con la bandera redonda de Países Bajos; es también
    la portada;
  - **solo subtítulos** (`python3 tools/gen.py --sin-tarjeta`): sin tarjeta.
- **Subtítulos:** por frases, sincronizados palabra a palabra (ElevenLabs Scribe, comprobado con una segunda pasada):
  - el holandés va grande, en mayúsculas, todo al mismo tamaño, con la palabra que se dice en amarillo;
  - el español va debajo, en una pastilla gris, en una línea siempre que cabe (si no, cortada a mano con «|»);
  - van abajo, sobre la barbilla: por encima de la franja del texto de Instagram (y ≤ 1500) y a la izquierda de su
    columna de botones (x < 912), con una sombra suave debajo;
  - las frases del periodista, que no sale en el plano, llevan una pastilla «Periodista»;
  - el holandés roto de Suárez se deja tal cual («Wij echt blij», «Trainer weet»); solo se quitan los «uh» y las
    repeticiones;
  - una frase no pasa nunca de un momento al siguiente, y entre dos frases seguidas no queda ningún fotograma vacío.
- **Sonido:** el de la entrevista, con un filtro de graves a 90 Hz (el viento y los golpes del micrófono de mano) y
  fundidos cortos en cada corte. La voz del periodista va más baja, porque está pegado al micrófono y sonaba mucho más
  fuerte que Suárez: 6 dB, 10 dB en el segundo momento y 8 dB en el último, que sube 3 dB porque Suárez habla ahí más
  bajo (`REPORTER_DB`, `SEG_DB`). Todo a −14 LUFS, con el pico real por debajo de −2,5 dBTP.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md`, `STORYBOARD.md` | Petición, decisiones y frase a frase |
| `index.html` | El reel (lo genera `tools/gen.py`) |
| `subs.json` | Subtítulos con el tiempo de cada palabra (lo genera `tools/subs.py`) |
| `tools/subs.py` | Las frases en holandés y en español (`PHRASES`), alineadas con la transcripción de Scribe |
| `tools/frame.py` | El corte, el seguimiento de la cara, el borrado del micrófono, la ampliación y el sonido → `assets/video/habla-916.mp4` |
| `tools/gen.py` | La composición: la tarjeta (o `--sin-tarjeta`) y los subtítulos |
| `tools/fetch_assets.sh` | Lo reconstruye todo desde el Drive |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh
npx hyperframes check
npx hyperframes render . --quality high --fps 25 -o renders/reel-suarez-habla-v4-tarjeta.mp4
python3 tools/gen.py --sin-tarjeta
npx hyperframes render . --quality high --fps 25 -o renders/reel-suarez-habla-v4-solo-subtitulos.mp4
python3 tools/gen.py
```

Para cambiar una traducción, edita `PHRASES` en `tools/subs.py` y ejecuta `python3 tools/subs.py && python3 tools/gen.py`.
Para cambiar el corte, edita `SEGMENTS` en `tools/frame.py` y ejecuta `python3 tools/frame.py --track && python3 tools/frame.py`
(unos 90 minutos) y después `python3 tools/subs.py && python3 tools/gen.py`.
