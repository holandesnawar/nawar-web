# Vídeos de Holandés Nawar (Remotion)

## Reel de la guía gratuita (`GuiaBases`)

Vertical 9:16 (1080×1920, 30 fps): tramos de los clips grabados pasando las
páginas de la guía y, abajo, la línea `Responde "BASES" y te la envío`.

1. Copia los clips originales en `public/clips/` (no se suben a git).
2. En `src/Root.tsx`, cada entrada de `clips` es un tramo:
   - `src`: nombre del archivo en `public/clips/`
   - `from` / `to`: segundos del clip original
   - `zoom`, `x`, `y`: encuadre para dejar fuera dedos y bordes
   - `entry`: `"corte"` (paso de página real), `"deslizar"` o `"fundido"`
3. `npm run dev` para verlo y ajustarlo en Remotion Studio.
4. `npx remotion render GuiaBases out/guia-bases.mp4` para exportarlo.

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
