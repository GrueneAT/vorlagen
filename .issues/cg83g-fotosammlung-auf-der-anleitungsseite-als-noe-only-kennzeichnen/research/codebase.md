# Raw research — CODEBASE

**Issue:** cg83g-fotosammlung-auf-der-anleitungsseite-als-noe-only-kennzeichnen
**Date:** 2026-08-26
**Worktree:** `/Users/florianmotlik/Code/GrueneAT/web-apps/vorlagen/.worktrees/cg83g-fotosammlung-auf-der-anleitungsseite-als-noe-only-kennzeichnen`

## Relevant files

| File | Purpose | Last touched | Relevance |
|------|---------|--------------|-----------|
| `site/src/content/anleitung/06-fotosammlung.md` | The step to change | `8186814` (POC: Anschnitt, Impressum-Position, …) | THE edit target |
| `site/src/content.config.ts` | zod schema of the `anleitung` collection | — | Determines whether a schema change is needed (it is NOT) |
| `site/src/pages/anleitung/index.astro` | Renders all steps | `cdb585b`, `c180fcb` | Shows how `callout`/`title`/`links` are consumed |
| `site/src/styles/app.css` (L1093–1131) | `.app-step*` styles | `65bb4ef` | Explains what `callout:` does visually |
| `site/src/content/anleitung/02-schriften-installieren.md` | The ONE existing `callout: warn` step | `cdb585b` | The precedent to copy |
| `site/src/components/VideoGrid.astro` (L29) | The ONE existing `gat-callout--info` on this page | `120c54e` | The precedent for an *info*-level Hinweis |
| `site/src/layouts/Base.astro` (L12) | Loads the DS via CDN | — | Confirms `gat-callout` is available, no vendoring |

## Key finding: the schema already supports a callout — no schema change needed

`site/src/content.config.ts` L67–88 declares `callout: z.enum(['info','warn']).optional()`
on the `anleitung` collection, and `site/src/pages/anleitung/index.astro` L60 turns it into
`class="gat-callout gat-callout--<value> app-step"` on the whole `<section>`.

So the entire issue is satisfiable by editing **one Markdown file** — `title`, add
`callout:`, rewrite the body. `content.config.ts` and `index.astro` stay untouched.

## Interfaces

```ts
// site/src/content.config.ts — anleitung collection (L67–88)
const anleitung = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/anleitung' }),
  schema: z.object({
    order: z.number(),
    title: z.string(),
    // Optional: rendert den Abschnitt als Design-System-Callout statt als
    // schlichten Block (z.B. der Schriften-Hinweis).
    callout: z.enum(['info', 'warn']).optional(),
    links: z.array(z.object({
      label: z.string(),
      href: z.string(),
      kind: z.enum(['internal', 'download', 'external']),
    })).optional(),
  }),
});
export const collections = { templates, experiments, anleitung };
```

```astro
// site/src/pages/anleitung/index.astro — the step render (L20–33, L57–84)
const sections = (await getCollection('anleitung')).sort((a, b) => a.data.order - b.data.order);
const rendered = await Promise.all(
  sections.map(async s => ({ data: s.data, Content: (await render(s)).Content }))
);
const hrefFor = (l: { href: string; kind: string }) =>
  l.kind === 'external' ? l.href : url(l.href);

<section class={data.callout ? `gat-callout gat-callout--${data.callout} app-step` : 'app-step'}>
  <h3 class="gat-headline app-step__title">{data.title}</h3>   {/* plain text, Astro-escaped */}
  <div class="app-step__body"><Content /></div>                {/* Markdown body */}
  <ul class="app-step__links"> … {l.kind === 'download' ? '↓' : l.kind === 'external' ? '↗' : '→'} … </ul>
</section>
```

```css
/* site/src/styles/app.css — L1093–1131 */
.app-steps { display: grid; gap: 1.25rem; margin-top: 1.5rem; }
/* Ohne .gat-callout-Variante: weiße Karte wie im restlichen Grid. */
.app-step:not([class*='gat-callout']) {
  background: white; border-radius: var(--gat-web-radius-card);
  box-shadow: var(--gat-web-shadow); padding: 1.25rem;
}
h3.app-step__title { margin: 0 0 0.5rem 0; font-size: 1.1rem; }
.app-step__body > :first-child { margin-top: 0; }
.app-step__body > :last-child  { margin-bottom: 0; }
.app-step__links { list-style: none; margin: .9rem 0 0 0; padding: 0; display: grid; gap: .4rem; }
.app-step__link  { display: inline-flex; align-items: baseline; gap: .45rem; font-weight: bold; }
```

Consequence of the `:not([class*='gat-callout'])` guard: a step **with** `callout:` loses
the white card + shadow and instead gets the DS callout background + 4px left border.
That is intended and already visible on step 02.

## Current content of the edit target

