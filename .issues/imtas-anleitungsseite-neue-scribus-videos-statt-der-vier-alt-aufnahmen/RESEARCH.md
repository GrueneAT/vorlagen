# Research: Anleitungsseite — neue Scribus-Videos statt der vier Alt-Aufnahmen

**Researched:** 2026-08-26
**Issue:** imtas-anleitungsseite-neue-scribus-videos-statt-der-vier-alt-aufnahmen
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)
Kein CONTEXT.md gefunden — kein `issue:discuss` durchlaufen. ISSUE.md ist die einzige
verbindliche Vorgabe (siehe Datei); keine zusätzlichen Locked Decisions oder Deferred
Ideas zu übernehmen.
</user_constraints>

## Summary

Kleine, gut umrissene Datenänderung mit einem CSS-Nebenaspekt. Der Kern ist der Austausch
des `videos`-Arrays in `site/src/data/videos.ts`: vier Alt-Einträge raus, zwei neue rein,
kein `legacyDesign` mehr setzen. Der Hinweis-Callout in `VideoGrid.astro` ist bereits
korrekt bedingt gebaut (`hasLegacyDesign = videos.some(v => v.legacyDesign)`) — sobald kein
Eintrag mehr das Flag trägt, verschwindet er automatisch, ohne dass Markup angefasst werden
muss. Das ist exakt so von Commit `120c54e` vorgesehen worden.

Zwei Dinge sind nicht offensichtlich aus dem Issue-Text, aber code-verifiziert wichtig:
Erstens ist `.app-video-grid` kein festes Vier-Spalten-Grid, sondern
`repeat(auto-fill, minmax(220px, 1fr))` — mit nur zwei Karten bleiben bei `auto-fill` auf
breiten Viewports leere Grid-Spuren stehen (das ist exakt das im Akzeptanzkriterium
genannte "halbleere Raster"-Risiko). Der Standard-Fix ist der Wechsel auf `auto-fit`, eine
Ein-Zeilen-Änderung in `site/src/styles/app.css`. Zweitens gibt es einen Python-Test
(`tests/unit/test_site_anleitung_content.py`), der hart auf die vier alten Video-IDs
gekoppelt ist und dessen `test_legacy_design_notice_matches_the_data` beim Wegfall aller
`legacyDesign`-Flags absichtlich mit einer expliziten Anweisung fehlschlägt, sich selbst zu
entfernen. `npm run build` deckt diesen Test nicht ab — er muss separat mit `pytest`
laufen, sonst ist "Build läuft durch" trügerisch grün während CI rot wird.

`VideoGrid` wird nicht nur auf `/anleitung/` gerendert, sondern auch auf jeder
Vorlagen-Detailseite (`site/src/pages/templates/[...id].astro`), weil beide dieselbe
`videos`-Datenquelle einbinden — die Änderung wirkt sich also automatisch (und korrekt) auf
beide Stellen aus.

