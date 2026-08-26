# Codebase Research — imtas

Small, self-contained issue. Investigated directly (no sub-agent fan-out needed).

## Data source: site/src/data/videos.ts

- `export interface AnleitungsVideo { youtube: string; title: string; description?: string; duration?: string; poster?: string; legacyDesign?: boolean; }`
- Only `youtube` + `title` are required. `duration` is explicitly documented as optional, format `"M:SS"`.
- `posterFor(v)` → `v.poster ?? https://i.ytimg.com/vi/${v.youtube}/maxresdefault.jpg`
- `posterFallbackFor(v)` → `https://i.ytimg.com/vi/${v.youtube}/hqdefault.jpg` (client-side `onerror` fallback wired in VideoGrid.astro's inline script)
- `watchUrl(v)` → `https://www.youtube.com/watch?v=${v.youtube}`
- Current `videos` array has exactly 4 entries, all with `legacyDesign: true` and a `duration`.
- File header doc-comment (lines 1-19) already documents the "add/replace video" workflow and explicitly says only `youtube` + `title` are needed — matches the issue's ask to drop `legacyDesign` entirely and treat `duration` as optional.

## Consumers of `videos` / VideoGrid

`VideoGrid` is used in TWO places, not just `/anleitung/`:
- `site/src/pages/anleitung/index.astro` (line 55): `<VideoGrid videos={videos} modalId="anleitung-video" />`
- `site/src/pages/templates/[...id].astro` (line 135): `<VideoGrid videos={videos} modalId="template-video" />` — every template detail page also renders the same grid+notice.

Both consume the same shared array, so the legacy-notice removal and grid layout change apply to both surfaces. Issue's acceptance criteria only mention `/anleitung/` explicitly, but the template-detail pages get the same fix for free (and would break if forgotten).

## VideoGrid.astro (site/src/components/VideoGrid.astro)

- `const hasLegacyDesign = videos.some(v => v.legacyDesign);` — line 26.
- Notice block (lines 28-36) is a `gat-callout gat-callout--info app-video-notice`, only rendered `{hasLegacyDesign && (...)}`. Confirmed: once no entry has `legacyDesign: true`, `hasLegacyDesign` is `false` and the whole `<p>` is not rendered. No other place references `legacyDesign` — removing the flag from all data entries is sufficient, no markup edit needed (issue explicitly says the block may stay in the file, unrendered).
- Grid markup (lines 38-74): maps `videos` to `<a class="app-video-card">` cards; poster `<img>`, play badge, optional `<span class="app-video-card__duration">` (only rendered if `v.duration` truthy — so omitting `duration` is fully safe, no broken layout).
- Card `href={watchUrl(v)}` is the no-JS fallback link; `data-video-id`/`data-video-title` feed the modal open() call. Confirmed these are driven purely by `v.youtube`/`v.title` — no hardcoded video count or IDs in this component.

## VideoModal.astro

- Generic modal driven by `data-video-target`/`data-video-id`/`data-video-title` attributes set in VideoGrid — no video-count assumptions, no changes needed for this issue.

## Grid CSS: site/src/styles/app.css

```css
/* line 934 */
.app-video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}
...
@media (max-width: 640px) {   /* line 1132 */
  .app-video-grid {
    grid-template-columns: 1fr;
  }
}
```

Important: this is NOT a fixed 4-column grid — it's `auto-fill` with a 220px minimum card width. Commit c180fcb (see below) tuned the 220px minimum specifically so **4** cards fit in one row at desktop width; the "four columns" in the issue description is a side-effect of that minimum, not an explicit `repeat(4, ...)` rule.

With only 2 cards and `auto-fill`, the grid will NOT stretch each card to a quarter of the row width — `auto-fill` (as opposed to `auto-fit`) still reserves the grid tracks for the *would-be* additional columns implied by the container width, so on wide viewports 2 real cards + empty tracks can look like "two cards floating far apart on the left with dead space," OR (depending on exact `auto-fill` semantics — the implicit empty tracks stay zero-width if there isn't enough space, they only appear if the container is wide enough to physically fit more 220px tracks) very likely 2 narrow cards on the left with a large empty gap on a 1280px viewport, since 1280px / 220px ≈ 5 potential tracks are available. This is the exact "kein halbleeres Vier-Spalten-Raster" acceptance criterion the issue calls out.

**Fix options** (planner should pick one, not exploratory):
1. Switch `auto-fill` → `auto-fit` on `.app-video-grid`. `auto-fit` collapses empty tracks to 0 width and lets the existing fractional units (`1fr`) expand the real cards to fill the row — with 2 cards this makes each card grow to fill the available row width evenly, still capped by nothing (could get very wide on ultra-wide screens, since there's no `max-width` on the card). This is the standard, minimal, single-line CSS fix for "empty grid tracks when there are few items" (`auto-fill` vs `auto-fit` is the textbook CSS Grid distinction for exactly this problem).
2. Add a `max-width` cap or cap the grid to e.g. `minmax(220px, 340px)` so cards do not stretch too wide.
3. Add a video-count-aware class/breakpoint. Overkill for a static 2-item array.

Recommendation: `auto-fit` (option 1) is the smallest, most idiomatic fix, consistent with a "kleines Issue" scope. It does not need markup changes, just a CSS keyword change in `app.css` around line 936. Worth pairing with a modest max card width (e.g. `minmax(220px, 320px)`) so 2 cards don't stretch edge-to-edge on very wide viewports — comment in the file already explains the current 220px choice, so the same comment block should be updated to reflect the new reasoning (2 cards, not 4).

## Recent git history (relevant commits)

- `c180fcb` "Video-Modal zentrieren und Grid auf vier Spalten stellen" (2026-08-20): dropped `.app-video-grid` minmax from 260px → 220px specifically so 4 cards fit one row at desktop width (reflow noted in commit message: 4/4/2/1 cards at 1280/1024/768/375px). Also fixed modal centering (unrelated to this issue, do not touch).
- `120c54e` "Hinweis ergaenzen, dass die Videos im alten Design aufgenommen sind" (2026-08-20): introduced `legacyDesign` flag + `hasLegacyDesign` conditional render in VideoGrid.astro, plus the test `test_legacy_design_notice_matches_the_data` in tests/unit/test_site_anleitung_content.py. The commit message explicitly anticipated this exact issue: "Sind alle Videos neu aufgenommen, verschwindet der Hinweis von selbst."

Both files are stable / not in active development — no pending PRs found, no other branches touching them (single-branch worktree, clean status).

## Existing tests that WILL break and must be updated

`tests/unit/test_site_anleitung_content.py` (Python/pytest):

```python
EXPECTED_VIDEO_IDS = {
    "ZH9z7Cgiuy0", "GxKJLRHjvIs", "uBMazvTPPLI", "90rbNKbOlMM",
}

def test_video_ids_are_complete():
    ids = set(re.findall(r"youtube:\s*'([^']+)'", _videos_array()))
    assert ids == EXPECTED_VIDEO_IDS   # WILL FAIL once videos.ts is edited

def test_every_video_has_a_title():
    entries = re.findall(r"\{\s*youtube:.*?\n\s*\}", _videos_array(), re.S)
    assert len(entries) == len(EXPECTED_VIDEO_IDS)   # count-coupled, WILL FAIL
    ...

def test_legacy_design_notice_matches_the_data():
    ...
    any_legacy = "legacyDesign: true" in _videos_array()
    assert "hasLegacyDesign" in grid, ...
    if any_legacy:
        assert "alte" in grid and "Design" in grid, ...
    else:
        pytest.fail(
            "Kein Video mehr als legacyDesign markiert — Hinweis in VideoGrid.astro "
            "und diesen Test entfernen."
        )
```

This test file was DESIGNED to force this exact update: once no video has `legacyDesign: true`, `test_legacy_design_notice_matches_the_data` unconditionally fails with an explicit instruction in the failure message to remove both the notice markup AND this test. The plan must include:
1. Update `EXPECTED_VIDEO_IDS` to `{"SDT9eM9tReU", "3rMFX_VLvpE"}` (and update/remove the inline ID→title comments).
2. Either delete `test_legacy_design_notice_matches_the_data` entirely (as the fail message instructs) — note the issue says "der Hinweis-Block darf im Markup bleiben", so `hasLegacyDesign` stays in VideoGrid.astro; only the *test's* legacy-branch logic needs removing/adjusting, not the component code.
3. `test_every_video_has_a_title` only depends on `len(EXPECTED_VIDEO_IDS)`, so updating the constant fixes it automatically.

No other test files reference `videos.ts`, `legacyDesign`, or `duration` (confirmed via grep across `tests/` and `site/src/`).

## Build/test commands (verified in this environment)

- `cd site && npm run build` — Astro build. Confirmed green baseline (26 pages built, 3.4s). `site/node_modules` already installed in this worktree.
- `cd site && npm run check` — `astro check` (not run, but available; no TS errors expected from a data-only change).
- Python tests: `/root/.local/bin/pytest tests/unit/test_site_anleitung_content.py -q` — confirmed works (8 passed) in this container; plain `pytest`/`python3 -m pytest` is NOT on PATH by default (`python3 -m pip list` shows no pytest under the default python3; it lives under `/root/.local/bin/pytest` and `/opt/sortition-venv/bin/pytest`). Use the full path or ensure `/root/.local/bin` is on PATH.
- CI (`.github/workflows/ci.yml` line 75): `pytest tests/unit/ -q --ignore=tests/unit/test_idml_strict_mode.py` — the anleitung test file is included in this run.
- `bin/ci-local` mirrors `.github/workflows/pages.yml`'s build job (`npm run build` inside `site/`); supports `--no-site` to skip the Astro build for faster iteration, but this issue IS the Astro build, so run it with the site step.

## No poster/screenshot assets needed

`posterFor()` derives the poster URL purely from the YouTube ID (`maxresdefault.jpg` with `hqdefault.jpg` client-side fallback) — no files need to be added under `site/public/`.
