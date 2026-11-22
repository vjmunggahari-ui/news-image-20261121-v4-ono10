# NOTES — news-image-20261121 v4

## What this entry is

A broadsheet front page for Saturday 21 November 2026: **49 stories, 9
regions** (Middle East 5, Europe 12, Asia 9, Africa 5, N. America 9,
S. America 4, Oceania 3, Global 1, Space 1). Target: judge 989,000+
(top-50 bar was 988,923 when studied; v3 sits at 974,723).

## The distinctive system: half-life tags

The live #4 entry tags every story by confidence (CONFIRMED / REPORTED /
CLAIM). This entry deliberately does something else: every featured story
carries a **half-life tag** — how long the story will matter.

- **FLASH** — gone by Monday (a quake shock, a scoreline, a fire).
- **DEVELOPING** — settles in weeks (Bitcoin's bear market, a patrol standoff).
- **STRUCTURAL** — shifts the board for a year or more (a Gulf war, a trade
  pact, a climate summit with no deal).

On top of that, each hero story carries a **NEXT** line (what to watch
next), and the foot of the page carries a **WATCH ON SUNDAY** strip with
five timed items. The page answers "what happened" and "what happens next",
not "how sure are we".

## Live top-10 study (22 Nov ~15:20 WIB, 15,139 ranked entries)

- #1 992,049 — 35 stories, 9 regions, newspaper front page, map, date check.
- #2 991,548 — "Saturday 21 November 2026 in one picture", 35 stories.
- #3 991,529 — 36 stories, 7 regions.
- #4 991,256 — 49 stories, 7 regions, 41 fields, confidence tagging.
- #5 991,188, #8 991,188-class (42 stories, 7 regions, drawn scenes).
- Top-50 bar 988,923; top-100 bar 987,470. v3 (ono10) #3034 at 974,723.

Winning pattern across the top 10: masthead + date + count, UTC timeline,
big-number stat boxes, region bar, 3 hero panels with original drawn
scenes, ~13 numbered mid stories, dotted world map with pins, an
also-list to reach the count, a date-check box, source attributions.
v4 follows that grammar (it is the genre) with its own layout, drawings,
wording and the half-life system above — it does not copy #4's tagging.

## Skill / relay report (Step 0, mandatory)

Skills used:

- **viralforge** — deconstructed the top entries' structure (hook in the
  first line, density rhythm, stat-box cadence) and transferred the
  structure, not the content: masthead → timeline → numbers → heroes →
  list → date check.
- **media-judge** — measured QA on the render (see below): found the
  stray navy triangles from an absolute-coordinate bug in the jets
  mini-scene, hero-deck/source collisions, and the date-check overflow;
  re-measured after each fix until no defect remained.
- **canvas-design** — design philosophy: "Concrete Poetry" — monumental
  form, bold geometry, text as rare gesture; paper ground, red + navy,
  serif display type, information encoded spatially (region bar, map
  pins, half-life chips).

Relays used (same prompt to all seven; public news facts only, no
wallet/key/finding material):

- **Groq (gpt-oss-20b)** — answered. Proposed a "Narrative Resonance
  Index" (not used — gimmicky) and the hook "49 Stories, 9 Regions, One
  Pulse" (not used verbatim). No extra stories.
- **Xkiro (ministral-14b)** — answered. Proposed an "Iconic Silhouette
  Collage" (informed the hero-scene drawings). Its extra stories carried
  invented specifics (hypersonic missiles, buried villages) — discarded,
  unverified.
- **Bluesminds (ising-calibration-1.5-31b)** — answered. Proposed one
  unique stylised icon per story — adopted as the mini-drawings. Its extra
  stories were repeats of the given list.
- **Requesty (gemma-4-31b-it)** — answered. Proposed a "Tectonic Weight"
  1–5 scale; folded into the STRUCTURAL tag's meaning. Its extra stories
  (Artemis III habitat, UN AI treaty, Tokyo fusion district) read as
  fabrications — discarded, unverified.
- **Coarena** — DEGRADED. claude-fable-5 and claude-haiku-5-5 both return
  402 (not in the free tier); the free-tier model names from the error
  are not listed by the models endpoint (404 for deepseek-v4.1-flash-1017).
  No answer obtained; not retried further.
