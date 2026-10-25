# Voz automática para reels de vocabulario

Para los reels «¿Sabes decir ESTO en neerlandés?»: una cuadrícula de dibujos, cada uno con su palabra en una etiqueta
naranja, y las etiquetas se iluminan una tras otra. `reel_voz.py` le pone la voz al reel:

1. **detect** encuentra las etiquetas, lee las palabras por OCR y mide en qué fotograma se ilumina cada una.
2. **tts** hace dos generaciones con ElevenLabs:
   - la frase en español, «¿Sabes decir esto?»;
   - todas las palabras en neerlandés en una sola llamada (`/with-timestamps`).

   Cada palabra se recorta con los tiempos de sus letras, así todas tienen la misma voz y la misma entonación.
3. **mix** coloca la frase al principio y cada palabra cuando se ilumina su etiqueta. La música original del reel queda
   de fondo a un nivel fijo, con los picos en −16 dB, como al bajarla en el editor. La voz queda a −16 LUFS. La imagen
   no se toca.

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
- **Voces y frase.** Se eligen con `--voz-es` / `--voz-nl` (nombre o id; o con las variables `ELEVENLABS_VOICE_ES` /
  `ELEVENLABS_VOICE_NL`). La frase se cambia con `--frase "¿Sabes decir esto en neerlandés?"`, el modelo con
  `--modelo` (por defecto `eleven_multilingual_v2`).
- **Música.** `--musica -18` la deja más baja y `--musica -14` más alta (es el dB de sus picos). Con `--duck -3`, además,
  baja 3 dB cada vez que suena la voz.
- **Colocación.** La primera palabra espera a que termine la frase. Las demás entran 0,1 s después de que se ilumine su
  etiqueta.

Necesita ffmpeg, python3 con `numpy`, `opencv-python` y `pytesseract`, y tesseract con el idioma neerlandés
(`apt install tesseract-ocr tesseract-ocr-nld`).

## Probado con «Reel 3-3 - Vocab» (cuarto de baño, 20 palabras)

La detección encuentra las 20 etiquetas, lee bien todas las palabras (también «de föhn») y da los tiempos: una
etiqueta cada 3,0 s, desde 0,00 s hasta 56,93 s.
