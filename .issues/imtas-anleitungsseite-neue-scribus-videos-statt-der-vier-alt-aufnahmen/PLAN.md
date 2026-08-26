# Plan: Anleitungsseite — neue Scribus-Videos statt der vier Alt-Aufnahmen

<objective>
Was dieser Plan erreicht: Das `videos`-Array in `site/src/data/videos.ts` wird durch
genau zwei neue Scribus-Aufnahmen im aktuellen Corporate Design ersetzt (`SDT9eM9tReU`
"Erste Schritte mit Scribus", `3rMFX_VLvpE` "Export einer Scribus Datei"), kein Eintrag
traegt mehr `legacyDesign`. Damit verschwindet der Hinweis "im alten Design aufgenommen"
automatisch (er haengt in `VideoGrid.astro` an `videos.some(v => v.legacyDesign)`). Das
Video-Grid wird von `auto-fill` auf `auto-fit` mit moderater Obergrenze umgestellt, damit
zwei Karten kein halbleeres Vier-Spalten-Raster hinterlassen. Der Guard-Test
`tests/unit/test_site_anleitung_content.py` wird im selben Change mitgezogen.

Warum das wichtig ist: Die Seite behauptet aktuell dauerhaft, alle Videos seien veraltet
aufgenommen. Sobald die Neuaufnahmen drin sind, ist diese Aussage falsch — und der
Guard-Test bricht CI, wenn Datenaenderung und Testanpassung auseinanderfallen
(`npm run build` bleibt dabei truegerisch gruen).

Scope IN: `site/src/data/videos.ts` (Array-Austausch), `site/src/styles/app.css`
(`.app-video-grid` + Kommentar darueber), `tests/unit/test_site_anleitung_content.py`
(`EXPECTED_VIDEO_IDS`, Entfernen von `test_legacy_design_notice_matches_the_data`).

Scope OUT: `VideoGrid.astro` und `VideoModal.astro` werden NICHT angefasst (der
Legacy-Hinweis-Block darf laut ISSUE.md im Markup bleiben und rendert dann einfach nicht
mehr; das Modal ist vollstaendig datengetrieben). Ebenfalls OUT: das
`legacyDesign?: boolean`-Feld im `AnleitungsVideo`-Interface (bleibt als Mechanismus fuer
kuenftige Alt-Videos erhalten), der Mobile-Breakpoint `@media (max-width: 640px)` fuer
`.app-video-grid`, jede Aenderung an `pages/anleitung/index.astro` oder
`pages/templates/[...id].astro`.

Kein CONTEXT.md vorhanden (`issue:discuss` wurde nicht durchlaufen) — Entscheidungen
folgen ISSUE.md und den Empfehlungen aus RESEARCH.md. Abweichung von RESEARCH.md: die
dort als "nicht ermittelbar" markierten Laufzeiten sind inzwischen verifiziert (aus den
YouTube-Watch-Seiten: `lengthSeconds` 878 = 14:38 bzw. 519 = 8:39) und werden gesetzt,
nicht weggelassen.
</objective>

<strategy>
Richtung: Eine reine Datenaenderung plus zwei Folgeaenderungen, die sonst still
auseinanderlaufen. Der Kern ist ein Array-Austausch — alles Weitere ist bereits
datengetrieben gebaut und zieht automatisch nach.

Strategische Optionen und Entscheidung:

1. **Legacy-Hinweis entfernen vs. stehen lassen.** ISSUE.md sagt ausdruecklich: der
   Hinweis-Block darf im Markup bleiben, er rendert bei fehlendem `legacyDesign` einfach
   nicht mehr. Gewaehlt: stehen lassen. Das haelt den Diff klein und den Mechanismus fuer
   kuenftige Alt-Videos intakt. Verworfen: Markup + Interface-Feld loeschen — laut
   Recherche ein unnoetiger Diff, der eine bewusst gebaute Faehigkeit wegwirft.

