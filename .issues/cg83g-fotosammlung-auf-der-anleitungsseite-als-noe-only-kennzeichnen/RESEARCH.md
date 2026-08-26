# Research: Fotosammlung auf der Anleitungsseite als NÖ-only kennzeichnen

**Researched:** 2026-08-26
**Issue:** cg83g-fotosammlung-auf-der-anleitungsseite-als-noe-only-kennzeichnen
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)
No CONTEXT.md found for this issue — no `issue:discuss` run happened. ISSUE.md
itself carries an explicit "Constraints" section, which is treated with the
same authority:

- Reine Content-Änderung, keine neuen Komponenten nötig
- Conventional Commit, keine Werkzeug-Attribution
</user_constraints>

## Summary

Diese Änderung ist ein reiner Content-Fix in einer einzigen Datei:
`site/src/content/anleitung/06-fotosammlung.md`. Das Frontmatter-Schema der
`anleitung`-Collection (`site/src/content.config.ts`) besitzt bereits ein
optionales `callout: 'info' | 'warn'`-Feld, und `index.astro` rendert es
bereits als `gat-callout gat-callout--<wert>`-Klasse auf die `<section>`. Es
gibt also **kein Schema, keine Astro- oder CSS-Änderung** zu leisten — die
komplette Aufgabe ist: Titel umbenennen, `callout: info` setzen, den Fließtext
um den NÖ-/GGS-Login-Hinweis erweitern.

Ein Präzedenzfall existiert bereits auf derselben Seite: Schritt 02
(„Schriften installieren") nutzt `callout: warn`, um auf eine Lizenz-/
Landesbüro-Einschränkung hinzuweisen — stilistisch das nächstliegende Vorbild,
nicht nur strukturell (`callout:`-Feld), sondern auch inhaltlich (Hinweis auf
eine Einschränkung/Zugangsvoraussetzung). Für den Fotosammlungs-Hinweis passt
semantisch `callout: info` besser als `warn`: `warn` (blassgelb/dunkles Gelb,
via `#fdf3d2` / `#b78a1c`) signalisiert im Design-System eine Warnung/Achtung
("etwas kann schiefgehen, wenn ihr das ignoriert"), während der
NÖ-Only-Hinweis eine reine Zugangs-Information ist, kein Fehlerrisiko. `info`
nutzt eigene DS-Variablen (`--gat-web-callout-info-bg/-border/-text`, verifiziert
über die live gehostete `design-system.css`) und ist damit visuell klar von
`warn` unterscheidbar.

Der Tonfall der Schritte 01–05 ist konsistent: 2. Person Plural ("ihr"),
Imperativ, ein `**bold**`-Satz pro Abschnitt für die eine Handlung, die nicht
übersehen werden darf, Halbgeviertstrich `—`, korrekte Umlaute. Titel 04–06
sind unnummeriert-thematisch ("Fotosammlung für eure Druckwerke (nur NÖ)" o.ä.
bleibt in dieser Form, keine "N. Schritt:"-Präfix nötig). Es gibt keine
anderen Code- oder Doku-Referenzen auf "Fotosammlung" im Repo — die Änderung
ist vollständig isoliert.

**Primary recommendation:** Nur `06-fotosammlung.md` ändern — Titel um
„(nur NÖ)"-Hinweis ergänzen, `callout: info` im Frontmatter setzen (nach dem
Vorbild von `callout: warn` in Schritt 02), Body um einen expliziten Satz zum
GGS-NÖ-Login/Zugangsbeschränkung erweitern, `npm run build` in `site/`
ausführen und das gerenderte HTML stichprobenartig prüfen.

## Codebase Analysis

### Relevant Code

| File | Purpose | Last Modified | Relevance |
|------|---------|----------------|-----------|
| `site/src/content/anleitung/06-fotosammlung.md` | Der zu ändernde Anleitungsschritt | `8186814` | DAS Edit-Ziel |
| `site/src/content.config.ts` | Zod-Schema der `anleitung`-Collection (L67–90) | — | Bestätigt: `callout` existiert bereits, keine Schemaänderung nötig |
| `site/src/pages/anleitung/index.astro` | Rendert alle Schritte inkl. `callout`-Klasse | — | Keine Änderung nötig — Konsum des Frontmatters bereits generisch |
| `site/src/styles/app.css` (L1093–1131) | `.app-step*`-Styles | `65bb4ef` | Erklärt visuellen Effekt von `callout:` (weiße Karte vs. DS-Callout-Look) |
| `site/src/content/anleitung/02-schriften-installieren.md` | Einziger existierender `callout: warn`-Schritt | `cdb585b` | Stilistisches Vorbild für Ton + Frontmatter-Nutzung |
| `site/src/layouts/Base.astro` (L12) | Lädt Design-System per CDN (`design-system.gruene.at/design-system.css`) | — | Bestätigt: kein Vendoring, `gat-callout` ist bereits verfügbar |

