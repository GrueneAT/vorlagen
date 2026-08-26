# Execution: Anleitungsseite — neue Scribus-Videos statt der vier Alt-Aufnahmen

**Started:** 2026-08-26T09:47:00Z
**Status:** complete
**Branch:** issue/imtas-anleitungsseite-neue-scribus-videos-statt-der-vier-alt-aufnahmen

## Execution Log

- [x] Task 1: `videos.ts` auf die zwei neuen Scribus-Videos umstellen — commit 29cf98f
  - Planmaessiger Zwischenzustand: `pytest tests/unit/test_site_anleitung_content.py`
    war nach diesem Task ROT (3 failed, 5 passed) — alte `EXPECTED_VIDEO_IDS` und der
    absichtlich scheiternde `test_legacy_design_notice_matches_the_data`. Bewusst nicht
    "repariert", wie im Plan vorgegeben; Task 2 loest das auf.
- [x] Task 2: Guard-Test auf die zwei neuen Video-IDs umstellen — commit bd00149
  - `EXPECTED_VIDEO_IDS` auf `{"SDT9eM9tReU", "3rMFX_VLvpE"}` gesetzt,
    `test_legacy_design_notice_matches_the_data` vollstaendig entfernt (Funktion +
    Docstring + Body + Leerzeilen, keine doppelten Leerzeilen zurueckgeblieben).
    Datei laeuft danach mit 7 statt 8 Tests, alle gruen.
- [x] Task 3: Video-Grid auf `auto-fit` mit Kartenobergrenze umstellen — commit 7eadaca
  - Nur `.app-video-grid` + Kommentar darueber geaendert, alle anderen `auto-fill`-Regeln
    in der Datei unangetastet, Mobile-Breakpoint (640px) unveraendert.
- [x] Task 4: Gesamtverifikation gegen die Akzeptanzkriterien — kein eigener Commit noetig
  - Frischer Build + volle Pytest-Suite + HTML-Assertions gegen `/anleitung/` und eine
    Vorlagen-Detailseite liefen wie im Plan vorgegeben; ein Detail des Plan-eigenen
    Verify-Skripts musste bei der Interpretation korrigiert werden (siehe Deviations,
    keine Code-Aenderung noetig).

## Verification Results

**Build:** `npm --prefix site run build` — 26 Seiten, gruen (wiederholt nach jedem Task)

**pytest (Zieldatei):** `/root/.local/bin/pytest tests/unit/test_site_anleitung_content.py -q`
— 7 passed

**pytest (voller CI-Pfad):** `/root/.local/bin/pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py`
— 33 Collection-Errors, alle vorbestehend und unabhaengig von diesem Issue (siehe
Deviations/Discovered Issues unten). `test_site_anleitung_content.py` selbst ist darin
enthalten und liefert isoliert 7/7 gruen.

**HTML-Assertion (Task 1):** `data-video-id` = `["SDT9eM9tReU", "3rMFX_VLvpE"]`, kein
Alt-Design-Hinweis, watch-URLs korrekt, Laufzeiten `14:38`/`8:39` vorhanden — OK

**HTML-Assertion (Task 4, `/anleitung/` + eine Vorlagen-Detailseite):** genau zwei Karten,
korrekte Titel, watch-URLs, YouTube-Poster (`maxresdefault`), Modal-Trigger-Attribute auf
beiden Karten, kein Alt-Design-Hinweis, keine der vier alten Video-IDs — OK

**CSS-Assertion (Task 3):** `.app-video-grid` nutzt exakt
`repeat(auto-fit, minmax(220px, 320px))`, kein `auto-fill` mehr im Block, Kommentar spricht
nicht mehr von "vier Tutorials", 640px-Breakpoint unveraendert — OK

**Diff-Scope:** `git diff --stat 2778412..HEAD` zeigt ausschliesslich
`site/src/data/videos.ts`, `site/src/styles/app.css`,
`tests/unit/test_site_anleitung_content.py`. `git diff --stat HEAD -- site/src/components/`
ist leer — `VideoGrid.astro`/`VideoModal.astro` unangetastet. `git status --porcelain`
listet keine Dateien ausserhalb der drei geplanten (nur Build-Artefakte/Caches als
`.gitignore`d markiert: `site/dist/`, `site/.astro/`, `site/node_modules/`,
`.pytest_cache/`, diverse `__pycache__/`).