2. **Grid-Layout.** `.app-video-grid` steht auf `repeat(auto-fill, minmax(220px, 1fr))`;
   `auto-fill` reserviert bei zwei Karten weiterhin leere Spuren — genau das im
   Akzeptanzkriterium ausgeschlossene halbleere Raster. Gewaehlt:
   `repeat(auto-fit, minmax(220px, 320px))` — `auto-fit` kollabiert leere Spuren, die
   320px-Obergrenze verhindert, dass zwei Karten auf Ultrawide-Monitoren randlos
   auseinandergezogen werden. Verworfen: nur `auto-fit` mit `1fr` (Karten werden auf
   breiten Viewports uebergross), und eine feste `grid-template-columns: repeat(2, ...)`
   (bricht die bestehende, responsive Logik der Datei).

3. **Laufzeiten (`duration`).** RESEARCH.md empfahl Weglassen, weil kein verlaesslicher
   Wert ermittelbar war. Inzwischen sind beide Werte aus den YouTube-Watch-Seiten
   verifiziert (878s bzw. 519s). Gewaehlt: `duration: '14:38'` und `duration: '8:39'`
   setzen — die Karten behalten damit dieselbe Informationsdichte wie bisher.

4. **Verifikationsumfang.** `npm run build` allein reicht nicht: der Guard-Test
   `tests/unit/test_site_anleitung_content.py` ist hart auf die vier alten IDs gekoppelt
   und `test_legacy_design_notice_matches_the_data` schlaegt beim Wegfall aller
   `legacyDesign`-Flags absichtlich fehl (die Fail-Message enthaelt die Handlungsanweisung,
   den Test zu entfernen). Gewaehlt: Build UND `pytest tests/unit/` wie in CI, plus eine
   Assertion gegen das gebaute HTML, die alle drei sichtbaren Akzeptanzkriterien
   (zwei Karten, kein Alt-Design-Hinweis, korrekte watch-URLs) in einem Lauf abdeckt.
</strategy>

<skills>
Keine Workspace-Skill ist fuer dieses Issue einschlaegig. `.claude/skills/` enthaelt nur
`idml-import`, `idml-scaffold`, `idml-tune` und `experiments` — alle betreffen die
Print-/IDML-Pipeline, nicht die Astro-Galerie-Site. Es wird bewusst kein Skill getaggt.
</skills>

<context>
Issue: @.issues/imtas-anleitungsseite-neue-scribus-videos-statt-der-vier-alt-aufnahmen/ISSUE.md
Research: @.issues/imtas-anleitungsseite-neue-scribus-videos-statt-der-vier-alt-aufnahmen/RESEARCH.md

Alle Pfade sind relativ zur Worktree-Wurzel
`/Users/florianmotlik/Code/GrueneAT/web-apps/vorlagen/.worktrees/imtas-anleitungsseite-neue-scribus-videos-statt-der-vier-alt-aufnahmen`.
Alle Kommandos werden von dieser Wurzel aus ausgefuehrt. Niemals am Haupt-Checkout
arbeiten.

<interfaces>
<!-- Executor: diese Contracts direkt verwenden. Nicht im Codebase danach suchen. -->

From site/src/data/videos.ts:
export interface AnleitungsVideo {
  youtube: string;        // YouTube-Video-ID (der `v=`-Parameter der watch-URL)
  title: string;          // Kartentitel
  description?: string;   // optionale Kurzbeschreibung
  duration?: string;      // Laufzeit als "M:SS", rein informativ auf der Karte
  poster?: string;        // leer lassen -> YouTube-Thumbnail
  legacyDesign?: boolean; // true = im alten CD aufgenommen -> blendet den Hinweis ein
}
export function posterFor(v: AnleitungsVideo): string;         // v.poster ?? https://i.ytimg.com/vi/<id>/maxresdefault.jpg
export function posterFallbackFor(v: AnleitungsVideo): string; // https://i.ytimg.com/vi/<id>/hqdefault.jpg
export function watchUrl(v: AnleitungsVideo): string;          // https://www.youtube.com/watch?v=<id>
export const videos: AnleitungsVideo[];  // aktuell 4 Eintraege, alle legacyDesign: true

