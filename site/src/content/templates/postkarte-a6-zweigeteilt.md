---
id: postkarte-a6-zweigeteilt
version: 0.1.0
build_py_sha256: 03a51260b4b211ca4df4c9145dafd07f57c43e56410d99413c417bed74e9f636
title: Postkarte A6 – Variante 2
format: A6
orientation: portrait
pages: 2
preview_dpi: 100
audience:
- bezirksgruppe
- landesgruppe
- ortsgruppe
description: 'Zweiseitige A6-Kampagnen-Postkarte. Vorderseite zweigeteilt: randabfallendes
  Bildband oben, Botschaft und Call-to-Action auf Grün darunter. Rückseite identisch
  mit Variante 1.'
build:
  script: build.py
  output: template.sla
sla_diff_strict: false
previews_for_sla: ec576d8c0e9cda83fce9d2d6f9186293a57a32e324c65b3711cb688d6ad63a24
brand_overrides:
- id: brand:line_spacing_0.9
  reason: Rueckseite und Styles von postkarte-a6-kampagne uebernommen (dort aus postkarte-vorlage-original.sla
    erzeugt); the original's per-template para-styles drift from Quickguide 0.9 factor
    (e.g. Fließtext 13/12=1.083, Headline sehr wichtig 23/27=0.85). Round- trip diff
    (tools/sla_diff.py --strict) is the byte-stable contract for this template; tightening
    linesp would break round-trip.
- id: brand:visual_adjacency_drift
  reason: 'Per-template alignment encoding scheduled for the #22 follow-up. Spine-safety
    is a no-op (single-page-per-side template) and the new rule infrastructure ships
    globally in #22; CONSTRAINTS encoding for this template is deferred (Issue #22
    locked decision #12). Issue #23 renamed brand:undeclared_alignment_drift -> brand:visual_adjacency_drift.'
- id: brand:image_text_overlap
  reason: 'Scheduled for follow-up audit per #23 — caption-on-photo / decorative overlaps
    audited at time of #23, not yet reviewed for fix-vs-override classification.'
