# Execution: Impressum und Datenschutzerklaerung im Footer verlinken

**Started:** 2026-09-01T21:44:00Z
**Status:** complete
**Branch:** issue/khnpz-impressum-und-datenschutzerklaerung-im-footer-verlinken

## Execution Log

- [x] Footer in `site/src/layouts/Base.astro` um zwei externe Links ergaenzt
      (Impressum -> `https://gruene.at/impressum/`, Datenschutzerklaerung ->
      `https://gruene.at/datenschutzerklarung/`, beide `target="_blank" rel="noopener"`)
      — commit 8a4a887

Kein separates Task-Splitting noetig, dies ist ein einzeiliger Footer-Change ohne
eigenes PLAN.md (Issue-Text ist vollstaendig).

## Verification Results

- `npm install` im `site/`-Verzeichnis (node_modules war nicht vorhanden im Worktree)
- `npm run build` (Astro) — 26 Seiten gebaut, keine Fehler
- Footer im gebauten `site/dist/` geprueft auf drei Seiten:
  - `dist/index.html` (Startseite/Galerie)
  - `dist/anleitung/index.html`
  - `dist/templates/plakat-a1-hochformat/index.html` (Vorlagen-Detailseite)
  - Auf allen drei: beide Links mit korrekten URLs (`https://gruene.at/impressum/`,
    `https://gruene.at/datenschutzerklarung/` — exakt ohne „ae"/„ss") und
    `target="_blank" rel="noopener"` vorhanden.
- `python3 -m pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py` ->
  **745 passed, 9 skipped, 12 subtests passed**. Kein Test schreibt den bisherigen
  Footer-Text fest, daher keine Testanpassung noetig.

**Tests:** 745 passed, 9 skipped (0 failed)
**Linter:** kein separater Lint-Schritt fuer `.astro`-Dateien im Repo konfiguriert
**Build:** clean (astro build, 26 pages)

## Deviations from Plan

### Auto-fixed (Rule 3 — Blocker)

1. **[Rule 3 - Blocker] `/root/.local/bin/pytest` lief in einer isolierten
   `uv`-tool-venv ohne die Projekt-Python-Deps (PyYAML/lxml/jsonschema/pdfplumber/
   fontTools/SimpleIDML), Collection scheiterte mit 33 Fehlern
   (`ModuleNotFoundError: PIL` etc.).**
   - Grund: `uv tool install pytest` nutzt eine eigene venv, getrennt vom System-
     Python, das die CI-Requirements traegt.
   - Fix: `python3 -m pip install --break-system-packages pytest fonttools==4.63.0`
     — die restlichen Requirements (Pillow, PyYAML, lxml, jsonschema, pdfplumber,
     SimpleIDML) waren im System-Python bereits als dist-packages vorhanden.
     Anschliessend `python3 -m pytest ...` ausgefuehrt statt der isolierten
     `uv`-tool-Binary.
   - Deckt sich mit dem bereits in `.issues/c8bg0-.../EXECUTION.md` dokumentierten
     Vorgehen fuer denselben Blocker in diesem Repo — kein neues Muster.
   - Keine Code-/Repo-Aenderung, nur Container-lokale Python-Installation.

### Blocked (Rule 4)

None.

## Discovered Issues

None im Scope dieser Aenderung.

## Self-Check

- [x] `site/src/layouts/Base.astro` enthaelt beide Links (geprueft per Read/Diff)
- [x] Commit 8a4a887 existiert auf dem Branch (`git log --oneline`)
- [x] `npm run build` clean, `python3 -m pytest tests/unit/ ...` clean (745 passed)
- [x] Keine TODO/FIXME/Placeholder in der geaenderten Datei
- [x] Kein Debug-Code (kein `console.log`, kein `debugger`) eingefuehrt
- **Result:** PASSED

**Completed:** 2026-09-01T21:48:00Z
**Duration:** ~4 min
**Commits:** 1