From site/src/components/VideoGrid.astro  (READ-ONLY — nicht aendern):
interface Props { videos: AnleitungsVideo[]; modalId: string; }
const hasLegacyDesign = videos.some(v => v.legacyDesign);
// steuert den <p class="gat-callout ... app-video-notice">-Block; wird false, sobald kein
// Eintrag mehr legacyDesign traegt -> Hinweis rendert nicht mehr. Kein Eingriff noetig.
// Karte rendert: href={watchUrl(v)}, data-video-target={modalId}, data-video-id={v.youtube},
// data-video-title={v.title}, Poster via posterFor/posterFallbackFor,
// {v.duration && <span class="app-video-card__duration">{v.duration}</span>}

From site/src/components/VideoModal.astro  (READ-ONLY — nicht aendern):
interface Props { id: string; }
// vollstaendig datengetrieben ueber die data-Attribute der Karten, keine Video-Anzahl
// fest codiert.

From site/src/styles/app.css (Zeile ~936):
.app-video-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
// Direkt darueber steht ein Kommentar, der die 220px mit "die vier Tutorials" begruendet.
// Zeile ~1132: @media (max-width: 640px) { .app-video-grid { grid-template-columns: 1fr; } }  -> UNVERAENDERT lassen.

From tests/unit/test_site_anleitung_content.py:
EXPECTED_VIDEO_IDS: set[str]                       # aktuell die 4 alten IDs, hart kodiert
def test_video_ids_are_complete() -> None          # ids aus videos.ts == EXPECTED_VIDEO_IDS
def test_every_video_has_a_title() -> None         # Anzahl an len(EXPECTED_VIDEO_IDS) gekoppelt, passt sich automatisch an
def test_legacy_design_notice_matches_the_data() -> None
  # any_legacy = "legacyDesign: true" in _videos_array()
  # if not any_legacy: pytest.fail("Kein Video mehr als legacyDesign markiert — Hinweis in
  #   VideoGrid.astro und diesen Test entfernen.")
  # -> schlaegt zwingend fehl, sobald legacyDesign aus videos.ts verschwindet: Test loeschen.
def _videos_array() -> str                         # Helper, unveraendert lassen
# `import pytest` bleibt noetig (@pytest.fixture sections), `SITE` bleibt noetig.
</interfaces>

Key files:
@site/src/data/videos.ts — primaerer Aenderungsort, das `videos`-Array wird ersetzt
@site/src/styles/app.css — `.app-video-grid` (Zeile ~936) + der Kommentar darueber
@tests/unit/test_site_anleitung_content.py — Guard-Test, bricht CI ohne Anpassung

READ-ONLY (nicht anfassen, kein Diff erwuenscht):
@site/src/components/VideoGrid.astro — Legacy-Hinweis ist bereits datengetrieben bedingt
@site/src/components/VideoModal.astro — generisch ueber data-Attribute
@site/src/pages/anleitung/index.astro — konsumiert nur `videos`
@site/src/pages/templates/[...id].astro — zweiter Renderort desselben `VideoGrid`, profitiert automatisch mit

Umgebungshinweise (aus RESEARCH.md, verifiziert):
- `pytest` liegt NICHT auf dem Standard-PATH — immer `/root/.local/bin/pytest` verwenden.
- `python3 -c "import pytest"` schlaegt fehl (System-Python kennt pytest nicht). Deshalb
  KEIN `python3 -m unittest discover tests/unit` als zweites Gate: die Testdatei
  importiert pytest auf Modulebene und CI faehrt fuer `tests/unit/` ausschliesslich
  pytest (`.github/workflows/ci.yml:75`). `python3 -m unittest discover` laeuft in diesem
  Repo nur gegen `tools/sla_lib/tests` (`.github/workflows/pages.yml:106`) — von diesem
  Issue nicht beruehrt.