Alle Aussagen der vorherigen (abgebrochenen) Recherche in
`research/codebase.md` wurden gegen die aktuellen Dateien nachgeprüft und
sind korrekt: Schema, Astro-Rendering, CSS-Regeln, Ist-Zustand von
`06-fotosammlung.md`, Ton der Schritte 01–05, Isoliertheit der Datei
(keine weiteren Referenzen auf „Fotosammlung" im Repo, per
`grep -rn "Fotosammlung"` verifiziert).

### Interfaces

<interfaces>
// site/src/content.config.ts — anleitung collection (L67–90)
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
      // 'internal' -> BASE_URL-Präfix, 'download' -> interner Pfad + Pfeil,
      // 'external' -> unverändert, öffnet in neuem Tab.
      kind: z.enum(['internal', 'download', 'external']),
    })).optional(),
  }),
});
export const collections = { templates, experiments, anleitung };

// site/src/pages/anleitung/index.astro — Step-Rendering (Ausschnitt)
const sections = (await getCollection('anleitung')).sort((a, b) => a.data.order - b.data.order);
const rendered = await Promise.all(
  sections.map(async s => ({ data: s.data, Content: (await render(s)).Content }))
);
// <section class={data.callout ? `gat-callout gat-callout--${data.callout} app-step` : 'app-step'}>
//   <h3 class="gat-headline app-step__title">{data.title}</h3>
//   <div class="app-step__body"><Content /></div>
//   <ul class="app-step__links"> ... </ul>
// </section>
</interfaces>

### Aktueller Inhalt der Zieldatei (vor der Änderung)

```markdown
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

### Stilistisches Vorbild — Schritt 02 (callout: warn)

```markdown
---
order: 2
title: "2. Schritt: die richtigen Schriftarten installieren"
callout: warn
links: [ ... ]
---

Damit die Vorlage korrekt dargestellt wird, müssen die benötigten Schriften
**vor dem Öffnen** des Dokuments heruntergeladen und auf eurem Rechner
installiert sein. ...

**Bitte wendet euch dafür an euer Landesbüro.**
```

Muster: ein eigener, knapper `**bold**`-Satz am Ende trägt die zentrale
Handlungsaufforderung/Einschränkung. Für Schritt 06 heißt das analog: ein
eigener fett gesetzter Satz, der klarstellt, dass nur Gruppen der Grünen
Niederösterreich Zugang haben.

### Reusable Components (nicht neu bauen)

| Bedarf | Existiert bereits | Wo |
|--------|--------------------|----|
| Hervorgehobene Hinweisbox pro Schritt | `callout: info \| warn` im Frontmatter | `content.config.ts` L74 |
| DS-Callout-CSS (Farbvarianten) | `.gat-callout`, `.gat-callout--info`, `.gat-callout--warn` | Design-System via CDN (`Base.astro` L12) |
| Rendering des Modifiers | bereits implementiert | `index.astro` |
| „Aufforderungssatz"-Emphase | schlichter `**bold**`-Absatz | `02-schriften-installieren.md` |
| Externer Link mit ↗ + `target=_blank` + `rel=noopener` | `kind: external` | `index.astro` |

### Potential Conflicts

Keine im Code. `grep -rn "Fotosammlung" site/src` liefert nur Treffer in
`06-fotosammlung.md`. Der Titeltext wird nirgends als Anker/TOC-Eintrag
referenziert — `/anleitung/` hat keine In-Page-Navigation. Kein offener PR
berührt `site/src/content/anleitung/`.

## Standard Stack

Kein neuer Stack-Bedarf. Das Repo nutzt Astro 5 (Content Collections, Zod-
Schema) und lädt das Grüne-AT-Design-System per CDN
(`https://design-system.gruene.at/design-system.css`, verifiziert live —
enthält `.gat-callout`, `.gat-callout--info`, `.gat-callout--warn`). Beides
ist bereits vollständig im Projekt verdrahtet; für dieses Issue wird nichts
Neues installiert oder verlinkt.

| Library/System | Version | Zweck | Confidence |
|-----------------|---------|-------|------------|
| Astro | ^5.0.0 (`site/package.json`) | Content Collections, Rendering | HIGH (codebase) |
| Grüne-AT Design System | live, via CDN | `.gat-callout` Varianten `info`/`warn` | HIGH (live CSS gefetcht und verifiziert) |

## Don't Hand-Roll

