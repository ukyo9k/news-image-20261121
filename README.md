# The World Today — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/ukyo9k/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/ukyo9k/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image summing up the world's news of **Saturday 21 November 2026**, built for the
[make.fun bounty](https://make.fun/bounty/news-image-20261121) of the same name.

## The image

`entry.png` (1024 × 1024) is a front-page poster of the day:

- **Lead:** Russian missiles land in Poland during a huge overnight barrage on Ukraine — NATO calls it a grave violation — as three bridges across the Dnipro in Kyiv are hit and at least nine people are killed.
- **Markets:** the S&P 500 and the Dow enter correction territory as AI shares plunge.
- **Europe:** Britain and the EU seal deals on food trade, carbon markets and youth mobility at a Brussels summit.
- **Justice:** a Los Angeles jury convicts Jonathan Rinderknecht of starting the deadly 2025 Palisades Fire.
- **Health:** a pancreatic-cancer pill combined with chemotherapy shrinks tumours in 6 in 10 patients in early trial data.
- **Climate:** the COP31 talks in Turkey enter their final stage, with fossil fuels and climate finance unresolved.
- **Weather:** Cyclone Akvan weakens after landfall near Gopalpur, India, where about 370,000 people were evacuated; heavy rain lingers into Saturday.

Every story was reported on 21 November 2026 (overnight and Asia–Pacific morning reports) and is
sourced from Reuters, AP, the BBC, the India Meteorological Department and the US Department of Justice.

## How it is made

`draw_poster.py` draws the poster from scratch with Pillow (run locally to regenerate
`entry.png`). `main.py` is the entrypoint: Python 3.13 standard library only, it copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, deterministically — two runs produce
byte-identical output.

```sh
python3 draw_poster.py   # regenerate entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