- `site/node_modules` ist im Worktree bereits installiert; `npm --prefix site run build`
  laeuft ohne weitere Vorbereitung (Baseline vor der Aenderung: 26 Seiten, gruen).
- `site/dist/` ist gitignored (`site/.gitignore:2`) — Build-Artefakte werden nie committet.
- Kein Vendoring: YouTube-Thumbnails und -Embeds bleiben remote referenziert, es wird
  kein Asset ins Repo kopiert.
</context>

<commit_format>
Format: conventional mit Issue-Prefix (aus `.issues/config.yaml`: `format: conventional`,
`prefix: true`; Issue-ID `imtas`).
Beispiel: `imtas: feat(site): replace Anleitung videos with the two new recordings`
Pattern: `imtas: {type}({scope}): {description}`
Typen: feat, fix, test, refactor, docs, chore. Scope hier sinnvoll: `site` bzw. `tests`.
Commit-Messages auf Englisch, keinerlei Werkzeug-Attribution (kein "Claude", kein
"Generated with", kein `Co-Authored-By`).
</commit_format>

<tasks>

<task type="auto">
  <name>Task 1: videos.ts auf die zwei neuen Scribus-Videos umstellen</name>
  <files>site/src/data/videos.ts</files>
  <action>
  In `site/src/data/videos.ts` das gesamte `export const videos`-Array (aktuell vier
  Eintraege, alle mit `legacyDesign: true`) durch exakt diesen Block ersetzen — woertlich,
  inklusive Reihenfolge, Anfuehrungszeichen und Trailing Commas:

  export const videos: AnleitungsVideo[] = [
    {
      youtube: 'SDT9eM9tReU',
      title: 'Erste Schritte mit Scribus',
      duration: '14:38',
    },
    {
      youtube: '3rMFX_VLvpE',
      title: 'Export einer Scribus Datei',
      duration: '8:39',
    },
  ];

  Regeln dazu:
  - KEIN `legacyDesign` bei einem der beiden Eintraege — das ist der Schalter, der den
    Hinweis "im alten Design aufgenommen" in `VideoGrid.astro` abschaltet.
  - KEIN `poster` setzen: `posterFor()` leitet das Bild aus der Video-ID ab
    (`maxresdefault`, mit `hqdefault`-Fallback). Kein eigenes Bild, kein Download eines
    Thumbnails ins Repo (Vendoring-Verbot).
  - KEIN `description` erfinden.
  - Die Laufzeiten sind verifiziert (YouTube `lengthSeconds`: 878 = 14:38, 519 = 8:39) —
    nicht weglassen und nicht veraendern. Damit ist die als LOW confidence markierte
    offene Frage aus RESEARCH.md beantwortet.
  - Der Titel des zweiten Videos lautet exakt "Export einer Scribus Datei" (ohne
    Bindestrich, nicht "PDF-Export einer Scribus-Datei" wie beim alten Video).
  - Interface `AnleitungsVideo` unveraendert lassen, insbesondere das Feld
    `legacyDesign?: boolean` samt Doc-Kommentar NICHT entfernen — es bleibt der
    Mechanismus fuer kuenftige Alt-Aufnahmen.
  - Den Datei-Kopfkommentar unveraendert lassen (er beschreibt weiterhin korrekt, wie
    Videos ergaenzt/getauscht werden; die Beispiel-ID `dQw4w9WgXcQ` darin bleibt stehen,
    der Guard-Test schneidet bewusst nur den Array-Body aus).
  - `VideoGrid.astro` und `VideoModal.astro` NICHT anfassen.

  Erwartet: `pytest tests/unit/test_site_anleitung_content.py` ist nach diesem Task ROT
  (alte IDs erwartet, `test_legacy_design_notice_matches_the_data` failt absichtlich).
  Das ist der geplante Zwischenzustand und wird in Task 2 aufgeloest — hier nicht
  "reparieren", indem `legacyDesign` wieder gesetzt wird.

  Commit: `imtas: feat(site): replace Anleitung videos with the two new recordings`
  </action>
  <verify>
  <automated>