Die neuen Video-IDs und Titel wurden per YouTube-oEmbed verifiziert (Kanal "Die Grünen
Niederösterreich", Titel stimmen exakt mit dem Issue überein). Eine verlässliche Laufzeit
(`duration`) ließ sich mit den verfügbaren Tools nicht ermitteln — oEmbed liefert keine
Dauer, und die Watch-Seite rendert sie clientseitig per JS. Da `duration` ein rein
kosmetisches, optionales Feld ist (nirgends getestet), empfiehlt sich, es für die neuen
Einträge wegzulassen, statt einen Wert zu raten.

**Primary recommendation:** `videos.ts` auf die zwei neuen Einträge ohne `legacyDesign`
und ohne `duration` reduzieren, `.app-video-grid` von `auto-fill` auf `auto-fit` (plus
moderater Max-Breite) umstellen, und `tests/unit/test_site_anleitung_content.py`
(`EXPECTED_VIDEO_IDS` aktualisieren, `test_legacy_design_notice_matches_der_data`
entfernen) in derselben Änderung mitziehen — sonst bricht CI trotz grünem `npm run build`.

## Codebase Analysis

### Relevant Code

| File | Purpose | Last Modified | Relevance |
|---|---|---|---|
| `site/src/data/videos.ts` | `videos`-Array, `AnleitungsVideo`-Interface, Poster/Watch-URL-Helper | zuletzt inhaltlich in `120c54e` (legacyDesign eingeführt) | Primärer Änderungsort — Array ersetzen |
| `site/src/components/VideoGrid.astro` | rendert Grid + bedingten Legacy-Hinweis | `120c54e` | Kein Code-Änderungsbedarf — Verhalten bereits korrekt bedingt |
| `site/src/components/VideoModal.astro` | YouTube-Modal, generisch über data-Attribute | `c180fcb` (Modal-Zentrierung, unrelated) | Keine Änderung nötig |
| `site/src/pages/anleitung/index.astro` | bindet `VideoGrid` ein | — | Keine Änderung nötig, konsumiert nur `videos` |
| `site/src/pages/templates/[...id].astro` | bindet ebenfalls `VideoGrid` mit derselben `videos`-Quelle ein | — | Zweiter, im Issue nicht erwähnter Renderort — profitiert automatisch mit |
| `site/src/styles/app.css` (ab Zeile 934) | `.app-video-grid`-Layout | `c180fcb` (220px-Minimum für 4 Spalten) | Grid-Spaltenlogik anpassen (`auto-fill` → `auto-fit`) |
| `tests/unit/test_site_anleitung_content.py` | Guard-Tests für Video-Array & Legacy-Hinweis | `120c54e` | Muss mitgeändert werden, sonst CI-Fail |

### Interfaces

<interfaces>
// From site/src/data/videos.ts
export interface AnleitungsVideo {
  /** YouTube-Video-ID (der `v=`-Parameter der watch-URL). */
  youtube: string;
  /** Kartentitel. Standard: der YouTube-Titel des Videos. */
  title: string;
  /** Optionale Kurzbeschreibung unter dem Titel. */
  description?: string;
  /** Laufzeit als "M:SS" — rein informativ auf der Karte. */
  duration?: string;
  /** Poster-Bild-URL. Leer lassen für das YouTube-Thumbnail. */
  poster?: string;
  /** true = im alten Corporate Design aufgenommen. */
  legacyDesign?: boolean;
}
export function posterFor(v: AnleitungsVideo): string;          // -> `https://i.ytimg.com/vi/${v.youtube}/maxresdefault.jpg` (or v.poster)
export function posterFallbackFor(v: AnleitungsVideo): string;  // -> `https://i.ytimg.com/vi/${v.youtube}/hqdefault.jpg`
export function watchUrl(v: AnleitungsVideo): string;           // -> `https://www.youtube.com/watch?v=${v.youtube}`
export const videos: AnleitungsVideo[];  // currently 4 entries, all legacyDesign: true

// From site/src/components/VideoGrid.astro
interface Props { videos: AnleitungsVideo[]; modalId: string; }
// const hasLegacyDesign = videos.some(v => v.legacyDesign);  <- drives the notice <p> — becomes false, notice unrenders, once no entry has legacyDesign: true

// From site/src/components/VideoModal.astro
interface Props { id: string; }
// trigger contract (any element): data-video-target={modalId} data-video-id={youtube} data-video-title={title}, href = watchUrl(v) as no-JS fallback

// From site/src/styles/app.css (line ~934)
// .app-video-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
// @media (max-width: 640px) { .app-video-grid { grid-template-columns: 1fr; } }  <- mobile breakpoint, unaffected by this issue

// From tests/unit/test_site_anleitung_content.py
EXPECTED_VIDEO_IDS: set[str]  // hardcoded 4 legacy IDs — must become {"SDT9eM9tReU", "3rMFX_VLvpE"}
def test_video_ids_are_complete() -> None    // asserts extracted `youtube:` values == EXPECTED_VIDEO_IDS
def test_every_video_has_a_title() -> None   // count-coupled to len(EXPECTED_VIDEO_IDS), auto-fixed once constant updated
def test_legacy_design_notice_matches_the_data() -> None
  // any_legacy = "legacyDesign: true" in videos_array_source
  // if not any_legacy: pytest.fail("... Hinweis in VideoGrid.astro und diesen Test entfernen.")
  // -> WILL fail once legacyDesign is fully removed from videos.ts; delete this test (not the notice markup in VideoGrid.astro, which the issue says may stay)
</interfaces>

### Reusable Components

Alles Notwendige existiert bereits: `posterFor`/`posterFallbackFor`/`watchUrl` decken das
Poster/Fallback/No-JS-Link-Verhalten vollautomatisch aus der `youtube`-ID ab — kein eigenes
Bild, kein zusätzlicher Code nötig. Der Legacy-Hinweis-Mechanismus (`hasLegacyDesign`) ist
bereits so gebaut, dass er "von selbst" verschwindet — keine Komponentenänderung
erforderlich, nur Datenänderung.

### Potential Conflicts

- CSS: `.app-video-grid`s `auto-fill`-Minimum von 220px wurde in `c180fcb` bewusst für vier
  Karten gewählt (Kommentar im Code referenziert das explizit) — dieser Kommentar sollte bei
  der CSS-Änderung mit-aktualisiert werden, sonst irreführend für künftige Leser.
- Tests: `tests/unit/test_site_anleitung_content.py` ist hart auf die alten IDs/den
  Legacy-Zustand gekoppelt (siehe oben) — ohne Anpassung schlägt CI fehl, obwohl
  `npm run build` grün bleibt.
- Kein Konflikt mit `VideoModal.astro` — vollständig datengetrieben, keine Video-Zahl fest
  codiert.

### Code Patterns in Use

- Datengetriebene UI: Komponenten leiten Zustand (`hasLegacyDesign`, Karten-Anzahl, Poster)
  rein aus dem `videos`-Array ab, keine Seiten-spezifische Logik nötig.
- Guard-Tests statt reinem Build-Check: `tests/unit/test_site_anleitung_content.py` prüft
  Content-Integrität, die Astro selbst nicht validiert (Kommentar im Testfile-Header
  begründet das explizit).

## Standard Stack

Keine neue Library nötig — reine Datenänderung in bestehendem Astro/TypeScript-Setup
(`astro@^5.0.0`, laut `site/package.json`). Kein Grund, vom bestehenden Stack abzuweichen.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| Poster-Bild pro Video | eigener Screenshot/Upload | `posterFor()` (YouTube-Thumbnail-CDN) | existiert bereits, im Issue explizit bestätigt ("Poster kommt automatisch") |
| Sichtbarkeit des Legacy-Hinweises | manuelles Ein-/Ausblenden pro Seite | bestehendes `hasLegacyDesign`-Derivat in `VideoGrid.astro` | bereits korrekt datengetrieben, keine Seiten-Logik nötig |
| Grid-Spaltenzahl je nach Karten-Anzahl | JS/Zähl-Logik | CSS `auto-fit` statt `auto-fill` | Standard-CSS-Grid-Lösung für "wenige Items in einem `minmax`-Grid" |

## Architecture Patterns

### Recommended Approach

1. `site/src/data/videos.ts`: `videos`-Array durch genau die zwei Einträge ersetzen
   (`SDT9eM9tReU` "Erste Schritte mit Scribus", `3rMFX_VLvpE` "Export einer Scribus
   Datei"), kein `legacyDesign`, `duration` weglassen (siehe Common Pitfalls).
2. `site/src/styles/app.css`: `.app-video-grid { grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }`
   → `repeat(auto-fit, minmax(220px, 320px))` (oder ähnliche moderate Obergrenze), Kommentar
   direkt darüber (aktuell referenziert "vier Tutorials") auf den neuen Stand (zwei
   Tutorials) aktualisieren. Mobile-Breakpoint (`max-width: 640px`) unverändert lassen.
3. `tests/unit/test_site_anleitung_content.py`: `EXPECTED_VIDEO_IDS` auf die zwei neuen IDs
   setzen (Kommentare mit Titeln aktualisieren), `test_legacy_design_notice_matches_the_data`
   entfernen (Fail-Message der Funktion instruiert das explizit).
4. Verifikation: `cd site && npm run build` UND
   `/root/.local/bin/pytest tests/unit/test_site_anleitung_content.py -q` (bzw. `pytest
   tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py` wie in CI) — beide müssen
   grün sein.

### Anti-Patterns to Avoid

- **Legacy-Hinweis-Markup in VideoGrid.astro entfernen:** Issue sagt ausdrücklich, der Block
  darf im Markup bleiben (rendert einfach nicht mehr) — nicht anfassen, spart unnötigen Diff.
- **`duration` raten/erfinden:** kein verlässlicher Wert ermittelbar (siehe Pitfalls) — Feld
  ist optional und ungetestet, lieber weglassen als falsch angeben.
- **Nur `npm run build` als Fertig-Kriterium nehmen:** deckt den Python-Testbruch nicht ab.

## Common Pitfalls

### `duration` nicht zuverlässig ermittelbar

**What goes wrong:** Ein erfundener oder veralteter Laufzeit-Wert landet auf der Karte.
**Why it happens:** YouTube-oEmbed liefert keine Dauer; die Watch-Seite rendert sie
clientseitig, WebFetch bekommt sie nicht.
**How to avoid:** Feld weglassen (ist optional, laut Interface-Kommentar "rein
informativ") — kein Codepfad hängt daran (`{v.duration && ...}` in `VideoGrid.astro`
Zeile 66 rendert einfach nichts).
**Warning signs:** Ein Duration-Wert im Diff, der nicht aus einer verifizierten Quelle
stammt.

### CSS Grid `auto-fill` lässt bei wenigen Items Lücken

**What goes wrong:** Zwei Karten stehen mit sichtbarem Leerraum daneben statt den Platz zu
füllen — genau das im Akzeptanzkriterium ausgeschlossene "halbleere Raster".
**Why it happens:** `auto-fill` reserviert weiterhin so viele Spuren, wie in die
Container-Breite passen, auch wenn sie leer bleiben; nur `auto-fit` kollabiert leere
Spuren und lässt `1fr` den realen Items den Platz zuweisen.
**How to avoid:** `auto-fill` → `auto-fit`, plus moderate Max-Breite pro Karte, damit zwei
Karten nicht randlos über die volle Breite gezogen werden.
**Warning signs:** Visuelle Prüfung bei typischer Desktop-Breite (~1280px) nach der
Änderung — sollte mit `auto-fit` und den Standard-`app.css`-Werten sauber aussehen.

### Guard-Test bricht CI trotz grünem Build

**What goes wrong:** `npm run build` ist grün, `pytest tests/unit/` ist rot, PR/CI schlägt
fehl.
**Why it happens:** `tests/unit/test_site_anleitung_content.py` prüft Inhalte, die Astro
selbst nicht validiert; der Test wurde bewusst so gebaut, dass er beim vollständigen
Wegfall von `legacyDesign` explizit fehlschlägt (Fail-Message enthält die
Handlungsanweisung).
**How to avoid:** Testdatei im selben Change mitziehen (siehe Architecture Patterns,
Schritt 3), beide Testläufe vor Abschluss ausführen.
**Warning signs:** `EXPECTED_VIDEO_IDS` noch mit alten IDs im Diff sichtbar.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|---|---|---|---|---|
| node/npm | `npm run build` | yes | node v26.7.0, npm 11.19.0 | — |
| `site/node_modules` | Astro build | yes, bereits installiert in diesem Worktree | — | `npm install` falls fehlend |
| python3 | Testsuite | yes | 3.13.5 | — |
| pytest | `tests/unit/` | yes, aber NICHT auf Standard-PATH | `/root/.local/bin/pytest` (auch `/opt/sortition-venv/bin/pytest`) | vollen Pfad verwenden |
| PyYAML | Testsuite (`import yaml`) | yes | 6.0.3 | — |

## Project Constraints (from CLAUDE.md)

Aus `/root/.config/claude/CLAUDE.md` (Container-weit) und
`/Users/florianmotlik/Code/GrueneAT/web-apps/CLAUDE.md` (Workspace-weit):

- **Kein Vendoring von Drittabhängigkeiten.** YouTube bleibt eingebettet wie bisher (per
  `youtube-nocookie.com`-iframe, unverändert) — keine lokalen Kopien von Thumbnails/Assets.
  Deckt sich mit dem Issue-Constraint.
- **Keine Werkzeug-Attribution** in Commits/Code/Kommentaren — kein "claude", kein
  "Generated with", kein `Co-Authored-By`. Gilt für alle Artefakte dieser Änderung.
- **Conventional Commit**, englische Bezeichner/Commit-Messages, deutsche Fachtexte wo
  passend (Issue-Body ist Deutsch, Code-Kommentare im Repo sind bereits gemischt
  Deutsch/Englisch je nach bestehendem Stil in der jeweiligen Datei — bestehendem
  Dateikontext folgen, nicht neu erfinden).
- **Nicht direkt am main-Checkout arbeiten** — bereits erfüllt, diese Recherche läuft im
  korrekten Worktree.
- Kein `.claude/skills/`-Eintrag ist für dieses Issue einschlägig (nur
  `idml-import`/`idml-scaffold`/`idml-tune`/`experiments` vorhanden — betreffen die
  Print-Pipeline, nicht die Astro-Galerie-Site).
- `.issues/MAP.md` existiert nicht in diesem Repo — keine Altlast-Staleness zu vermerken.

## Sources

### HIGH confidence
- Codebase-Analyse: `site/src/data/videos.ts`, `VideoGrid.astro`, `VideoModal.astro`,
  `app.css`, `tests/unit/test_site_anleitung_content.py`, `pages/anleitung/index.astro`,
  `pages/templates/[...id].astro` (alle direkt gelesen).
- `git show c180fcb`, `git show 120c54e` — Commit-Historie und -Begründung direkt
  eingesehen.
- `npm run build` lokal ausgeführt — grüne Baseline (26 Seiten, 3.4s) vor jeder Änderung.
- `/root/.local/bin/pytest tests/unit/test_site_anleitung_content.py -q` lokal ausgeführt —
  8/8 grün als Baseline.
- YouTube-oEmbed-Abfrage für beide neuen Video-IDs — Titel und Kanal bestätigt
  ("Die Grünen Niederösterreich").

### MEDIUM confidence
- CSS-`auto-fill`-vs-`auto-fit`-Verhalten — Standard-CSS-Grid-Spezifikationswissen, nicht
  gegen eine externe Quelle verifiziert, aber unstrittig und im konkreten Fall durch die
  Grid-Definition + Kartenzahl direkt nachvollziehbar.

### LOW confidence (needs validation)
- Video-Laufzeiten (`duration`) für die beiden neuen Videos — nicht ermittelbar mit den
  verfügbaren Tools (siehe Common Pitfalls). Empfehlung: weglassen statt raten.

## Metadata

**Confidence breakdown:**
- Codebase: HIGH — alle relevanten Dateien gelesen, Commit-Historie eingesehen, Build +
  Tests lokal grün verifiziert.
- Standard Stack: HIGH — keine neue Dependency, bestehender Stack ausreichend.
- Architecture (CSS-Fix): MEDIUM-HIGH — Standardlösung, aber visuelle Feinabstimmung
  (Max-Breite) ist Geschmackssache, kein exakter Pixelwert vorgeschrieben.
- Pitfalls: HIGH für Test-Kopplung (Code direkt gelesen), LOW für `duration`-Werte
  (nicht ermittelbar).

**Research date:** 2026-08-26
**Sub-agents used:** keine — Issue klein genug für direkte Recherche (light/standard
Mischform), kein Ecosystem-Sub-Agent nötig (keine neue Library), kein separater
Codebase-Sub-Agent nötig (Scope passt in eine Session).
**Raw research files:** `.issues/imtas-anleitungsseite-neue-scribus-videos-statt-der-vier-alt-aufnahmen/research/` (`codebase.md`, `pitfalls.md`)
