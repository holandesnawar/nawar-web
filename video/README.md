# Vídeos de Holandés Nawar (Remotion)

## Reel de la guía gratuita (`GuiaBases`)

Vertical 9:16 (1080×1920, 30 fps) con la toma IMG_6678 y el encuadre natural,
sin zoom. En cada paso de página se corta la parte en la que la mano llega y
coge la hoja: cada tramo empieza con la hoja ya en el aire, cae y se ve la
página nueva; también se cortan los ratos en que la mano ronda por abajo. Sin
texto encima (la línea `cta` va vacía; si se rellena, sale abajo con lo
entrecomillado resaltado).

1. Copia los clips originales en `public/clips/` (no se suben a git) y pásalos
   a 1080×1920 y 30 fps en `public/clips/hd/`:
   ```console
   ffmpeg -i public/clips/IMG_6678.MOV -an -vf "scale=1080:1920,fps=30" \
     -c:v libx264 -crf 16 -pix_fmt yuv420p public/clips/hd/IMG_6678.mp4
   ```
2. En `src/Root.tsx`, cada entrada de `clips` es un tramo:
   - `src`: archivo dentro de `public/clips/`
   - `from` / `to`: segundos del clip
   - `zoom`: 1 = encuadre natural (con más, se acerca anclado arriba)
   - `hold`: segundos que se queda quieto el último fotograma
   - `entry`: `"corte"` (lo normal), `"deslizar"` o `"fundido"`
   - `push`: acercamiento durante el tramo (1 = nada)
3. `npm run dev` para verlo y ajustarlo en Remotion Studio.
4. `npx remotion render GuiaBases out/guia-bases.mp4` para exportarlo.

`scripts/limpiar-pagina-04.py` limpia unas rayas de tinta de la tabla de la
página 04 en la toma IMG_6675 (no hace falta con IMG_6678).

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
