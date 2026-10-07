# Anuncio UGC · Formación Nawar (Meta / TikTok Ads, 9:16) — proyecto HyperFrames

Anuncio de 50 s en vertical (1080×1920). **v2:** la chica habla siempre a cámara (solo la toma de frente, en un
plano continuo y sin cortes en su voz) y, cuando explica algo, la imagen corta a un gráfico a pantalla completa con
el diseño del VSL (fondo PAPER para el problema, NAWAR BLUE para la solución, producto real en ventana o en móvil)
y vuelve a ella. Subtítulos blancos y limpios, zooms de énfasis sobre su cara y cierre con ella a cámara y un bloque de matrícula hacia el formulario.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md` | Petición del cliente, público, reglas de marca |
| `STORYBOARD.md` | Plano a plano: qué aparece en cada frase y con qué movimiento |
| `edit.json` | El montaje: el plano de la chica, las ventanas de cada gráfico y cada palabra con su tiempo en el vídeo |
| `index.html` | Montaje final (lo genera `tools/gen.py`): la chica, su encuadre, música y efectos |
| `compositions/ins-NN.html` | Los gráficos a pantalla completa (uno por explicación) |
| `compositions/outro.html` | El bloque de matrícula del cierre (ella sigue en pantalla) |
| `compositions/captions.html` | Subtítulos palabra a palabra |
| `tools/edit.py` | Ventanas de los gráficos (`INSERTS`, atadas a palabras) → `edit.json` (velocidad 1,05×) |
| `tools/build_audio.py` | Música de fondo (el tema del VSL, calmado y a nivel constante) + tono de llamada |
| `tools/gen.py` | Genera `index.html`, los gráficos y los subtítulos desde `edit.json` |
| `tools/align/` | Alineación palabra a palabra de cada toma (forzada + Whisper) |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh            # tomas desde el Drive + medios de marca del VSL; genera todo
npx hyperframes check
npx hyperframes render . --quality high -o renders/nawar-ugc-v2.mp4
```

Cambiar cuándo entra o sale un gráfico: edita `INSERTS` en `tools/edit.py` y vuelve a ejecutar `python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py`
— todos los gráficos y subtítulos se recolocan solos porque van atados a las palabras.
