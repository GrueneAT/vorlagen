---
id: imtas
title: 'Anleitungsseite: neue Scribus-Videos statt der vier Alt-Aufnahmen'
status: open
priority: high
labels:
- documentation
remote:
- source: github
  id: '157'
  url: https://github.com/GrueneAT/vorlagen/issues/157
---

Die vier Video-Anleitungen auf `/anleitung/` sind allesamt im alten Corporate
Design aufgenommen (`legacyDesign: true`, mit entsprechendem Hinweis ueber dem
Grid). Es gibt jetzt zwei Neuaufnahmen im aktuellen Design. Mehr sind nicht
geplant: bei den Bildern gab es zu wenig Erklaerbedarf fuer ein eigenes Video,
und beim Falzflyer ist in den Vorlagen ohnehin schon alles voreingestellt.

## Was zu tun ist

`site/src/data/videos.ts`: das `videos`-Array durch genau diese zwei Eintraege
ersetzen — die vier Alt-Videos fallen ersatzlos weg.

| YouTube-ID | Titel |
|---|---|
| `SDT9eM9tReU` | Erste Schritte mit Scribus |
| `3rMFX_VLvpE` | Export einer Scribus Datei |

- Kein `legacyDesign` mehr setzen. Damit verschwindet der Hinweis „im alten
  Design aufgenommen" automatisch (so ist er gebaut) — der Hinweis-Block darf
  im Markup bleiben, er rendert dann einfach nicht mehr.
- `duration` aus YouTube uebernehmen (optionales Feld, „M:SS").
- Poster kommt automatisch vom YouTube-Thumbnail, kein eigenes Bild noetig.
- Das Grid steht auf vier Spalten (siehe c180fcb) — pruefen, ob zwei Karten
  darin noch gut aussehen, sonst Spaltenzahl anpassen.

## Akzeptanzkriterien

- [ ] `/anleitung/` zeigt genau zwei Video-Karten mit den obigen Titeln
- [ ] Der Hinweis auf das alte Design erscheint nirgends mehr
- [ ] Beide Karten oeffnen das Video-Modal, der no-JS-Fallback-Link zeigt auf
      die richtige watch-URL
- [ ] Zwei Karten sitzen im Grid sauber (kein halbleeres Vier-Spalten-Raster)
- [ ] Build laeuft durch

## Constraints

- Kein Vendoring, YouTube bleibt eingebettet wie bisher
- Conventional Commit, keine Werkzeug-Attribution
