# Pitfalls Research — imtas

## Video metadata: `duration` cannot be reliably fetched here

Verified both new videos exist and titles match exactly via YouTube's public oEmbed endpoint
(`https://www.youtube.com/oembed?url=...&format=json`):

- `SDT9eM9tReU` → title "Erste Schritte mit Scribus", author "Die Grünen Niederösterreich" (HIGH confidence — matches issue and channel).
- `3rMFX_VLvpE` → title "Export einer Scribus Datei", author "Die Grünen Niederösterreich" (HIGH confidence).

oEmbed does NOT return duration (YouTube's oEmbed response has no `duration` field), and WebFetch
against the watch page itself only returns static/pre-render markup (player chrome is JS-rendered
client-side), so no reliable duration could be extracted through available tools (LOW confidence /
not obtainable this way — would need the YouTube Data API v3 with an API key, or manual lookup in a
browser). Since `duration` is an optional, purely cosmetic field (only renders a small badge if
present — `site/src/components/VideoGrid.astro` line 66) and nothing in the codebase or tests
enforces its presence or format, the safe default is to add the two new entries WITHOUT `duration`,
or have the human who added the issue fill it in manually if they have it. Do not fabricate a
duration value.

## CSS Grid `auto-fill` vs `auto-fit` — the actual root cause of the "empty grid" risk

`.app-video-grid` uses `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));`. This is a
well-documented CSS Grid distinction:
- `auto-fill` keeps reserving as many tracks as fit the container width, even if some end up empty —
  so with only 2 real items on a wide viewport, the 2 cards stay pinned to their intrinsic width and
  leave visible empty grid tracks after them (looks like items are stuck on the left / not filling
  the row).
- `auto-fit` collapses the empty tracks to `0` and lets `1fr` distribute the remaining space across
  the actual items — with 2 items this makes both cards expand evenly to fill the row.

This is standard, well-established CSS Grid behavior (not something needing external verification
beyond spec knowledge) — HIGH confidence. The fix is a one-line swap (`auto-fill` → `auto-fit`) in
`site/src/styles/app.css`. Recommend also bounding the max card width (e.g.
`minmax(220px, 320px)`) so 2 cards don't stretch edge-to-edge/oversized on ultra-wide monitors —
without a cap, `auto-fit` + `1fr` can make each of only 2 cards grow arbitrarily wide.

## Test coupling gotcha

`tests/unit/test_site_anleitung_content.py` hardcodes the 4 legacy video IDs in
`EXPECTED_VIDEO_IDS` and has a test (`test_legacy_design_notice_matches_the_data`) that is
*designed* to hard-fail once no video carries `legacyDesign: true` anymore, with an explicit
message instructing the test to be removed. Easy to miss if only `site/` is touched and the
Python test suite isn't run — `npm run build` will NOT catch this, only `pytest tests/unit/` will.
Must run both build and pytest before considering the issue done (issue's own acceptance criterion
"Build laeuft durch" only covers half of the gate; CI additionally runs
`pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py`).

## Environment availability (probed in this worktree)

| Tool | Available | Version | Notes |
|---|---|---|---|
| node | yes | v26.7.0 | |
| npm | yes | 11.19.0 | `site/node_modules` already installed |
| python3 | yes | 3.13.5 | plain `python3 -m pip list` has no pytest |
| pytest | yes, but not on default PATH | via `/root/.local/bin/pytest` (also `/opt/sortition-venv/bin/pytest`) | use full path, 8/8 existing anleitung tests pass as baseline |
| PyYAML | yes | 6.0.3 | required by the test file (`import yaml`) |

## Security / scope

None — pure content/data + CSS change, no new dependencies, no vendoring (YouTube stays embedded
via existing `youtube-nocookie.com` iframe mechanism, untouched).
