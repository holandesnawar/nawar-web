# Voz automática para reels de vocabulario

Para los reels «¿Sabes decir ESTO en neerlandés?»: una cuadrícula de dibujos, cada uno con su palabra en una etiqueta
naranja, y las etiquetas se iluminan una tras otra. `reel_voz.py` le pone la voz al reel:

1. **detect** encuentra las etiquetas, lee las palabras por OCR y mide en qué fotograma se ilumina cada una.
2. **tts** hace dos generaciones con ElevenLabs:
   - la frase en español, «¿Sabes decir esto?»;
   - todas las palabras en neerlandés en una sola llamada (`/with-timestamps`).

   Cada palabra se recorta con los tiempos de sus letras, así todas tienen la misma voz y la misma entonación.
3. **mix** coloca la frase al principio y cada palabra cuando se ilumina su etiqueta.
   - La voz va un 10 % más lenta que como sale de ElevenLabs, sin cambiar el tono (Rubber Band).
   - Lleva una compresión suave y queda a −11 LUFS.
   - La música original del reel queda de fondo a un nivel fijo, con los picos en −19 dB como mucho: si viene más
     alta, baja; si ya está más baja, no se toca.
   - La imagen no se toca.

## Uso

```bash
export ELEVENLABS_API_KEY=...          # o un secreto de red para api.elevenlabs.io
python3 reel_voz.py all "Reel 3-3 - Vocab.mp4" --work trabajo/ --out "Reel 3-3 - Vocab (voz).mp4"
```

Por pasos, para revisar antes de gastar créditos:

```bash
python3 reel_voz.py detect REEL.mp4 --work trabajo/   # revisa trabajo/deteccion.jpg y trabajo/palabras.txt
python3 reel_voz.py tts --work trabajo/ --voz-es "Nombre" --voz-nl "Nombre"
python3 reel_voz.py mix REEL.mp4 --work trabajo/ --out REEL-voz.mp4
python3 reel_voz.py voices                            # las voces de tu cuenta
```

- **Palabras.** `trabajo/palabras.txt` tiene una palabra por línea, en el orden en que se iluminan. Si el OCR lee mal
  alguna, corrígela ahí y vuelve a lanzar `tts` y `mix`: el fichero manda sobre el OCR.
- **Pronunciación.** Si la voz pronuncia mal una palabra, escribe cómo debe sonar después de una barra:
  `het wc-papier | het weesee-papier`.
- **Repetir solo una palabra.** `python3 reel_voz.py tts --work trabajo/ --solo 11,17` genera de nuevo solo esas
  palabras (por su número en `palabras.txt`), en un fichero aparte. Usa la misma voz, modelo y velocidad que la toma,
  que quedan guardados en `trabajo/voz.json`. Las demás palabras y la frase se quedan como estaban, y luego basta con
  `mix`.
- **Voces y frase.** Se eligen con `--voz-es` / `--voz-nl` (nombre o id; o con las variables `ELEVENLABS_VOICE_ES` /
  `ELEVENLABS_VOICE_NL`). La frase se cambia con `--frase "¿Sabes decir esto en neerlandés?"`, el modelo con
  `--modelo` (por defecto `eleven_multilingual_v2`).
- **Volumen.** `--voz` es el volumen de la voz en LUFS: `--voz -9` más alta, `--voz -13` más baja. `--musica` es el dB
  máximo de los picos de la música: `--musica -22` la deja más baja y `--musica -16` más alta (nunca por encima de como
  viene en el reel). Con `--duck 3`, además, la música baja 3 dB cada vez que suena la voz.
- **Velocidad.** `--tempo 0.85` la hace más lenta y `--tempo 1` la deja como sale de ElevenLabs. Se aplica al mezclar,
  así que cambiarla no gasta créditos. El parámetro de velocidad de ElevenLabs (`--velocidad` en `tts`) no es fiable
  para esto: con 0,9 la frase salió más lenta, pero las palabras de la lista salieron más rápidas y solo se alargaron
  las pausas.
- **Colocación.** La primera palabra espera a que termine la frase. Las demás se empiezan a oír 0,12 s después de que
  se ilumine su etiqueta.
  - El momento se mide en el sonido, no en los tiempos de letra de ElevenLabs, que a veces se desvían ~0,1 s.
  - Cada corte empieza y acaba donde hay voz de verdad, así que no se come el principio ni el final de ninguna
    palabra.

Necesita ffmpeg, python3 con `numpy`, `opencv-python` y `pytesseract`, y tesseract con el idioma neerlandés
(`apt install tesseract-ocr tesseract-ocr-nld`).

## Probado con «Reel 3-3 - Vocab» (cuarto de baño, 20 palabras)

La detección encuentra las 20 etiquetas, lee bien todas las palabras (también «de föhn») y da los tiempos: una
etiqueta cada 3,0 s, desde 0,00 s hasta 56,93 s. Con la voz de Yair (española, elegida para las dos generaciones) se
entienden las 20 palabras y todos los artículos. «het douchegordijn» tiene una g algo suave. Escribirla de otras ocho
maneras no lo mejoró, y el reconocedor tampoco entiende mejor «scheermes» con voces holandesas nativas, así que se
quedan las tomas originales. La música del reel venía con picos en −13,7 dB (−25,9 LUFS): baja
5,3 dB y queda a unos −31 LUFS, unos 20 dB por debajo de la voz. El vídeo final mide −11,7 LUFS con picos de −1 dBTP.
