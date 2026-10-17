# Limpia unas rayas de tinta de la tabla de la página 04 en IMG_6675 y escribe
# IMG_6675_fix.mp4. Sigue la tabla fotograma a fotograma (la cámara se mueve) y
# repinta con el fondo de la propia tabla solo la zona entre columnas, sin texto.
# Solo actúa cuando la tabla se ve limpia (no mientras pasa la hoja por encima).
#   pip install opencv-python-headless numpy imageio-ffmpeg
#   python3 scripts/limpiar-pagina-04.py
import cv2, numpy as np, subprocess, imageio_ffmpeg, sys, os
HD = os.path.join(os.path.dirname(__file__), "..", "public", "clips", "hd")
SRC = os.path.join(HD, "IMG_6675.mp4")
DST = os.path.join(HD, "IMG_6675_fix.mp4")
T0, T1 = 16.2, 18.8                              # tramo con la página 04 a la vista
_c = cv2.VideoCapture(SRC); _c.set(cv2.CAP_PROP_POS_FRAMES, 525); ref = _c.read()[1]   # 17.5 s
PX0, PY0, PX1, PY1 = 200, 900, 1020, 1140        # zona de seguimiento (tabla + textos)
refp = cv2.cvtColor(ref[PY0:PY1, PX0:PX1], cv2.COLOR_BGR2GRAY).astype(np.float32)
win = cv2.createHanningWindow(refp.shape[::-1], cv2.CV_32F)
# zonas sin texto a repintar (coordenadas del fotograma de referencia)
RECTS = [(382, 965, 778, 1100), (824, 1010, 946, 1062)]
mask_ref = np.zeros(ref.shape[:2], np.float32)
for x0, y0, x1, y1 in RECTS: mask_ref[y0:y1, x0:x1] = 1
mask_ref = cv2.GaussianBlur(mask_ref, (0, 0), 2)
cap = cv2.VideoCapture(SRC); fps = cap.get(cv2.CAP_PROP_FPS)
w, h = int(cap.get(3)), int(cap.get(4))
dry = len(sys.argv) > 1   # con cualquier argumento solo muestra el seguimiento
proc = None if dry else subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
    "-s", f"{w}x{h}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", DST], stdin=subprocess.PIPE)
i = 0; log = []
while True:
    ok, f = cap.read()
    if not ok: break
    t = i / fps
    if T0 <= t <= T1:
        cur = cv2.cvtColor(f[PY0:PY1, PX0:PX1], cv2.COLOR_BGR2GRAY).astype(np.float32)
        (dx, dy), resp = cv2.phaseCorrelate(refp, cur, win)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        # ¿la tabla se ve limpia (sin la hoja volando encima)? comparar con la referencia alineada
        refa = cv2.warpAffine(ref, M, (w, h))
        a = cv2.cvtColor(f[PY0:PY1, PX0:PX1], cv2.COLOR_BGR2GRAY).astype(np.float32)
        b = cv2.cvtColor(refa[PY0:PY1, PX0:PX1], cv2.COLOR_BGR2GRAY).astype(np.float32)
        ncc = float(np.corrcoef(a.ravel(), b.ravel())[0, 1])
        applied = ncc > 0.85
        if applied:
            m = cv2.warpAffine(mask_ref, M, (w, h))[..., None]
            ys, xs = np.where(m[..., 0] > 0.01); ya, yb, xa, xb = ys.min() - 30, ys.max() + 30, xs.min() - 30, xs.max() + 30
            reg = f[ya:yb, xa:xb]
            bg = cv2.GaussianBlur(cv2.medianBlur(reg, 41), (0, 0), 4).astype(np.float32)
            # grano suave para que no quede "plano"
            noise = np.random.default_rng(i).normal(0, 1.2, bg.shape).astype(np.float32)
            mm = m[ya:yb, xa:xb]
            f[ya:yb, xa:xb] = np.clip(reg * (1 - mm) + (bg + noise) * mm, 0, 255).astype(np.uint8)
        log.append((round(t, 2), round(dx, 1), round(dy, 1), round(ncc, 3), applied))
    if proc: proc.stdin.write(f.tobytes())
    i += 1
if proc: proc.stdin.close(); proc.wait()
print("fotogramas", i); print("aplicado en", sum(1 for l in log if l[4]), "de", len(log))
for l in log[::6]: print(l)