```markdown
<!-- site/src/content/anleitung/06-fotosammlung.md — CURRENT -->
---
order: 6
title: "Fotosammlung für eure Druckwerke"
links:
  - label: "Zur Fotosammlung (GGS NÖ, Login nötig)"
    href: "https://ggs-noe.gruene.at/fotosammlung-fuer-social-media-und-druckwerke/"
    kind: external
---

Im Gemeindegruppenservice findet ihr Bilder, die über Adobe Stock erworben
wurden und die ihr somit für Social-Media-Beiträge oder eure Druckwerke
verwenden könnt.
```

## The one existing callout step (the precedent)

```markdown
<!-- site/src/content/anleitung/02-schriften-installieren.md -->
---
order: 2
title: "2. Schritt: die richtigen Schriftarten installieren"
callout: warn
links: [ … ]
---

Damit die Vorlage korrekt dargestellt wird, müssen die benötigten Schriften
**vor dem Öffnen** des Dokuments heruntergeladen … installiert sein. …

Die Vorlagen sind in **Gotham Narrow** … gesetzt. …

**Bitte wendet euch dafür an euer Landesbüro.**
```

Pattern: an own bold single-sentence paragraph at the end carries the call-to-action.
Commit `65bb4ef` ("Landesbuero-Hinweis im Schrift-Callout hervorheben") applied the same
idea to the *template detail pages*, not to this file — it added
`.app-font-notice__action` in `app.css` and split the paragraph in
`site/src/pages/templates/[...id].astro`. **The anleitung page never got a custom
highlight class**; there the plain `**bold**` paragraph is the whole pattern.

## Tone of steps 01–05 (verbatim excerpts)

- 01: "Scribus ist kostenlos und läuft unter Windows, macOS und Linux. **Ladet euch** die aktuelle Version herunter und **installiert sie**, bevor ihr eine Vorlage öffnet."
- 02: "Damit die Vorlage korrekt dargestellt wird, **müssen** die benötigten Schriften **vor dem Öffnen** … installiert sein." / "**Bitte wendet euch dafür an euer Landesbüro.**"
- 03: "In der Galerie **findet ihr** Flyer, Falzflyer … **Wählt** die passende Vorlage, **ladet** die Scribus-Datei … herunter und **öffnet sie** in Scribus."
- 04: "**Ladet** `eci_offset_2009.zip` herunter und **installiert** den Farbraum … **Bitte stellt jedoch sicher**, dass ihr im Vorfeld mit der Druckerei abklärt …"
- 05: "Um Fehler zu vermeiden, **solltet ihr** einige Dinge beachten … **Arbeitet die Checkliste bitte sorgfältig durch.**"

House style, distilled:
- Second person plural, **"ihr"**, never "du" and never "Sie".
- Imperative sentences ("Ladet", "Wählt", "Arbeitet …durch").
- `**Bold**` for the one thing that must not be missed; sparingly, one per section.
- Em dash `—` (U+2014) as the aside separator; real umlauts throughout.
- Body lines hard-wrapped at roughly 78 columns.
- Titles: steps 01–03 are numbered ("N. Schritt: …"), 04–06 are unnumbered topical
  titles ("Vor dem Erstellen der Druckdatei: Farbraum", "Checkliste vor dem Druck",
  "Fotosammlung für eure Druckwerke"). So step 06 has NO numbering prefix to preserve.

## Reusable components (do not rebuild)

| Need | Already exists | Where |
|------|----------------|-------|
| Highlighted hint box on a step | `callout: info \| warn` frontmatter field | `content.config.ts` L74 |
| The callout CSS | `.gat-callout`, `.gat-callout--info/--warn` | DS via CDN, `Base.astro` L12 |
| Rendering the modifier onto the step | already implemented | `index.astro` L60 |
| "Aufforderungssatz" emphasis | plain `**bold**` paragraph | `02-schriften-installieren.md` |
| External link w/ ↗ + `target=_blank` + `rel=noopener` | `kind: external` | `index.astro` L69–78 |

## Potential conflicts

- **None in code.** No other file references the Fotosammlung step. Verified:
  `grep -rn "Fotosammlung" site/src docs README.md` → only `06-fotosammlung.md`.
- The heading text is not used as an anchor / TOC entry anywhere, so renaming the
  title breaks no link (`/anleitung/` has no in-page nav).
- No open PR touches `site/src/content/anleitung/` — last two commits to that dir are
  `cdb585b` (creation) and `8186814`.

## Rendered output today (from `site/dist/anleitung/index.html`, build verified)

```html
<section class="app-step">
  <h3 class="gat-headline app-step__title">Fotosammlung für eure Druckwerke</h3>
  <div class="app-step__body"><p>Im Gemeindegruppenservice findet ihr Bilder, …</p></div>
  <ul class="app-step__links"><li><a href="https://ggs-noe.gruene.at/…" class="app-step__link"
    target="_blank" rel="noopener noreferrer"><span aria-hidden="true">↗</span>
    Zur Fotosammlung (GGS NÖ, Login nötig)</a></li></ul>
</section>
```

vs. step 02 today:

```html
<section class="gat-callout gat-callout--warn app-step"> … </section>
```
