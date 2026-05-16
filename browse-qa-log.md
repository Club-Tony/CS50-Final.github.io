# browse-qa-log — CS50 Final (Flask website)

Dated log of `/browse`-driven interactive QA sweeps against the static HTML pages under `CS50 flask website/`. The project's README notes "haven't updated code since importing from cs50 codespace. Some links could be broken." — there is no `app.py`, so sweeps run against `python -m http.server`. See `Repositories/Agent-Hub/Plans/browse-driven-qa-targets.md` for the per-target checklist.

---

## 2026-05-14 — initial sweep (Plan Phase 5)

**Scope:** route smoke, Bootstrap conflict, responsive.

**Setup:** `python -m http.server 8088 --bind 127.0.0.1` from `CS50 flask website/`. **Note:** port 5060 is on Chromium's `ERR_UNSAFE_PORT` blocklist (SIP) — avoid that and similar well-known service ports when serving static.

**Pass:**
- T12-1 Route smoke: `index.html`, `chickennuggets.html`, `hedgehog.html`, `soundcloud.html`, `cover.html` all return HTTP 200 and render an `<h1>`.
- T12-4 Responsive @ 375 px: no body overflow, h1 visible.

**Bugs found:**

- **F-CS50-1 — Bootstrap version conflict on `index.html`.** Both 5.2.3 and 4.5.3 CSS and JS bundles are loaded simultaneously, so the two stylesheets compete and the second-loaded JS clobbers the first. Picking one version and removing the other is the right cleanup.
- **F-CS50-2 — Broken embedded media.** `soundcloud.html`'s SoundCloud embed (`tracks/1605811671`) returns HTTP 403 — track removed or made private. Embedded YouTube video (`O0RO5FnVmPM`) reports `Video_unavailable` in QoE stats. Either swap to current content or remove the embeds.

**Status:** project is dormant. These findings are documented for future revival; no fix planned in this sweep.