npm --prefix site run build
python3 - <<'PY'
import pathlib, re
html = pathlib.Path("site/dist/anleitung/index.html").read_text(encoding="utf-8")
ids = re.findall(r'data-video-id="([^"]+)"', html)
assert ids == ["SDT9eM9tReU", "3rMFX_VLvpE"], ids
assert "Aufnahmen zeigen noch das alte" not in html, "Legacy-Hinweis wird noch gerendert"
for vid in ids:
    assert 'href="https://www.youtube.com/watch?v=%s"' % vid in html, vid
assert "14:38" in html and "8:39" in html, "Laufzeiten fehlen auf den Karten"
print("Task 1 OK")
PY
  </automated>
  </verify>
  <done>
  - `site/src/data/videos.ts` enthaelt genau zwei Eintraege: `SDT9eM9tReU` / "Erste Schritte mit Scribus" / '14:38' und `3rMFX_VLvpE` / "Export einer Scribus Datei" / '8:39'
  - Keine Vorkommen von `legacyDesign: true` mehr im `videos`-Array
  - `AnleitungsVideo`-Interface inkl. `legacyDesign?: boolean` unveraendert
  - `npm --prefix site run build` laeuft gruen durch
  - Das gebaute `site/dist/anleitung/index.html` enthaelt genau zwei `data-video-id`-Karten mit den neuen IDs, die passenden watch-URLs und keinen Alt-Design-Hinweis
  - `git status` zeigt nur `site/src/data/videos.ts` als geaendert
  </done>
</task>