- id: brand:image_fills_frame
  reason: 'Scheduled for follow-up audit per #24 — image-fills-frame check added in
    #24 surfaces letterbox/INJECT_MAP-drift class globally; per-template review for
    fix-vs-override classification deferred to follow-up issue (#25). Zeitung is the
    only template with verified clean image-content extents post-#24.'
- id: brand:band_consistency
  reason: 'Scheduled for follow-up audit per #25 — band-consistency check added in
    #25 needs per-template body_block_margins spec authoring; deferred to follow-up
    issue. Zeitung is the only template with verified body-pool band model post-#25.'
ci_overrides:
  non_ci_styles:
  - Default Paragraph Style
  - Fließtext
  - Impressum
  - Default Paragraph Style (2)
  - Schrift rosa Kreis
  - Headline sehr wichtig
  - Kontaktmöglichkeiten
  - Vollkorn Headline sehr wichtig
  - Unterüberschrift
  non_ci_colors:
  - Green
slots:
  headline:
    type: text
    description: 4-zeilige Hauptbotschaft (Vorderseite, alternierend Weiß/Gelb)
    lines: 4
    max_chars_per_line: 22
    anname: Headline 4-zeilig (Brand-Wechselfarbe)
  cta:
    type: text
    description: Call-to-Action unter Headline (1 Zeile)
    anname: CTA
  stoerer:
    type: text
    description: 3-zeiliger Störer-Text im Magenta-Kreis
    lines: 3
    anname: Störer-Text 3-zeilig
  body:
    type: text
    description: Erklärtext auf der Rückseite
    multiline: true
    anname: Erklärtext Rückseite
  url:
    type: text
    description: Kampagnen-URL unterm QR-Code
    pattern: ^https?://
    anname: Kampagnen-URL
  social:
    type: text
    description: Social-Handles (4 Zeilen)
    lines: 4
    anname: Social Handles (4-zeilig)
  impressum:
    type: text
    description: Impressum-Block, gesetzlich vorgeschrieben
    multiline: true
    anname: Impressum (1-zeilig)
  hero:
    type: image
    description: Bildband auf der Vorderseite (randabfallend, oberes Drittel)
    anname: P1 Hero
  logo:
    type: image
    description: Grünen-Logo (Vorderseite, rechts unten)
    source: shared/logos/gruene-weiss.png
    anname: Logo Grüne (weiss, zentriert)
  qr:
    type: image
    description: QR-Code zum Kampagnen-URL (kann manuell eingefügt werden)
    anname: QR-Code (wird aus URL generiert)
preflight:
  bleed_mm: 3
  cmyk_only: true
  min_image_dpi: 300
category: postkarte
category_label: Postkarten
variant_label: Variante 2
_downloads:
- label: Burgenland
  bundesland: bgld
  sla: /templates/postkarte-a6-zweigeteilt/impressum/bgld.sla
- label: Kärnten
  bundesland: ktn
  sla: /templates/postkarte-a6-zweigeteilt/impressum/ktn.sla
- label: Niederösterreich
  bundesland: noe
  sla: /templates/postkarte-a6-zweigeteilt/impressum/noe.sla
- label: Oberösterreich
  bundesland: ooe
  sla: /templates/postkarte-a6-zweigeteilt/impressum/ooe.sla
- label: Salzburg
  bundesland: sbg
  sla: /templates/postkarte-a6-zweigeteilt/impressum/sbg.sla
- label: Steiermark
  bundesland: stmk
  sla: /templates/postkarte-a6-zweigeteilt/impressum/stmk.sla
- label: Tirol
  bundesland: tirol
  sla: /templates/postkarte-a6-zweigeteilt/impressum/tirol.sla
- label: Vorarlberg
  bundesland: vbg
  sla: /templates/postkarte-a6-zweigeteilt/impressum/vbg.sla
- label: Wien
  bundesland: wien
  sla: /templates/postkarte-a6-zweigeteilt/impressum/wien.sla
_preview_pdf: /templates/postkarte-a6-zweigeteilt/preview.pdf
_previews:
- label: Seite 1
  src: /templates/postkarte-a6-zweigeteilt/page-01.png
- label: Seite 2
  src: /templates/postkarte-a6-zweigeteilt/page-02.png
---

# So nutzt du die Postkarten-Vorlage (Variante 2)

Eine zweiseitige A6-Postkarte für Kampagnen, Petitionen und Events. Die
Vorderseite ist zweigeteilt: oben ein randabfallendes Bildband, darunter auf
grünem Grund die Botschaft und der Call-to-Action. Die Rückseite ist identisch
mit Variante 1.

Wenn du keine Bildfläche willst, nimm **Variante 1** — dort besteht die
Vorderseite nur aus dem grünen Hintergrund und dem Text.

## Schritt für Schritt

1. **Vorlage öffnen** — `template.sla` mit [Scribus](https://www.scribus.net/downloads/)
   öffnen (kostenlos für Windows, macOS und Linux). Die Schriften vorher
   installieren.
2. **Bild einsetzen** — den leeren Bildrahmen oben (`P1 Hero`) anklicken und
   über *Datei → Importieren → Bild laden* dein eigenes Motiv einsetzen. Der
   Rahmen läuft absichtlich über den Seitenrand hinaus (Anschnitt) — das Bild
   sollte ihn vollständig füllen.
3. **Inhalte ersetzen** — Texte überschreiben, Logo bei Bedarf tauschen. Die
   Rahmen sind beschriftet: ein Klick zeigt unten rechts den Namen, z. B.
   „Headline", „Störer-Text", „Erklärtext Rückseite" oder „Kampagnen-URL".
4. **QR-Code einsetzen** — den Platzhalter „QR-Code" auf der Rückseite durch
   dein eigenes QR-Bild ersetzen (deine Kampagnen-URL). Die URL darunter im
   Textfeld anpassen.
5. **Impressum prüfen** — der einzeilige Impressums-Block ist gesetzlich
   vorgeschrieben. Angaben ergänzen, nicht löschen.
6. **Als PDF exportieren** — *Datei → Exportieren → Als PDF speichern*. Fertig
   für die Druckerei.

> Die pinken Beschriftungen „Vorderseite" / „Rückseite" am oberen Rand liegen
> auf dem Hilfslinien-Layer und werden nicht gedruckt.
