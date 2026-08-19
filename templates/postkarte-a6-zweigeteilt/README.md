# Postkarte A6 – Variante 2 (zweigeteilt)

Zweiseitige A6-Postkarte für Kampagnen, Petitionen, Events. Vorderseite
zweigeteilt (Bildband oben, Text auf Grün darunter) nach dem Vorbild von
Seite 1 des `flyer-a6-hochformat-zweigeteilt`. Rückseite identisch mit
`postkarte-a6-kampagne` (Variante 1).

## Aufbau

`build.py` wurde aus `templates/postkarte-a6-kampagne/build.py` abgeleitet:
Brand, Styles, Seiten-Setup und die komplette Rückseite sind übernommen, nur
der Seiten-0-Block ist neu komponiert. Änderungen an den gemeinsamen Styles
müssen daher in beiden Varianten nachgezogen werden.

Vorderseiten-Geometrie (mm, Seite 105×148 + 3 mm Anschnitt):

| Element              | x     | y     | b     | h    |
|----------------------|-------|-------|-------|------|
| Bildband `P1 Hero`   | -3    | -3    | 111   | 66   |
| Störer-Kreis         | 73.1  | 52.5  | 20.5  | 20.5 |
| Headline (4-zeilig)  | 6.3   | 76    | 92.5  | 34   |
| Call-to-Action       | 17.5  | 110   | 69.9  | 8.4  |
| Logo                 | 76.5  | 120   | 20.5  | 20.9 |

Der Störer-Kreis überlappt die Bild-/Grün-Kante bewusst — wie beim Flyer.

## So nutzt du die Vorlage

Siehe `USAGE.md`.
