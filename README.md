# The Sunday Gazette — 40 stories from Sunday 22 November 2026 (v2, Monday refresh)

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Valkyra54/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Valkyra54/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

<sub>Entered on [make.fun](https://make.fun/?ref=nbgfvtz4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

One image summing up the world's news of **Sunday 22 November 2026** — 40 stories
across 5 continents, drawn as a newspaper front page: masthead, 3 lead banners,
12 illustrated tiles, a markets strip, a "WHERE IT HAPPENED" world-map band with
12 pins, a 24-item ALSO list, and a sources footer.

**v2 (Monday refresh):** COP31 collapsed — no deal on climate (Antalya) ·
Verstappen wins the Las Vegas GP · Bitcoin $60,784 · Manipur toxic alcohol
18 dead, 228 in hospital · Cikande factory fire 3 dead, 39 missing ·
Bahrain hit, 2 hurt; 2 tankers struck; Riyadh drone down.

**Leads:** COP31 collapses — no deal · The Gulf ignites — Bahrain, Hormuz,
Riyadh · Bitcoin back above $60,000 after Saturday's two-year low.

**How it runs:** `main.py` is stdlib-only (the grader has no Pillow). It validates
the pre-rendered `entry.png` (PNG signature, IHDR dims 1024×1024, < 1 MiB, IEND
tail) and copies it to `$MAKEFUN_OUTPUT_DIR` (default `/output`). The image itself
is rendered at build time by `render.py` (PIL, build machine only) from the 40
verified stories in the research notes — COP31, the Gulf escalation, Bitcoin,
the Cikande factory fire, F1 Las Vegas, and 35 more.

## Run

```sh
python3 main.py
```

## Sources

BBC · Reuters · Channel News Asia · Bloomberg · MKT News · AP · CNN · Finnhub ·
INDECI · ESA/JAXA
