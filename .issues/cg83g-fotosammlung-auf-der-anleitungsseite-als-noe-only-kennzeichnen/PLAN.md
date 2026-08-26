# Plan: Fotosammlung auf der Anleitungsseite als NÖ-only kennzeichnen

<objective>
What this plan accomplishes: Der Anleitungsschritt „Fotosammlung" auf
`/anleitung/` weist unübersehbar aus, dass die Sammlung nur für
Niederösterreich gilt — im Titel, als Design-System-Callout und mit einem
expliziten Satz im Fließtext zum GGS-NÖ-Login.

Why it matters: Anwenderfeedback (GitHub-Issue #158): Die Fotosammlung steht
aktuell als allgemeiner Punkt auf der Seite. Der einzige Hinweis auf die
Einschränkung steckt im Link-Label „(GGS NÖ, Login nötig)" — Gruppen außerhalb
Niederösterreichs klicken sich in eine Sackgasse.

Scope:
- IN: eine einzige Datei — `site/src/content/anleitung/06-fotosammlung.md`
  (Frontmatter `title` + `callout`, Body-Text).
- OUT: `site/src/content.config.ts`, `site/src/pages/anleitung/index.astro`,
  `site/src/styles/app.css`, das Design-System, neue CSS-Klassen oder
  Komponenten, das bestehende Link-Label, alle anderen Anleitungsschritte.

Kein CONTEXT.md vorhanden (kein `issue:discuss`-Lauf) — die Entscheidungen
folgen der Constraints-Sektion von ISSUE.md („reine Content-Änderung, keine
neuen Komponenten nötig") und den Empfehlungen aus RESEARCH.md.
</objective>

<strategy>
Richtung: Das Frontmatter-Schema der `anleitung`-Collection hat bereits ein
optionales `callout: 'info' | 'warn'`-Feld, und `index.astro` rendert es schon
generisch als `gat-callout gat-callout--<wert>` auf die `<section>`. Schritt 02
(„Schriften installieren") nutzt das Muster bereits für einen
Einschränkungs-Hinweis. Damit ist die gesamte Aufgabe eine Content-Änderung an
genau einer Markdown-Datei — kein Schema-, Astro- oder CSS-Eingriff.

Strategische Optionen:
1. **Bestehendes `callout`-Feld nutzen (gewählt).** Null neue Struktur, exakt
   das Muster, das die Seite selbst schon verwendet, erfüllt den ISSUE-Constraint
   „keine neuen Komponenten nötig".
2. Eigene Hinweis-Klasse nach dem Vorbild von `.app-font-notice__action`
   (Commit `65bb4ef`) — verworfen: diese Klasse ist bewusst
   Template-Detailseiten vorbehalten, hier wäre sie neue Struktur ohne Nutzen.
3. Nur das Link-Label schärfen — verworfen: verletzt das Akzeptanzkriterium
   „Der Login-Hinweis steht im Text, nicht nur im Link-Label".

Entscheidungspunkte:
- **`info` statt `warn`:** `warn` ist der einzige Präzedenzfall im Repo und
  deshalb verführerisch, signalisiert im DS aber ein Fehlerrisiko. Der
  NÖ-Hinweis ist eine reine Zugangsinformation → `info`.
- **Wortlaut ist im Plan vorgegeben,** nicht dem Executor überlassen: der Ton
  der Schritte 01–05 (2. Person Plural, Halbgeviertstrich, ein `**bold**`-Satz
  für die zentrale Aussage) ist redaktionell, nicht ableitbar.
- **Link-Label bleibt unverändert** — es ist bereits korrekt, der Hinweis
  gehört zusätzlich in den Fließtext.
</strategy>

<skills>
Keine Workspace-Skill ist für dieses Issue einschlägig. Die vorhandenen Skills
(`experiments`, `idml-import`, `idml-scaffold`, `idml-tune`) betreffen die
IDML-/Vorlagen-Pipeline, nicht die Astro-Content-Collection der
Anleitungsseite. Es wird bewusst keine Skill getaggt.
</skills>

<context>
Issue: @.issues/cg83g-fotosammlung-auf-der-anleitungsseite-als-noe-only-kennzeichnen/ISSUE.md
Research: @.issues/cg83g-fotosammlung-auf-der-anleitungsseite-als-noe-only-kennzeichnen/RESEARCH.md

<interfaces>
<!-- Executor: diese Verträge direkt verwenden. Den Codebase nicht danach
     durchsuchen. Beide Dateien sind READ-ONLY für dieses Issue. -->

// site/src/content.config.ts — anleitung collection (bereits vorhanden, NICHT ändern)
const anleitung = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/anleitung' }),
  schema: z.object({
    order: z.number(),
    title: z.string(),
    // Optional: rendert den Abschnitt als Design-System-Callout statt als
    // schlichten Block.
    callout: z.enum(['info', 'warn']).optional(),
    links: z.array(z.object({
      label: z.string(),
      href: z.string(),
      kind: z.enum(['internal', 'download', 'external']),
    })).optional(),
  }),
});

// site/src/pages/anleitung/index.astro — Step-Rendering (bereits vorhanden, NICHT ändern)
// <section class={data.callout ? `gat-callout gat-callout--${data.callout} app-step` : 'app-step'}>
//   <h3 class="gat-headline app-step__title">{data.title}</h3>
//   <div class="app-step__body"><Content /></div>
//   <ul class="app-step__links"> ... </ul>
// </section>

// Konsequenz: `callout: info` im Frontmatter erzeugt ohne weiteren Eingriff
// `class="gat-callout gat-callout--info app-step"` im gerenderten HTML.
// `.gat-callout--info` kommt aus dem per CDN geladenen Design-System
// (site/src/layouts/Base.astro L12, https://design-system.gruene.at/design-system.css).
</interfaces>

Ist-Zustand von `site/src/content/anleitung/06-fotosammlung.md` (Ausgangspunkt
der Änderung):

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

Key files:
@site/src/content/anleitung/06-fotosammlung.md — die einzige zu ändernde Datei
@site/src/content/anleitung/02-schriften-installieren.md — stilistisches Vorbild
  (`callout: warn` + abschließender `**bold**`-Satz), NUR lesen, nicht ändern
</context>

<commit_format>
Format: conventional mit Issue-ID-Präfix (`.issues/config.yaml`:
`commits.format: conventional`, `commits.prefix: true`; deckt sich mit der
History, z. B. `cg83g: docs(issues): research cg83g-...`).
Example: cg83g: docs(anleitung): mark photo collection as Lower-Austria-only
Pattern: {issue-id}: {type}({scope}): {description}
Commit-Subject auf Englisch, Inhaltstexte auf Deutsch. KEINE
Werkzeug-Attribution, kein `Co-Authored-By`, keine Nennung von Tools.
</commit_format>

<tasks>

<task type="auto">
  <name>Task 1: 06-fotosammlung.md als NÖ-only kennzeichnen</name>
  <files>site/src/content/anleitung/06-fotosammlung.md</files>
  <action>
  Ersetze den kompletten Inhalt von
  `site/src/content/anleitung/06-fotosammlung.md` EXAKT durch den folgenden
  Text. Der Wortlaut ist eine redaktionelle Vorgabe dieses Plans — nicht
  umformulieren, nicht kürzen, nicht „verbessern", keine zusätzlichen Absätze
  ergänzen. Umlaute und der Halbgeviertstrich `—` sind bewusst gesetzt und
  müssen erhalten bleiben (UTF-8, kein `oe`/`ae`/`ue`, kein `-` statt `—`).
  Der Block zwischen den beiden Markierungen ist der vollständige, wörtliche
  Dateiinhalt — beginnend bei Spalte 1, keine Einrückung ergänzen:

BEGIN DATEIINHALT (diese Zeile selbst NICHT übernehmen)
---
order: 6
title: "Fotosammlung für eure Druckwerke (nur NÖ)"
callout: info
links:
  - label: "Zur Fotosammlung (GGS NÖ, Login nötig)"
    href: "https://ggs-noe.gruene.at/fotosammlung-fuer-social-media-und-druckwerke/"
    kind: external
---

Im Gemeindegruppenservice der Grünen Niederösterreich findet ihr Bilder, die
über Adobe Stock erworben wurden und die ihr somit für Social-Media-Beiträge
oder eure Druckwerke verwenden könnt.

Der Zugang läuft über den GGS NÖ und setzt ein Login der Grünen
Niederösterreich voraus — Gruppen außerhalb Niederösterreichs können die
Sammlung daher nicht nutzen.

**Diese Sammlung gibt es nur für Niederösterreich.**
END DATEIINHALT (diese Zeile selbst NICHT übernehmen)

  Detailvorgaben und Begründungen:
  - `order: 6` und der gesamte `links:`-Block bleiben unverändert — Label,
    href und `kind: external` sind bereits korrekt.
  - `callout: info`, NICHT `warn`. `warn` ist zwar der einzige Präzedenzfall im
    Repo (Schritt 02), signalisiert im Design-System aber ein Fehlerrisiko. Der
    NÖ-Hinweis ist eine reine Zugangsinformation. Ein Tippfehler im Wert
    scheitert an `z.enum(['info','warn'])` beim Build.
  - `callout` steht nach `title` und vor `links` — analog zur Position in
    `02-schriften-installieren.md`.
  - Der `**bold**`-Schlusssatz folgt dem Muster von Schritt 02
    („**Bitte wendet euch dafür an euer Landesbüro.**"): ein eigener, knapper
    Absatz trägt die zentrale Einschränkung.
  - KEIN Nummerierungspräfix „6. Schritt:" ergänzen — die Schritte 04–06 sind
    bewusst unnummeriert-thematisch betitelt.
  - `site/src/content.config.ts`, `site/src/pages/anleitung/index.astro` und
    `site/src/styles/app.css` NICHT anfassen: das `callout`-Feld existiert
    bereits im Schema und wird bereits generisch gerendert. Keine neue
    CSS-Klasse, keine neue Komponente (expliziter ISSUE-Constraint).
  </action>
  <verify>
  <automated>cd site && npm run build</automated>
  </verify>
  <done>
  - `site/src/content/anleitung/06-fotosammlung.md` hat den Titel
    "Fotosammlung für eure Druckwerke (nur NÖ)"
  - Frontmatter enthält `callout: info`
  - Body enthält einen Absatz zu GGS-NÖ-Login und fehlendem Zugang außerhalb
    Niederösterreichs sowie den `**bold**`-Schlusssatz
  - `order`- und `links`-Block sind unverändert
  - `npm run build` in `site/` läuft ohne Fehler durch (Zod-Schema akzeptiert
    `callout: info`)
  - `git status --short` zeigt genau eine geänderte Datei unter `site/`
  </done>
</task>

<task type="auto">
  <name>Task 2: Gerendertes HTML gegen die Akzeptanzkriterien prüfen</name>
  <files>site/dist/anleitung/index.html (nur lesen, Build-Artefakt — nicht committen)</files>
  <action>
  Verifiziere am tatsächlich gebauten Output, dass die drei Akzeptanzkriterien
  aus ISSUE.md erfüllt sind. Keine Quelldatei wird in diesem Task geändert.

  Führe aus (aus dem Repo-Root):

      cd site && npm run build && \
      grep -q 'gat-callout gat-callout--info app-step' dist/anleitung/index.html && \
      grep -q 'Fotosammlung für eure Druckwerke (nur NÖ)' dist/anleitung/index.html && \
      grep -q 'Login der Grünen' dist/anleitung/index.html && \
      grep -q 'außerhalb Niederösterreichs' dist/anleitung/index.html && \
      echo "ANLEITUNG OK"

  Prüfe zusätzlich per Augenschein im Ausschnitt
  `grep -B2 -A25 'gat-callout--info' dist/anleitung/index.html`:
  - Der `(nur NÖ)`-Zusatz steht in der `<h3 class="gat-headline app-step__title">`
    des Fotosammlungs-Abschnitts, ist also ohne Klick sichtbar.
  - Der Login-/NÖ-Hinweis steht im `app-step__body`, nicht ausschließlich im
    `app-step__link`-Label.
  - Umlaute sind korrekt gerendert (keine Mojibake, kein `nur NOe`).

  Falls ein `grep` fehlschlägt: der Fehler liegt in Task 1 — dort korrigieren
  (Tippfehler im Titel, falscher `callout`-Wert, fehlender Body-Absatz), NICHT
  die grep-Muster aufweichen und NICHT `dist/` von Hand editieren.

  `site/dist/` ist Build-Output und wird nicht committet — prüfe vor dem Commit
  mit `git status --short`, dass nur
  `site/src/content/anleitung/06-fotosammlung.md` in der Änderungsliste steht
  (plus die Issue-Artefakte, sofern der Workflow sie mitführt).
  </action>
  <verify>
  <automated>cd site && npm run build && grep -q 'gat-callout gat-callout--info app-step' dist/anleitung/index.html && grep -q 'Fotosammlung für eure Druckwerke (nur NÖ)' dist/anleitung/index.html && grep -q 'Login der Grünen' dist/anleitung/index.html && grep -q 'außerhalb Niederösterreichs' dist/anleitung/index.html && echo "ANLEITUNG OK"</automated>
  </verify>
  <done>
  - Das Kommando endet mit `ANLEITUNG OK` (Exit 0)
  - Der Fotosammlungs-Abschnitt trägt im gebauten HTML die Klassen
    `gat-callout gat-callout--info app-step`
  - „(nur NÖ)" steht in der Überschrift des Abschnitts
  - Der Login-Hinweis steht im Body-Text, nicht nur im Link-Label
  - `git status --short` listet keine Dateien unter `site/dist/`
  </done>
</task>

</tasks>

<verification>
Abschließende Prüfungen nach allen Tasks:
- `cd site && npm run build` — Astro-Build inklusive Zod-Schema-Validierung
- KEIN `npm run check` nötig — `astro check` verlangt `@astrojs/check`, das
  nicht in `site/package.json` steht, und würde nur einen Installationsdialog
  auslösen. Es wurde keine `.astro`/`.ts`-Datei angefasst.
- `git diff --stat` — genau eine geänderte Quelldatei:
  `site/src/content/anleitung/06-fotosammlung.md`
- `git diff` — enthält keinerlei Werkzeug-/AI-Attribution
</verification>

<success_criteria>
Bildet 1:1 die Akzeptanzkriterien aus ISSUE.md ab:
- Auf `/anleitung/` ist ohne Klick erkennbar, dass die Fotosammlung nur für
  Niederösterreich ist — der Titel lautet „Fotosammlung für eure Druckwerke
  (nur NÖ)" und der Abschnitt ist als `gat-callout--info` hervorgehoben
- Der Login-Hinweis steht im Fließtext („Der Zugang läuft über den GGS NÖ und
  setzt ein Login der Grünen Niederösterreich voraus — Gruppen außerhalb
  Niederösterreichs können die Sammlung daher nicht nutzen."), nicht nur im
  Link-Label
- Build läuft durch: `cd site && npm run build` endet mit Exit 0
- Zusatz aus den Constraints: reine Content-Änderung, keine neue Komponente,
  keine neue CSS-Klasse, kein Schema-Eingriff
</success_criteria>