- **100milionseek (deepseek-v4.1-flash-free)** — answered. Proposed the
  **"Half-Life tags"** (Flash / Developing / Structural) — ADOPTED as the
  entry's distinctive per-story system — and the hook "A world on
  overtime: quakes, tariffs and a last-lap title" (adapted into the deck).
  Its three extra stories were flagged by the model itself as
  unverifiable candidates; none used without a source check.
- **Xingchi** — DEGRADED. chat/completions returns 400
  (chat_completions_disabled — Responses API only); the codex CLI fails
  (code-mode host executable missing). No answer obtained.

Relay claims were treated as untrusted: every fact on the page was checked
against same-day reporting (search results, 22 Nov) or against agreement
between two or more live top-10 entries. Relay-invented specifics were
discarded.

## Fact checks (22 Nov, same-day reporting)

- Peru M6.7: 00:09 UTC Sat 21 Nov, near Junin, USGS depth 108 km
  (IGP 129 km), felt in Lima, no tsunami threat. First reports: no deaths.
- Banda Sea M6.8: 09:42 UTC, 226 km NE of Dili (GFZ) / 103 km NE of
  Lospalos (USGS), felt in Dili and Darwin, no tsunami threat.
- IEU-CEPA: signed Brussels 21 Nov; 90.4% of Indonesian tariff lines
  duty-free from day one; 98.5% is the EU-goods-into-Indonesia figure.
  In force 2027 after ratification.
- Bitcoin: low $55,130–$55,251.60 (two-year low, weakest since Sep 2024),
  then +9% back over $60,000 (Reuters / CoinDesk).
- Iran / Bahrain: IRGC claims missile + drone strikes on US positions at
  al-Riffa and Awali, two Patriot radars destroyed (claim); Bahrain says a
  civilian industrial facility burned, no injuries; UKMTO: two tankers hit
  off Khasab (stern 20 km N, engine room 31 km E).
- "El Chapo Isidro": Fausto Isidro Meza Flores captured Fri night in
  Guasave, Sinaloa, with US intelligence; 11 die (7 gunmen, 4 soldiers);
  FBI Top 10, $5m reward; announced Sat 21 Nov.
- Houthi missiles over Riyadh (Fri 23:43 UTC) are deliberately LEFT OUT
  in the date-check box — first reported before Saturday (UTC).

## Media-judge QA (self-judged; fresh-eyes note)

Measured on the final render (entry.png, 1024×1024, 249,534 bytes,
sha256 9284150ea36dcfbe3a460d093148c2e3eee582511eb4a5473d42f8845f886e9b):

- Defects found and fixed: (1) stray navy triangles over the kicker —
  absolute y-coordinates in the jets mini-scene (yy 14/26 instead of
  y+14/y+26), caught by pixel scan, fixed, re-verified 0 stray pixels;
  (2) hero decks colliding with source/NEXT lines — decks shortened to
  ≤3 lines, layout re-stacked; (3) mid-story decks overflowing rows —
  decks shortened to ≤2 lines, rows raised to 74 px; (4) Gulf scene
  clutter — redrawn, Khasab dot moved off its label; (5) date-check
  text overflowing its box — box raised to 28 px, text shortened.
- Final state: no measured defect. 49 stories counted in stories.json
  (3 hero + 13 mid + 33 list); 9 region counts sum to 49; all 16
  featured stories have a half-life chip and a source line; all text
  legible at full size with no overlaps; map pins 1–16 placed (7 and 8
  placeless, noted on the page).
- Determinism: render.py run twice → identical sha256.
  main.ts run twice → identical output bytes.
- Not settled by this run: how the AI judge ranks the image against the
  live top 10 (only the platform can measure that).

## Badges (README)

- rank.svg → 200, reward.svg → 200 (verified 22 Nov, pre-submit).
- bounty.svg → **404** `{"success":false,"error":[{"message":"no badge
  news-image-20261121/vjmunggahari-ui/news-image-20261121-v4-ono10/bounty.svg"}]}`.
  The same 404 occurs for the already-submitted news-image-20261122 entry,
  so no bounty badge exists for this competition family — it is a
  platform-side absence, not a repo problem. All three lines are kept in
  the README as briefed; the parent may drop the bounty line at submit time.

## Verification (grader-like, before finishing)

- Read-only copy of the repo, run as an unprivileged user with
  MAKEFUN_OUTPUT_DIR set: exit 0, entry.png written to the OUT dir
  (not the repo), sha256 matches.
- main.ts: written, run, EDITED (added source-hash + IEND trailer
  checks), re-run twice byte-identical.
