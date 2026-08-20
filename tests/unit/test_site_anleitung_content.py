"""Guards for the /anleitung/ page content taken over from the GGS-NÖ site.

The Astro build itself only fails on broken *code*; it happily ships an
Anleitung whose download link 404s or whose video list lost an entry. These
tests check the sources instead, so a missing asset shows up in CI rather
than on the live site.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
ANLEITUNG_DIR = SITE / "src" / "content" / "anleitung"
VIDEOS_TS = SITE / "src" / "data" / "videos.ts"
PUBLIC = SITE / "public"

# The four Scribus tutorials that lived on the GGS page. Kept explicit: if
# one is dropped or swapped, that should be a deliberate edit here too.
EXPECTED_VIDEO_IDS = {
    "ZH9z7Cgiuy0",  # Erste Schritte mit Scribus
    "GxKJLRHjvIs",  # Bilder einfügen und verschieben in Scribus
    "uBMazvTPPLI",  # PDF-Export einer Scribus-Datei
    "90rbNKbOlMM",  # Besonderheiten bei der Flyerbearbeitung
}


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path.name}: kein YAML-Frontmatter"
    return yaml.safe_load(m.group(1))


@pytest.fixture(scope="module")
def sections() -> list[tuple[Path, dict]]:
    files = sorted(ANLEITUNG_DIR.glob("*.md"))
    assert files, "keine Anleitungs-Abschnitte gefunden"
    return [(p, _frontmatter(p)) for p in files]


# ---------------------------------------------------------------------------
# Videos
# ---------------------------------------------------------------------------
def _videos_array() -> str:
    """Body des `export const videos = [...]`-Arrays.

    Bewusst nur dieser Ausschnitt statt der ganzen Datei — der Doc-Kommentar
    oben enthaelt eine Beispiel-Video-ID, die sonst mitgezaehlt wuerde.
    """
    src = VIDEOS_TS.read_text(encoding="utf-8")
    m = re.search(r"export const videos[^=]*=\s*\[(.*?)\n\];", src, re.S)
    assert m, "videos-Array in videos.ts nicht gefunden"
    return m.group(1)


def test_video_ids_are_complete():
    ids = set(re.findall(r"youtube:\s*'([^']+)'", _videos_array()))
    assert ids == EXPECTED_VIDEO_IDS


def test_every_video_has_a_title():
    entries = re.findall(r"\{\s*youtube:.*?\n\s*\}", _videos_array(), re.S)
    assert len(entries) == len(EXPECTED_VIDEO_IDS)
    for entry in entries:
        assert "title:" in entry, f"Video ohne Titel: {entry}"


def test_legacy_design_notice_matches_the_data():
    """Der Hinweis "im alten Design aufgenommen" haengt am `legacyDesign`-Flag.

    Solange noch ein Video so markiert ist, muss VideoGrid.astro den Hinweis
    rendern. Sind alle Videos neu aufgenommen (kein Flag mehr), muss er
    verschwinden — sonst behauptet die Seite dauerhaft etwas Falsches.
    """
    grid = (SITE / "src" / "components" / "VideoGrid.astro").read_text(encoding="utf-8")
    any_legacy = "legacyDesign: true" in _videos_array()

    assert "hasLegacyDesign" in grid, "VideoGrid rendert den Hinweis nicht mehr bedingt"
    if any_legacy:
        assert "alte" in grid and "Design" in grid, "Hinweis-Text fehlt in VideoGrid.astro"
    else:
        pytest.fail(
            "Kein Video mehr als legacyDesign markiert — Hinweis in VideoGrid.astro "
            "und diesen Test entfernen."
        )


# ---------------------------------------------------------------------------
# Anleitungs-Abschnitte
# ---------------------------------------------------------------------------
def test_section_order_is_unique_and_gapless(sections):
    orders = sorted(fm["order"] for _, fm in sections)
    assert orders == list(range(1, len(orders) + 1))


def test_sections_have_titles(sections):
    for path, fm in sections:
        assert fm.get("title"), f"{path.name}: kein Titel"


def test_internal_links_resolve_to_real_files(sections):
    """`internal`/`download` hrefs müssen unter site/public/ existieren.

    Ausnahme: '/' und andere von Astro generierte Routen — die haben keine
    Datei in public/. Erkennbar daran, dass sie nicht auf eine Dateiendung
    zeigen.
    """
    for path, fm in sections:
        for link in fm.get("links") or []:
            if link["kind"] == "external":
                continue
            href = link["href"]
            if not Path(href).suffix:
                continue  # Astro-Route, kein statisches Asset
            asset = PUBLIC / href.lstrip("/")
            assert asset.is_file(), f"{path.name}: {href} fehlt unter site/public/"


def test_link_kinds_are_known(sections):
    for path, fm in sections:
        for link in fm.get("links") or []:
            assert link["kind"] in {"internal", "download", "external"}, (
                f"{path.name}: unbekannter link kind {link['kind']!r}"
            )


def test_gotham_narrow_is_not_offered_for_download(sections):
    """Gotham Narrow ist lizenzpflichtig — nur der Verweis aufs Landesbüro.

    Die GGS-Seite bot die Schrift als ZIP an; das darf hier nicht passieren.
    """
    for path, fm in sections:
        for link in fm.get("links") or []:
            assert "gotham" not in link["href"].lower(), (
                f"{path.name}: Gotham Narrow darf nicht zum Download angeboten werden"
            )