| Problem | Nicht bauen | Stattdessen | Warum |
|---------|-------------|--------------|-------|
| Hervorgehobene Hinweisbox | Eigene CSS-Klasse/Komponente | `callout: info` im Frontmatter | Existiert bereits, Issue verlangt ausdrücklich „keine neuen Komponenten" |
| Handlungssatz hervorheben | Neue `.app-*-notice`-Klasse (wie in `templates/[...id].astro`, Commit `65bb4ef`) | Einfacher `**bold**`-Absatz im Markdown-Body | Das ist das Muster, das auf der Anleitungsseite selbst tatsächlich verwendet wird (Schritt 02); die `.app-font-notice__action`-Klasse ist Template-Detail-Seiten vorbehalten und dort nicht referenziert |

## Architecture Patterns

### Recommended Approach

1. `title` in `06-fotosammlung.md` erweitern, z. B.
   `"Fotosammlung für eure Druckwerke (nur NÖ)"` — sichtbar ohne Klick, wie
   in den Akzeptanzkriterien gefordert.
2. `callout: info` ins Frontmatter setzen (nach dem `title`, vor `links`,
   analog zur Position von `callout: warn` in Schritt 02).
3. Body-Text um einen zusätzlichen, klar hervorgehobenen Satz ergänzen, der
   erklärt: Zugang läuft über den GGS NÖ, benötigt ein Login der Grünen
   Niederösterreich, Gruppen außerhalb NÖs haben keinen Zugriff. Ton wie
   Schritt 02: ein eigener `**bold**`-Satz für den zentralen Hinweis.
4. Link-Label kann unverändert bleiben (`"Zur Fotosammlung (GGS NÖ, Login
   nötig)"`) — der Hinweis MUSS laut Akzeptanzkriterium im Fließtext stehen,
   nicht nur im Label.
5. `cd site && npm run build` ausführen, danach `dist/anleitung/index.html`
   stichprobenartig prüfen (`grep -A3 "gat-callout--info" dist/anleitung/index.html`),
   dass der Callout korrekt gerendert wird.

### Anti-Patterns to Avoid

- **Neue CSS-Klasse/Komponente einführen:** Verstößt gegen den expliziten
  Constraint „keine neuen Komponenten nötig". `.app-font-notice__action`
  (Commit `65bb4ef`) ist bewusst nur für Template-Detail-Seiten gebaut — hier
  nicht kopieren.
- **`content.config.ts` oder `index.astro` anfassen:** Nicht nötig, das
  Rendering ist bereits generisch für `callout` implementiert.
- **Nummerierungspräfix „6. Schritt:" ergänzen:** Bricht mit der bestehenden
  Konvention (04–06 sind unnummeriert-thematisch betitelt).

## Common Pitfalls

### Callout-Variante falsch wählen

**What goes wrong:** `callout: warn` statt `info` verwenden (naheliegend,
weil es der einzige existierende Präzedenzfall ist), obwohl der Hinweis kein
Fehlerrisiko, sondern eine reine Zugangsinformation ist.
**Why it happens:** Schritt 02 ist das einzige Vorbild im Repo und nutzt
`warn`.
**How to avoid:** `info` verwenden — semantisch korrekt für einen reinen
Hinweis ohne Warncharakter; visuell im DS klar von `warn` unterscheidbar
(eigene `--gat-web-callout-info-*`-Variablen statt `#fdf3d2`/`#b78a1c`).
**Warning signs:** Falls im PR-Review die Farbe/Konnotation als „zu
alarmierend" für eine reine Info auffällt.

### Hinweis nur im Link-Label statt im Fließtext

**What goes wrong:** Nur das bestehende Link-Label „(GGS NÖ, Login nötig)"
belassen und den Hinweis nicht in den Body-Text aufnehmen — genau der
Ist-Zustand, den das Issue kritisiert.
**Why it happens:** Das Label existiert schon und wirkt informativ genug.
**How to avoid:** Akzeptanzkriterium explizit prüfen: „Der Login-Hinweis
steht im Text, nicht nur im Link-Label."
**Warning signs:** Body-Diff enthält keine neue Erwähnung von „NÖ" oder
„Login".

### Build nicht verifiziert

