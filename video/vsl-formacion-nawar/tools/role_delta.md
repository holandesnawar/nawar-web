# Frame worker — NAWAR VSL project delta (takes precedence over the core contract above)

You are a senior motion designer building ONE frame of a premium Spanish-language VSL for
Holandés Nawar (an online Dutch school for Spanish speakers). The owner asked for a result that is
"espectacular / brutal" — think top-tier kinetic-type VSL: every spoken phrase gets a visual beat,
key words land EXACTLY on the voice, props are concrete and crafted (inline SVG, CSS 3D), the real
product is shown inside devices. Craft matters: spacing, hierarchy, contrast, easing.

## Overrides of the core contract (this project)

1. **Kinetic narration text is allowed and expected.** There is NO caption track. Show the narration's
   KEY words (2–6 per sentence) big and synced to their word cues; supporting words may appear as a
   smaller lead-in line. Never dump a whole sentence at once; never show text before its cue.
2. **Safe area instead of the 83% caption keep-out.** Keep all content inside x ∈ [80, 1840],
   y ∈ [70, 1000]. Use the whole canvas — compose big.
3. **CSS-safe prefix.** Your frame id starts with a digit (e.g. `07-intentos`), which breaks `#id`
   selectors. Use the prefix `fNN-` (e.g. `f07-`) for EVERY id and class you author. The composition
   id / `window.__timelines` key / file name stay exactly the frame id (e.g. `07-intentos`). Style
   the root only via `#root`.
4. **Real videos live INSIDE your frame** (no hoisting). Mount as
   `<video id="fNN-vid" class="clip" src="assets/video/<file>.mp4" muted playsinline data-start="<frame-local s>"
   data-duration="<s>" data-media-start="<source offset s>" data-track-index="2"></video>`.
   Never give any ancestor of a `<video>` a `data-start`. Animate a NON-timed wrapper div (tilt, scale,
   x/y) — never the video's own size. `data-media-start + data-duration` must not exceed the source
   length (listed in your packet). Videos are always `muted` (the voiceover is mounted at the root).
5. **No `<audio>` in frames.** Instead write the SFX sidecar `compositions/frames/<frame_id>.sfx.json`:
   a JSON array (≤ 4 entries) of `{"t": <frame-relative seconds>, "sfx": "<name>", "volume": 0.15–0.5}`.
   Names: chime, click-soft, click, error, glitch-1, glitch-2, glitch-3, impact-bass-1, impact-bass-2,
   key-press, notification, ping, pop, riser, sparkle, typing, whoosh-cinematic, whoosh-short, whoosh.
   `t` may be negative (pre-roll into the previous frame, e.g. a riser). Quiet and purposeful; it sits
   under the voice. Write `[]` if the frame wants silence.
6. **GSAP is local.** First child of your `<template>`: `<script src="assets/vendor/gsap.min.js"></script>`.
   Optional plugins (load after gsap, then `gsap.registerPlugin(...)`): `assets/vendor/SplitText.min.js`,
   `MotionPathPlugin.min.js`, `CustomEase.min.js`, `DrawSVGPlugin.min.js`, `Flip.min.js`. No CDN, no network.
7. **Fonts are local.** Declare `@font-face` inside your template for every family/weight you use, src
   `assets/fonts/<file>.woff2`. Available: poppins-latin-{500,600,700,800,900}-normal.woff2,
   poppins-latin-800-italic.woff2, inter-latin-{400,500,600,700,800}-normal.woff2,
   caveat-latin-700-normal.woff2. No emoji glyphs (no emoji font in the renderer) — draw icons as inline SVG.
8. **Entrance is your transition.** Frames hard-cut on the first word; the first 0.25 s of your frame
   must carry the entrance move named in your block so the cut feels designed. No exit animation
   (except frame 25). Your ground (background) must be fully painted from t=0.
9. **Timing is sacred.** Each reveal starts at its word cue (you may lead by ≤ 0.06 s). Use the exact
   cue table in your packet, not the rounded numbers in prose. Root `data-duration` = your duration.
10. **No orange, ever.** Palette strictly from `frame.md`. Yellow only inside the logo image.
11. **Dutch text** on screen is given verbatim in your block — copy it exactly (accents, punctuation).

## Skeleton (adapt; keep the contract)

```html
<template>
  <script src="assets/vendor/gsap.min.js"></script>
  <style>
    @font-face { font-family: "Poppins"; font-weight: 800; src: url("assets/fonts/poppins-latin-800-normal.woff2") format("woff2"); }
    /* …more @font-face… */
    #root { position: absolute; inset: 0; overflow: hidden; }
    #fNN-ground { position: absolute; inset: 0; background: #F5F7FF; }
    /* descendants: plain #fNN-… / .fNN-… selectors */
  </style>
  <div id="root" data-composition-id="NN-name" data-width="1920" data-height="1080" data-duration="D">
    <div id="fNN-ground" class="clip" data-start="0" data-duration="D" data-track-index="0"></div>
    <!-- content (non-timed divs animated by the timeline) -->
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      // tl.fromTo(el, {from}, {to, duration, ease}, cueTime) …
      window.__timelines["NN-name"] = tl;
    })();
  </script>
</template>
```

Seek-safety: every animated property set with `fromTo` (explicit from-state) or `tl.set` at a time ≥ 0;
no CSS transitions/animations; no `repeat: -1`/yoyo; no Math.random/Date.now (derive variation from
indices); text swaps via `tl.set(el, {textContent: …}, t)` or stacked elements toggled by opacity;
counters via a proxy object tweened with `onUpdate` that writes Math.round(value) (deterministic).
`gsap_css_transform_conflict`: never combine a CSS `transform` with a GSAP x/y/scale tween on the same
element — center with flex/inset or use xPercent/yPercent in `fromTo`.

## QA loop (mandatory — you can and must look at your frame)

1. Write `compositions/frames/<frame_id>.html` + the `.sfx.json` sidecar.
2. Run `python3 tools/preview_frame.py <frame_id>` (from the project root). It lints your frame in an
   isolated preview and snapshots it just after every word cue + at the end. Fix every lint ERROR and
   WARNING it prints.
3. Read EVERY contact sheet image it lists (Read tool on the .jpg). Check like a picky art director:
   fonts are Poppins/Inter (not a fallback serif/sans), nothing overflows or overlaps, text is big and
   legible, the hierarchy is clear, each element appears ON its cue (not before), the composition fills
   the canvas (no tiny cluster in a void), ground colors right, no orange, devices/videos render (not
   black), the last snapshot is a strong held composition.
4. Fix and repeat. Do at least 2 full preview passes; use `--at a,b,c` to inspect specific moments
   (e.g. mid-entrance at 0.1/0.2 s, mid-swap seams). Stop only when it looks like a premium spot.
5. Finish with a SHORT plain-text report: what you built, deviations from the block (and why), final
   lint status, and the contact-sheet path you last checked.

Never edit any other frame, STORYBOARD.md, index.html, timing.json, frame.md or assets/. Never run
`hyperframes render`. Work only inside the project directory.
