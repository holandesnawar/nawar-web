# Anuncio UGC #4 «Nuestro Black Friday empieza hoy» · Holandés Nawar (Meta / TikTok Ads, 9:16) — proyecto HyperFrames

Creativo UGC en vertical (1080×1920, 45,6 s): el Black Friday empieza antes de tiempo. La primera oferta es el libro
«Holandés sin miedo», para principiantes y explicado en español, por 1 € hasta el 30 de noviembre, y quien lo consigue
entra en la lista prioritaria y ve antes que nadie lo que preparamos para el Black Friday.

Es el lenguaje de los primeros anuncios de la Formación (`../ugc-nawar`, `../ugc-nawar-2`), no el vestido Black Friday
del último (`../ugc-nawar-bf`):
- Ella habla a cámara. Cuando explica algo, la imagen corta a un gráfico a pantalla completa (papel o azul Nawar) y
  vuelve a ella.
- Subtítulos blancos palabra a palabra; cierre con el botón azul «CONSÍGUELO POR 1 €».
- Solo una etiqueta blanca en el gancho («Black Friday anticipado»); nada de fondos de texto gigantes, negro ni amarillo.
- El ebook es la animación real del cliente («Animación Libro»), recortada de su negro y sobre el azul Nawar.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md`, `STORYBOARD.md` | Petición, tomas elegidas y plano a plano |
| `edit.json` | El montaje: tramos de la toma, ventanas de los gráficos, palabras con su tiempo |
| `index.html` | Montaje final (lo genera `tools/gen.py`): la chica, encuadres, música y efectos |
| `compositions/ins-01…06.html` | Los gráficos a pantalla completa (`tools/inserts/ins_01…06.py`) |
| `compositions/hook.html`, `outro.html` | Lo que va sobre ella: la etiqueta del gancho y el botón final con «Hasta el 30 de noviembre» |
| `compositions/captions.html` | Subtítulos blancos palabra a palabra, cortados por frases |
| `tools/align_fix.py` | Palabras de ElevenLabs Scribe (`tools/align/scribe_p.json`) → `tools/align/whisper_p.json` |
| `tools/edit.py` | Las mejores tomas (`SEGMENTS`), cortes propios de la grabación (`JUMPS`), pausas recortadas (`TIGHT`) y ventanas de los gráficos (`INSERTS`) → `edit.json` |
| `tools/libro_clip.py` | La animación del ebook entera (abre, pasa páginas, cierra) un poco más rápida, hasta «un euro», y recortada de su negro → `libro-ins05.webm` con transparencia |
| `tools/build_audio.py` | La música («musica v1»): el groove entra en «¿Por qué tan pronto?», unos 21 LU bajo la voz |
| `tools/common.py` | Sistema de diseño (el del VSL y los UGC: papel, azul Nawar, tarjetas, pastillas) y utilidades |
| `tools/sfx_impact.py` | Sintetiza el sonido de página del ebook |
| `tools/fetch_assets.sh` | Descarga la toma, la animación y la música del Drive y lo regenera todo |

## Cómo se rehace

```bash
bash tools/fetch_assets.sh          # (necesita ../vsl-formacion-nawar con sus assets)
npx hyperframes check
npx hyperframes render . --quality high -o renders/nawar-ugc4-v1-1.mp4
```

Un gráfico solo, para mirarlo: `python3 tools/gen.py --solo ins-03 --out /tmp/x` y `npx hyperframes snapshot` en `/tmp/x`.
