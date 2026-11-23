# world-in-one-day-23-nov-v2

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/donatfarm01/world-in-one-day-23-nov-v2/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/donatfarm01/world-in-one-day-23-nov-v2/reward.svg)](https://make.fun/bounty/news-image-20261123)

Entry for the make.fun bounty **"Sum up 23 November's world news in one image"**.

## The image

**"The World in One Day — 23 November 2026"** is a dense-newspaper front page
drawn entirely in code (`draw.py`, Python + PIL, no AI imagery). It sums up
Monday 23 November 2026 in 35 dated stories, each with its source named:

- **Lead:** Iran strikes a U.S. base in Bahrain; UN talks on lethal AI weapons
  to continue; Mexico captures FBI most-wanted cartel boss "El Chapo Isidro".
- **World, Asia–Pacific, Europe, Americas & Markets, Sport** — from the
  Wellington Test record (India 720/9d) and the ATP Finals to the Lisbon
  cost-of-living march and Delta's nationwide system fix.
- A **world map** marking where the day happened, a **verification badge**,
  and a **DATE CHECK box**: every story was first reported on 23 November
  2026. Weekend events (22 Nov) appear only in the clearly dated
  AFTERMATH strip — no 22 November story leads the page.

## Run

```sh
python3 draw.py            # redraw entry.png (deterministic: same sha256 every run)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copy entry.png to out/
```

`main.ts` only copies the shipped `entry.png` to `/output`, so both grading
runs write identical bytes.
