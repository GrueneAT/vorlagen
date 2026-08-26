---
id: cg83g
title: Fotosammlung auf der Anleitungsseite als NOe-only kennzeichnen
status: done
priority: medium
labels:
- documentation
remote:
- source: github
  id: '158'
  url: https://github.com/GrueneAT/vorlagen/issues/158
---

Auf der Anleitungsseite steht die Fotosammlung als allgemeiner Punkt. Sie liegt
aber im Gemeindegruppenservice der Gruenen Niederoesterreich und ist nur fuer
NOe zugaenglich — aus dem Text geht das nicht hervor, nur das „(GGS NOe, Login
noetig)" im Link-Label. Rueckmeldung aus dem Anwenderfeedback: dazuschreiben, dass
das nur fuer NOe gilt, damit klar ist, dass nicht alle Zugriff haben.

## Was zu tun ist

`site/src/content/anleitung/06-fotosammlung.md`:

- Im Titel oder direkt im ersten Satz kennzeichnen, dass die Sammlung nur fuer
  Niederoesterreich ist (z. B. Titel „Fotosammlung fuer eure Druckwerke (nur
  NOe)").
- Im Text sagen, dass der Zugang ueber den GGS NOe laeuft und ein Login der
  Gruenen Niederoesterreich noetig ist — Gruppen ausserhalb NOes koennen die
  Sammlung nicht nutzen.
- Wenn die Anleitungsseite dafuer ein Callout/Hinweis-Muster hat, das nutzen
  statt Fliesstext (DS-Callout), damit der Hinweis nicht ueberlesen wird.

## Akzeptanzkriterien

- [ ] Auf `/anleitung/` ist ohne Klick erkennbar, dass die Fotosammlung nur
      fuer Niederoesterreich ist
- [ ] Der Login-Hinweis steht im Text, nicht nur im Link-Label
- [ ] Build laeuft durch

## Constraints

- Reine Content-Aenderung, keine neuen Komponenten noetig
- Conventional Commit, keine Werkzeug-Attribution
