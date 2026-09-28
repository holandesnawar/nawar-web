# Vídeos de Holandés Nawar (Remotion)

## Reel de la guía gratuita (`GuiaBases`)

Vertical 9:16 (1080×1920, 30 fps), vídeo a pantalla completa con la toma
IMG_6675: cada página se ve quieta con el encuadre natural y, entre página y
página, un instante de la hoja volando con zoom (así la mano que la sujeta
queda fuera). Los cortes se saltan el momento de coger la página y la espera.
Abajo, la línea `Responde "BASES" y te la envío`.

1. Copia los clips originales en `public/clips/` (no se suben a git) y pásalos
   a 1080×1920 y 30 fps en `public/clips/hd/`:
   ```console
   ffmpeg -i public/clips/IMG_6675.MOV -an -vf "scale=1080:1920,fps=30" \
     -c:v libx264 -crf 16 -pix_fmt yuv420p public/clips/hd/IMG_6675.mp4
   ```
2. Limpia las rayas de tinta de la tabla de la página 04 (crea `IMG_6675_fix.mp4`):
   ```console
   python3 scripts/limpiar-pagina-04.py
   ```
3. El final alarga el fotograma 845 (contraportada) en `IMG_6675_fin.mp4`:
   ```console
   ffmpeg -i public/clips/hd/IMG_6675_fix.mp4 -vf "select=eq(n\,845)" -frames:v 1 fin.png
   ffmpeg -loop 1 -framerate 30 -i fin.png -t 3 -c:v libx264 -crf 16 \
     -pix_fmt yuv420p public/clips/hd/IMG_6675_fin.mp4
   ```
4. En `src/Root.tsx`, cada entrada de `clips` es un tramo:
   - `src`: archivo dentro de `public/clips/`
   - `from` / `to`: segundos del clip
   - `zoom`: 1 = encuadre natural; 1.25 en los pasos de página
   - `entry`: `"corte"` (lo normal), `"deslizar"` o `"fundido"`
   - `push`: acercamiento durante el tramo (1 = nada)
5. `npm run dev` para verlo y ajustarlo en Remotion Studio.
6. `npx remotion render GuiaBases out/guia-bases.mp4` para exportarlo.

Los clips van sin sonido; la música se pone en Instagram/TikTok.

---

# Remotion video

<p align="center">
  <a href="https://github.com/remotion-dev/logo">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-dark.apng">
      <img alt="Animated Remotion Logo" src="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-light.gif">
    </picture>
  </a>
</p>

Welcome to your Remotion project!

## Commands

**Install Dependencies**

```console
npm i
```

**Start Preview**

```console
npm run dev
```

**Render video**

```console
npx remotion render
```

**Upgrade Remotion**

```console
npx remotion upgrade
```

## Docs

Get started with Remotion by reading the [fundamentals page](https://www.remotion.dev/docs/the-fundamentals).

## Help

We provide help on our [Discord server](https://discord.gg/6VzzNDwUwV).

## Issues

Found an issue with Remotion? [File an issue here](https://github.com/remotion-dev/remotion/issues/new).

## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
