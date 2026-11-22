# Saturday 21 November 2026: 49 dated stories, 9 regions

![bounty](https://make.fun/badge/news-image-20261121.svg)
![rank](https://make.fun/badge/news-image-20261121/vjmunggahari-ui/news-image-20261121-v4-ono10/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/vjmunggahari-ui/news-image-20261121-v4-ono10/reward.svg)

**Saturday 21 November 2026: 49 dated stories, 9 regions — Iran hits Bahrain bases, deep Peru quake, COP31 overtime.**

One broadsheet front page that sums up the day's world news: a UTC
timeline, six big numbers, a 9-region bar, three hero panels with original
drawn scenes (the Gulf strikes, the Peru quake cross-section, the COP31
calendar), 13 numbered mid stories with mini-drawings, a dotted world map
with numbered pins, and 33 more stories in the also-list — 49 in all.

Every story carries a **half-life tag** instead of a confidence tag: how
long the story will matter, not how sure we are of it. **FLASH** (gone by
Monday), **DEVELOPING** (settles in weeks), **STRUCTURAL** (shifts the
board for a year or more). Every hero story also carries a **NEXT** line —
what to watch next. A date-check box names the older news left out on
purpose and the events not yet happened; a watch strip lists Sunday's five
things to follow.

## How it works

- `stories.json` — all 49 stories, each dated, sourced, regioned and
  half-life tagged. Every story happened, or was first reported, on
  Saturday 21 November 2026.
- `tools/render.py` — draws the front page with Pillow (fixed fonts, fixed
  geometry, no timestamps). Deterministic: run it twice, the bytes match.
- `main.ts` — copies `entry.png` to `MAKEFUN_OUTPUT_DIR` and reads it back,
  verifying size, PNG signature, IEND trailer, 1024×1024 dimensions and
  sha256 before exiting.
- `entry.png` — the front page: 1024×1024, 249,534 bytes.

## Run it

```sh
node main.ts            # writes entry.png to ./output (or $MAKEFUN_OUTPUT_DIR)
```

## Lead events

- Iran hits US bases in Bahrain; two tankers struck off Oman (IRGC claim;
  Bahrain says a civilian plant burned; UKMTO reports the tankers).
- Deep 6.7 quake shakes central Peru at 00:09 UTC; a second M6.8 in the
  Banda Sea rattles Darwin hours later.
- COP31 runs into overtime in Antalya with no deal; final vote Sunday.