<task type="auto">
  <name>Task 2: Guard-Test auf die zwei neuen Video-IDs umstellen</name>
  <files>tests/unit/test_site_anleitung_content.py</files>
  <action>
  Zwei Aenderungen in `tests/unit/test_site_anleitung_content.py`, sonst nichts:

  1. Konstante `EXPECTED_VIDEO_IDS` samt Kommentar darueber ersetzen. Aktuell:

     # The four Scribus tutorials that lived on the GGS page. Kept explicit: if
     # one is dropped or swapped, that should be a deliberate edit here too.
     EXPECTED_VIDEO_IDS = {
         "ZH9z7Cgiuy0",  # Erste Schritte mit Scribus
         "GxKJLRHjvIs",  # Bilder einfügen und verschieben in Scribus
         "uBMazvTPPLI",  # PDF-Export einer Scribus-Datei
         "90rbNKbOlMM",  # Besonderheiten bei der Flyerbearbeitung
     }

     Neu — woertlich so:

     # The two Scribus tutorials recorded in the current design. Kept explicit: if
     # one is dropped or swapped, that should be a deliberate edit here too.
     EXPECTED_VIDEO_IDS = {
         "SDT9eM9tReU",  # Erste Schritte mit Scribus
         "3rMFX_VLvpE",  # Export einer Scribus Datei
     }

  2. Die Funktion `test_legacy_design_notice_matches_the_data` vollstaendig entfernen —
     Signatur, Docstring und Body, inklusive der davor stehenden Leerzeilen, sodass keine
     doppelten Leerzeilen zurueckbleiben. Das ist genau die Handlungsanweisung aus der
     eigenen Fail-Message des Tests ("Kein Video mehr als legacyDesign markiert — Hinweis
     in VideoGrid.astro und diesen Test entfernen"). Der Hinweis-Block in
     `VideoGrid.astro` bleibt dabei stehen (ISSUE.md erlaubt das ausdruecklich) — nur der
     Test verschwindet.

  Nicht aendern:
  - `test_video_ids_are_complete` und `test_every_video_has_a_title` bleiben unveraendert;
    beide sind ueber `EXPECTED_VIDEO_IDS` bzw. dessen Laenge automatisch mitgezogen.
  - Der Helper `_videos_array()`, die `sections`-Fixture und alle Tests im Abschnitt
    "Anleitungs-Abschnitte" bleiben unveraendert.
  - `import pytest` bleibt stehen (wird weiterhin von `@pytest.fixture` gebraucht),
    ebenso die Konstante `SITE` (wird von `ANLEITUNG_DIR`, `VIDEOS_TS`, `PUBLIC`
    verwendet). Keine ungenutzten Imports zuruecklassen und keine benutzten entfernen.
  - Keine neuen Tests hinzufuegen.

  Nach diesem Task laeuft die Datei mit 7 statt 8 Tests, alle gruen.

  Commit: `imtas: test(site): point the Anleitung video guard at the new recordings`
  </action>
  <verify>
  <automated>
/root/.local/bin/pytest tests/unit/test_site_anleitung_content.py -q
/root/.local/bin/pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py
grep -c "legacyDesign" tests/unit/test_site_anleitung_content.py || echo "keine legacyDesign-Referenz mehr im Test - erwartet"
  </automated>
  </verify>
  <done>
  - `EXPECTED_VIDEO_IDS` enthaelt genau `{"SDT9eM9tReU", "3rMFX_VLvpE"}` mit den passenden Titel-Kommentaren
  - `test_legacy_design_notice_matches_the_data` existiert nicht mehr in der Datei
  - `/root/.local/bin/pytest tests/unit/test_site_anleitung_content.py -q` meldet 7 passed
  - Der volle CI-Lauf `/root/.local/bin/pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py` ist gruen
  - `git status` zeigt ausser der Testdatei keine weiteren Aenderungen in diesem Commit
  </done>
</task>

<task type="auto">
  <name>Task 3: Video-Grid auf auto-fit mit Kartenobergrenze umstellen</name>
  <files>site/src/styles/app.css</files>
  <action>
  In `site/src/styles/app.css` (Bereich `.app-video-grid`, aktuell Zeile ~934-939) den
  Kommentar und die Grid-Regel ersetzen. Aktuell:

    /* 220px Mindestbreite, damit die vier Tutorials auf Desktop-Breite in
       einer Reihe stehen — so lagen sie auch auf der GGS-Seite. */
    .app-video-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 1.5rem;
      margin-top: 1.5rem;
    }

  Neu — woertlich so:

    /* 220px Mindest-, 320px Maximalbreite pro Karte. `auto-fit` (nicht
       `auto-fill`) laesst leere Spuren kollabieren, damit die zwei Tutorials
       nebeneinander stehen statt in einem halbleeren Raster; die Obergrenze
       verhindert, dass zwei Karten auf breiten Viewports auseinandergezogen
       werden. */
    .app-video-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 320px));
      gap: 1.5rem;
      margin-top: 1.5rem;
    }

  Regeln dazu:
  - Nur dieser eine Regelblock plus der Kommentar darueber wird angefasst. Alle anderen
    `.app-video-*`-Regeln (`.app-video-notice`, `.app-video-card`, `.app-video-card__media`,
    `__play`, `__duration`, `__body`, `__title`, `__desc`) bleiben unveraendert.
  - Der Mobile-Breakpoint `@media (max-width: 640px) { .app-video-grid { grid-template-columns: 1fr; } }`
    (Zeile ~1132) bleibt unveraendert — auf Handybreite ist eine Spalte weiterhin richtig.
  - Andere Grids in der Datei (`auto-fill`-Regeln in den Zeilen ~175, 199, 311, 342, 447,
    452, 577, 881) NICHT mit umstellen — die haben andere Item-Zahlen und sind nicht Teil
    dieses Issues.
  - Werte nicht "verbessern": 220px/320px sind die aus der Recherche uebernommenen
    Zielwerte, nicht Verhandlungsmasse.

  Commit: `imtas: fix(site): collapse empty video grid tracks for the two-card layout`
  </action>
  <verify>
  <automated>