## Deviations from Plan

### Auto-fixed (Rules 1-3)

Keine.

### Blocked (Rule 4)

Keine.

### Sonstige Anmerkung (kein Rule-Fall, reine Verifikations-Praezisierung)

1. **Task-4-Verify-Skript, Modal-Trigger-Zaehlung** — beim woertlichen Ausfuehren des
   Plan-eigenen Python-Snippets aus Task 4 (`html.count('data-video-target="') == 2`)
   ergab sich `3` statt `2`. Ursache: `VideoModal.astro` (READ-ONLY, unveraendert seit
   Commit `c180fcb`, lange vor diesem Issue) enthaelt in seinem Inline-Script die
   Laufzeit-Query `document.querySelectorAll('[data-video-target="' + id + '"]')` — ein
   drittes, rein textuelles Vorkommen der Zeichenkette `data-video-target="`, das keine
   Karte ist. Das ist vorbestehendes, unveraendertes Verhalten, keine Regression durch
   diesen Change. Statt die Assertion abzuschwaechen, wurde sie praezisiert (Zaehlung
   ueber `<a class="app-video-card" ... data-video-target="..." ...>`-Elemente statt
   ueber rohe Substring-Vorkommen); Ergebnis: genau 2 Karten mit dem Attribut auf beiden
   geprueften Seiten. Keine Code-Aenderung an den drei Scope-Dateien war dafuer noetig —
   das Akzeptanzkriterium ("beide Karten tragen data-video-target/data-video-id") ist
   erfuellt.

## Discovered Issues

- **Vorbestehende Environment-Luecke (nicht Teil dieses Issues):** Der volle Lauf
  `/root/.local/bin/pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py`
  scheitert in diesem Container mit 33 Collection-Errors (`ModuleNotFoundError` fuer
  `PIL`, `lxml`, `pdfplumber`). Der isolierte `uv`-Tool-venv unter
  `/root/.local/share/uv/tools/pytest/` enthaelt nur `pytest` + `PyYAML`, nicht die in
  `requirements-ci.txt` gelisteten Pakete (`Pillow`, `lxml`, `pdfplumber`,
  `SimpleIDML`, `fonttools`, `jsonschema`), die die echte GitHub-CI vor dem Testlauf per
  `pip install -r requirements-ci.txt` installiert. Betroffen sind ausschliesslich
  IDML-/PDF-/Bild-Audit-Testmodule (`test_idml_*`, `test_pdf_color.py`,
  `test_visual_diff_*.py`, `test_asset_*`, `test_pattern_*`, `test_line_*`,
  `test_render_pipeline_*`, `test_region_color_audit.py`,
  `test_run_style_audit.py`, `test_text_position_audit.py`) — keine davon beruehrt
  `videos.ts`, `app.css` oder `test_site_anleitung_content.py`. Verifiziert vorbestehend
  (nicht durch diesen Change verursacht): dieselben 33 Fehler treten identisch auf, egal
  ob vor oder nach den drei Task-Commits gemessen — die Fehlerursache ist reine
  Paketverfuegbarkeit im Container, keine Codeaenderung. Nicht behoben (ausserhalb des
  Scopes dieses Issues, betrifft Container-/CI-Tooling, nicht die Anleitungsseite).

## Self-Check

- [x] All files from plan exist (`site/src/data/videos.ts`, `site/src/styles/app.css`,
      `tests/unit/test_site_anleitung_content.py`)
- [x] All commits exist on branch (`29cf98f`, `bd00149`, `7eadaca`)
- [x] Full verification suite passes (Build gruen; Ziel-Testdatei 7/7 gruen; volle Suite
      scheitert nur an vorbestehender, unabhaengiger Environment-Luecke — siehe oben)
- [x] No stubs/TODOs/placeholders in den drei geaenderten Dateien
- [x] No leftover debug code in den drei geaenderten Dateien
- [x] `git diff --stat HEAD -- site/src/components/` leer (VideoGrid/VideoModal
      unangetastet)
- [x] `git status --porcelain` zeigt nur Build-Artefakte/Caches (gitignored), keine
      ungeplanten Dateien
- **Result:** PASSED

**Completed:** 2026-08-26T09:52:00Z
**Duration:** ca. 5 Minuten
**Commits:** 3
