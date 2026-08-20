/**
 * Video-Anleitungen für die Arbeit mit Scribus.
 *
 * Übernommen aus der GGS-NÖ-Seite "Scribus – Druckvorlagen & Downloads",
 * die diese Site vollständig ersetzt. Dort lagen die Videos als
 * Kadence-Video-Popups mit Screenshot-Postern; hier kommen Titel und
 * Laufzeit aus YouTube selbst, das Poster vom YouTube-Thumbnail-CDN.
 *
 * ---- Video hinzufügen / austauschen ----------------------------------
 * Ein Eintrag = eine Karte auf /anleitung/. Reihenfolge im Array =
 * Reihenfolge im Grid. Nötig ist nur `youtube` + `title`:
 *
 *   { youtube: 'dQw4w9WgXcQ', title: 'Neues Video' }
 *
 * `poster` nur setzen, wenn das YouTube-Thumbnail nicht passt (z.B. ein
 * eigener Screenshot unter site/public/). Sonst wird es aus der Video-ID
 * abgeleitet — siehe posterFor().
 * ---------------------------------------------------------------------
 */

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
  /**
   * true = im alten Corporate Design aufgenommen. Blendet über dem Grid
   * den Hinweis ein, dass die Optik veraltet, der gezeigte Ablauf aber
   * weiterhin korrekt ist.
   *
   * Bewusst pro Video statt global: sobald ein Video neu aufgenommen ist,
   * fällt hier das Flag weg — und wenn keines mehr gesetzt ist,
   * verschwindet der Hinweis von selbst.
   */
  legacyDesign?: boolean;
}

/**
 * Poster-URL für ein Video. `maxresdefault` liefert 16:9 in voller
 * Auflösung, existiert aber nicht für jedes Video — die Karte fällt im
 * Fehlerfall per onerror auf `hqdefault` zurück (immer vorhanden).
 */
export function posterFor(v: AnleitungsVideo): string {
  return v.poster ?? `https://i.ytimg.com/vi/${v.youtube}/maxresdefault.jpg`;
}

/** Fallback-Poster, wenn posterFor() 404 liefert. */
export function posterFallbackFor(v: AnleitungsVideo): string {
  return `https://i.ytimg.com/vi/${v.youtube}/hqdefault.jpg`;
}

/** Watch-URL — no-JS-Fallback des Karten-Links. */
export function watchUrl(v: AnleitungsVideo): string {
  return `https://www.youtube.com/watch?v=${v.youtube}`;
}

export const videos: AnleitungsVideo[] = [
  {
    youtube: 'ZH9z7Cgiuy0',
    title: 'Erste Schritte mit Scribus',
    legacyDesign: true,
    duration: '17:52',
  },
  {
    youtube: 'GxKJLRHjvIs',
    title: 'Bilder einfügen und verschieben in Scribus',
    legacyDesign: true,
    duration: '14:45',
  },
  {
    youtube: 'uBMazvTPPLI',
    title: 'PDF-Export einer Scribus-Datei',
    legacyDesign: true,
    duration: '6:54',
  },
  {
    youtube: '90rbNKbOlMM',
    title: 'Besonderheiten bei der Flyerbearbeitung',
    legacyDesign: true,
    duration: '3:57',
  },
];