npm --prefix site run build
python3 - <<'PY'
import pathlib, re
css = pathlib.Path("site/src/styles/app.css").read_text(encoding="utf-8")
m = re.search(r"\.app-video-grid \{(.*?)\}", css, re.S)
assert m, ".app-video-grid nicht gefunden"
block = m.group(1)
assert "repeat(auto-fit, minmax(220px, 320px))" in block, block
assert "auto-fill" not in block, "auto-fill steht noch in .app-video-grid"
assert "vier Tutorials" not in css, "Kommentar spricht noch von vier Tutorials"
assert "grid-template-columns: 1fr" in css, "Mobile-Breakpoint fehlt"
print("Task 3 OK")
PY
  </automated>
  </verify>
  <done>
  - `.app-video-grid` nutzt `grid-template-columns: repeat(auto-fit, minmax(220px, 320px))`
  - Der Kommentar darueber begruendet die neuen Werte und spricht nicht mehr von "vier Tutorials"
  - Der 640px-Breakpoint fuer `.app-video-grid` ist unveraendert (`1fr`)
  - Keine andere `auto-fill`-Regel in `app.css` wurde geaendert
  - `npm --prefix site run build` laeuft gruen durch
  </done>
</task>

<task type="auto">
  <name>Task 4: Gesamtverifikation gegen die Akzeptanzkriterien</name>
  <files>site/src/data/videos.ts, site/src/styles/app.css, tests/unit/test_site_anleitung_content.py</files>
  <action>
  Kein neuer Code. Abschliessend pruefen, dass die drei Aenderungen zusammen alle
  Akzeptanzkriterien aus ISSUE.md erfuellen und der Diff sauber ist:

  1. Frischen Build erzeugen und sowohl `/anleitung/` als auch eine Vorlagen-Detailseite
     (zweiter Renderort desselben `VideoGrid`, in ISSUE.md nicht erwaehnt, aber
     automatisch mitbetroffen) gegen die Kriterien pruefen: genau zwei Karten, korrekte
     Titel, watch-URLs als no-JS-Fallback, `data-video-target`/`data-video-id` als
     Modal-Trigger, kein Alt-Design-Hinweis.
  2. Die Testsuite exakt so fahren, wie CI es tut
     (`.github/workflows/ci.yml:75`): `pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py`,
     mit dem vollen Pfad `/root/.local/bin/pytest`.
  3. `git status` und `git diff --stat` pruefen: geaendert sein duerfen ausschliesslich
     `site/src/data/videos.ts`, `site/src/styles/app.css` und
     `tests/unit/test_site_anleitung_content.py`. Insbesondere duerfen
     `site/src/components/VideoGrid.astro` und `site/src/components/VideoModal.astro`
     KEINEN Diff haben, und `site/dist/` darf nicht im Git-Status auftauchen
     (gitignored).

  Falls eine Assertion fehlschlaegt: die Ursache in dem Task beheben, zu dem sie gehoert
  (Daten -> Task 1, Test -> Task 2, CSS -> Task 3), nicht die Assertion abschwaechen.

  Kein eigener Commit noetig, sofern nichts nachzubessern war. Falls doch:
  `imtas: fix(site): <konkrete Nachbesserung>`.
  </action>
  <verify>
  <automated>