**What goes wrong:** Nur die Markdown-Datei ändern, ohne `astro build`
laufen zu lassen — Zod-Schema-Validierung (`callout: z.enum(['info','warn'])`)
würde einen Tippfehler im Wert sonst erst spät auffallen.
**How to avoid:** `cd site && npm run build` (Akzeptanzkriterium „Build läuft
durch").

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|--------------|-----------|---------|----------|
| Node.js/npm | `astro build` | im Container vorhanden (Standard für dieses Repo) | siehe `site/package.json` (`astro ^5.0.0`) | — |
| `astro check` | optionaler Typecheck | `npm run check` in `site/package.json` definiert | — | nicht zwingend für dieses Issue, `build` reicht |

Build-/Testkommandos (aus `site/package.json`):
```
npm run dev      # astro dev
npm run build    # astro build
npm run preview  # astro preview
npm run check    # astro check
```

## Project Constraints (from CLAUDE.md)

Aus `/Users/florianmotlik/Code/GrueneAT/web-apps/CLAUDE.md` (workspace-weit,
gilt für dieses Repo unter `/workspace/vorlagen`):

- **Immer im Worktree arbeiten** — niemals direkt am `main`-Checkout ändern.
  Dieser Auftrag läuft bereits im korrekten Worktree
  (`.worktrees/cg83g-...`); es wurde bereits per `issue-cli` erstellt.
- **Kein Vendoring von Drittabhängigkeiten** — bestätigt bereits eingehalten:
  Design-System kommt per `<link>` von `design-system.gruene.at`, keine
  lokale Kopie nötig oder zu erstellen.
- **Keine Werkzeug-Attribution** in Commits/Code/Kommentaren — gilt auch für
  den finalen Commit dieses Issues.

Aus `/root/.config/claude/CLAUDE.md` (Container-weit):
- Keine AI-Attribution in Commits/Code (deckt sich mit obigem).
- Deutsche Fachtexte für Domänenfragen — dieses RESEARCH.md ist entsprechend
  auf Deutsch verfasst, Bezeichner/technische Begriffe bleiben englisch.
- Kein Vendoring — deckungsgleich mit Workspace-Regel.
- „Working beats theoretically better" / „Don't over-engineer" — bestärkt die
  Empfehlung, ausschließlich das bestehende `callout`-Feld zu nutzen statt
  neuer Struktur.

Repo-Root von `vorlagen` selbst hat kein eigenes `CLAUDE.md` (nur
Workspace-`CLAUDE.md` gilt); `site/CLAUDE.md` existiert nicht (leer/nicht
vorhanden).

## Sources

### HIGH confidence
- Codebase-Analyse: `site/src/content.config.ts`, `site/src/pages/anleitung/index.astro`,
  `site/src/content/anleitung/06-fotosammlung.md`, `site/src/content/anleitung/02-schriften-installieren.md`,
  `site/src/styles/app.css`, `site/src/layouts/Base.astro` (alle direkt gelesen und verifiziert)
- `git log`/`git show 65bb4ef` (direkt im Repo geprüft)
- `grep -rn "Fotosammlung" site/src` (keine weiteren Referenzen gefunden)
- Live gefetchte `https://design-system.gruene.at/design-system.css` — bestätigt Existenz und
  unterschiedliche visuelle Definition von `.gat-callout`, `.gat-callout--info`, `.gat-callout--warn`

### MEDIUM confidence
- (keine — alle Kernaussagen sind direkt am Code/CSS verifiziert)

### LOW confidence (needs validation)
- Exakter Wortlaut des neuen Hinweistexts ist eine redaktionelle Entscheidung, keine
  technische — Planner/Executor sollte sich am Ton von Schritt 02 orientieren, aber der
  finale Satz ist nicht vorab „verifizierbar", sondern eine Content-Entscheidung.

## Metadata

**Confidence breakdown:**
- Codebase: HIGH — alle Dateien direkt gelesen, Vorgänger-Recherche stichprobenartig
  gegen den aktuellen Stand verifiziert, keine Abweichungen gefunden.
- Standard Stack: HIGH — keine neue Library, Astro-Version und DS-CDN-Link direkt geprüft.
- Architecture: HIGH — Muster ist 1:1 im Code vorhanden (Schritt 02) und wiederverwendbar.
- Pitfalls: MEDIUM — Pitfalls sind aus Analogie zum Issue-Text und bestehendem Code
  abgeleitet, nicht aus externer Recherche (kein externes Ökosystem-Risiko bei einem
  reinen Markdown-Content-Fix).

**Research date:** 2026-08-26
**Sub-agents used:** Kein Parallel-Dispatch — Light-Depth-Recherche für ein kleines
Content-Issue (1 Effektiv-Agent: Codebase, aufbauend auf abgebrochenem Vorlauf
in `research/codebase.md`, plus direkte Verifikation von Design-System-CSS statt
separatem Ecosystem-Sub-Agent, da kein neuer Stack involviert ist).
**Raw research files:** `.issues/cg83g-fotosammlung-auf-der-anleitungsseite-als-noe-only-kennzeichnen/research/codebase.md`
