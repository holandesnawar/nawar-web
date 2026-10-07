# Anuncio UGC · Formación Nawar (Meta / TikTok Ads, 9:16) — proyecto HyperFrames

Anuncio de ~52 s en vertical (1080×1920) montado a partir de las dos tomas UGC del cliente: la chica de frente
(gancho y CTA) y de lado (tipo entrevista), alternadas frase a frase, con zooms de énfasis, subtítulos dinámicos y
motion graphics con el producto real (lecciones con el profe Paul, ejercicios, clases en directo, calendario de
eventos de la plataforma) y cierre hacia el formulario.

## Estructura

| Ruta | Qué es |
|---|---|
| `BRIEF.md` | Petición del cliente, público, reglas de marca |
| `STORYBOARD.md` | Plano a plano: qué aparece en cada frase y con qué movimiento |
| `edit.json` | El montaje: planos (toma, entrada, duración) y cada palabra con su tiempo en el vídeo |
| `index.html` | Montaje final (lo genera `tools/gen.py`): cortes, zooms, música y efectos |
| `compositions/gfx-NN.html` | Los gráficos de cada plano (uno por frase) |
| `compositions/captions.html` | Subtítulos palabra a palabra |
| `tools/edit.py` | Lista de cortes → `edit.json` (velocidad 1,05×, cortes en silencios revisados) |
| `tools/build_audio.py` | Música de fondo (el tema del VSL reeditado por compases) + tono de llamada |
| `tools/gen.py` | Genera `index.html`, los gráficos y los subtítulos desde `edit.json` |
| `tools/align/` | Alineación palabra a palabra de cada toma (forzada + Whisper) |

## Reconstruir y renderizar

```bash
bash tools/fetch_assets.sh            # tomas desde el Drive + medios de marca del VSL; genera todo
npx hyperframes check
npx hyperframes render . --quality high -o renders/nawar-ugc.mp4
```

Cambiar un corte: edita `EDL` en `tools/edit.py` y vuelve a ejecutar `python3 tools/edit.py && python3 tools/build_audio.py && python3 tools/gen.py`
— todos los gráficos y subtítulos se recolocan solos porque van atados a las palabras.