npm --prefix site run build
/root/.local/bin/pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py
python3 - <<'PY'
import pathlib, re
EXPECTED = ["SDT9eM9tReU", "3rMFX_VLvpE"]
TITLES = ["Erste Schritte mit Scribus", "Export einer Scribus Datei"]
pages = [pathlib.Path("site/dist/anleitung/index.html")]
pages += sorted(pathlib.Path("site/dist/templates").glob("*/index.html"))[:1]
for page in pages:
    html = page.read_text(encoding="utf-8")
    ids = re.findall(r'data-video-id="([^"]+)"', html)
    assert ids == EXPECTED, (page, ids)
    assert html.count('data-video-target="') == 2, (page, "Modal-Trigger fehlen")
    for vid in EXPECTED:
        assert 'href="https://www.youtube.com/watch?v=%s"' % vid in html, (page, vid)
        assert 'https://i.ytimg.com/vi/%s/maxresdefault.jpg' % vid in html, (page, vid)
    for title in TITLES:
        assert title in html, (page, title)
    assert "Aufnahmen zeigen noch das alte" not in html, (page, "Alt-Design-Hinweis")
    assert "ZH9z7Cgiuy0" not in html and "90rbNKbOlMM" not in html, (page, "Alt-Video-ID")
print("Akzeptanzkriterien OK:", ", ".join(str(p) for p in pages))
PY
git status --porcelain
git diff --stat HEAD -- site/src/components/
  </automated>
  </verify>
  <done>
  - `npm --prefix site run build` gruen (26 Seiten)
  - `/root/.local/bin/pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py` gruen
  - `/anleitung/` und die geprueften Vorlagen-Detailseiten zeigen genau zwei Karten mit den neuen Titeln, korrekten watch-URLs, YouTube-Postern und Modal-Triggern
  - Nirgends im Build erscheint der Alt-Design-Hinweis oder eine der vier alten Video-IDs
  - `git diff --stat HEAD -- site/src/components/` ist leer (VideoGrid/VideoModal unangetastet)
  - `git status --porcelain` listet keine Dateien ausserhalb der drei geplanten
  </done>
</task>

</tasks>

<verification>
Abschliessende Pruefungen von der Worktree-Wurzel aus:
- `npm --prefix site run build` — Astro-Build muss gruen sein (Baseline: 26 Seiten)
- `/root/.local/bin/pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py` — identisch zu `.github/workflows/ci.yml:75`
- HTML-Assertion aus Task 4 gegen `site/dist/anleitung/index.html` und eine Vorlagen-Detailseite
- `git status --porcelain` — nur `site/src/data/videos.ts`, `site/src/styles/app.css`, `tests/unit/test_site_anleitung_content.py`
- Kein `python3 -m unittest discover tests/unit` — die Testdatei importiert pytest auf
  Modulebene und CI faehrt fuer `tests/unit/` ausschliesslich pytest; unittest discover
  laeuft in diesem Repo nur gegen `tools/sla_lib/tests` (hier nicht beruehrt).
</verification>

<success_criteria>
Abgeleitet 1:1 aus den Akzeptanzkriterien in ISSUE.md:
- `/anleitung/` zeigt genau zwei Video-Karten mit den Titeln "Erste Schritte mit Scribus" und "Export einer Scribus Datei" (verifiziert ueber `data-video-id`-Zaehlung und Titel-Assertion im gebauten HTML)
- Der Hinweis auf das alte Design erscheint nirgends mehr — weder auf `/anleitung/` noch auf den Vorlagen-Detailseiten (`legacyDesign` ist in `videos.ts` nirgends mehr gesetzt)
- Beide Karten tragen `data-video-target`/`data-video-id` als Modal-Trigger, und der no-JS-Fallback-Link zeigt auf `https://www.youtube.com/watch?v=SDT9eM9tReU` bzw. `.../watch?v=3rMFX_VLvpE`
- Zwei Karten sitzen sauber im Grid: `.app-video-grid` nutzt `repeat(auto-fit, minmax(220px, 320px))`, leere Spuren kollabieren, Mobile-Breakpoint unveraendert
- Build laeuft durch: `npm --prefix site run build` gruen
- Zusaetzlich (aus der Recherche, nicht im Issue-Text): `pytest tests/unit/` bleibt gruen, `EXPECTED_VIDEO_IDS` steht auf den zwei neuen IDs, `test_legacy_design_notice_matches_the_data` ist entfernt
- `VideoGrid.astro` und `VideoModal.astro` sind unveraendert
</success_criteria>
